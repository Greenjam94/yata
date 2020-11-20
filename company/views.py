"""
Copyright 2020 kivou.2000607@gmail.com

This file is part of yata.

    yata is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    yata is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with yata. If not, see <https://www.gnu.org/licenses/>.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

# cache and rate limit
from django.views.decorators.cache import cache_page
from ratelimit.decorators import ratelimit
from ratelimit.core import get_usage, is_ratelimited

import math
import json

from company.models import CompanyDescription
from company.models import Company

from yata.handy import *
from player.models import Player
from player.functions import updatePlayer


def index(request):
    try:
        player = getPlayer(request.session.get("player", {}).get("tId", -1))

        context = {"player": player, "compcat": True, "view": {"index": True}}
        page = 'company/content-reload.html' if request.method == 'POST' else 'company.html'
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)

def browse(request):
    try:
        player = getPlayer(request.session.get("player", {}).get("tId", -1))

        # get all companies
        companies = CompanyDescription.objects.order_by("name")

        if request.POST.get("type") == "company-details":
            company_details = companies.filter(tId=request.POST.get("company_id")).first()
            print(company_details)
            return render(request, "company/browse/details.html", {"player": player, "company_details": company_details})

        page = 'company/content-reload.html' if request.method == 'POST' else 'company.html'
        context = {"player": player, "companies": companies,"compcat": True, "view": {"browse": True}}
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)

def supervise(request):
    try:
        player = getPlayer(request.session.get("player", {}).get("tId", -1))

        # get company
        company = Company.objects.filter(tId=player.companyId).first()
        if company is None and not player.companyDi:
            context = {"player": player, "compcat": True, "view": {"supervise": True}}
            page = 'company/content-reload.html' if request.method == 'POST' else 'company.html'
            return render(request, page, context)
        elif company is None and player.companyDi:
            updatePlayer(player)
            company = Company.objects.filter(tId=player.companyId).first()
            company.update_info()

        # add employees requirements and potential efficiency on the fly
        company_positions = company.company_description.position_set.all()
        employees = company.employee_set.all().order_by("-effectiveness_total")
        for employee in employees:
            position = company_positions.filter(name=employee.position).first()
            employee.man_required = 0 if position is None else position.man_required
            employee.int_required = 0 if position is None else position.int_required
            employee.end_required = 0 if position is None else position.end_required
            t = employee.effectiveness_total
            n = employee.effectiveness_addiction + employee.effectiveness_inactivity
            employee.effectiveness_potential = 100 * (t + n) / max(t, 1)

        # send employees if show details
        if request.POST.get("type", False) == "show-details":
            company_data = company.companydata_set.filter(timestamp=request.POST.get("timestamp")).first()
            if company_data is not None:
                employees = json.loads(company_data.employees)
            return render(request, "company/supervise/details.html", {"company_data": company_data, "employees": employees})

        # get company data
        company_data = company.companydata_set.all().order_by("-timestamp")
        company_data_p = Paginator(company_data, 25)
        if request.GET.get('page') is not None:
            return render(request, "company/supervise/logs.html", {"company_data_p": company_data_p.get_page(request.GET.get('page'))})

        # create employee graph
        # current employees [id, name]
        employee_graph_headers = [[str(e.tId), f'{e.name} [{e.tId}]'] for e in employees]
        employee_graph_data = []
        for data in company_data:
            d = json.loads(data.employees)
            tmp_data = [data.timestamp, []]
            for e_id, e_name in employee_graph_headers:
                tmp_data[1].append([d.get(e_id, {}).get("effectiveness_total", "undefined"), d.get(e_id, {}).get("position", "undefined")])
            employee_graph_data.append(tmp_data)

        employees_graph = {"header": employee_graph_headers, "data": employee_graph_data}

        context = {"player": player,
                   "company": company,
                   "company_data": company_data,
                   "company_data_p": company_data_p.get_page(1),
                   "employees": employees,
                   "employees_graph": employees_graph,
                   "compcat": True,
                   "view": {"supervise": True}}

        page = 'company/content-reload.html' if request.method == 'POST' else 'company.html'
        return render(request, page, context)

    except Exception as e:
        return returnError(exc=e, session=request.session)


@cache_page(60*10)
def ws(request):
    payload = {"effectiveness": []}
    for company in Company.objects.all():
        if not company.director:
            print("no director")
            continue

        # add employees requirements and potential efficiency on the fly
        company_positions = company.company_description.position_set.all()
        employees = company.employee_set.all().order_by("-effectiveness_total")

        manager = employees.filter(position="Manager").first()
        manager_effectiveness = manager.effectiveness_total if manager is not None else 0
        for employee in employees:
            position = company_positions.filter(name=employee.position).first()
            if position is None:
                continue

            employee.man_required = 0 if position is None else position.man_required
            employee.int_required = 0 if position is None else position.int_required
            employee.end_required = 0 if position is None else position.end_required
            t = employee.effectiveness_total
            n = employee.effectiveness_addiction + employee.effectiveness_inactivity
            # compute theoretical efficiency
            req = [employee.man_required, employee.int_required, employee.end_required]
            sta = [employee.manual_labor, employee.intelligence, employee.endurance]
            Pi = req.index(max(req))
            Si = req.index(min([s for s in req if s]))
            P = sta[Pi] / float(req[Pi])
            S = sta[Si] / float(req[Si])
            # P = round(sta[Pi] / float(req[Pi]), 0)
            # S = round(sta[Si] / float(req[Si]), 0)
            # P = math.ceil(sta[Pi] / float(req[Pi]))
            # S = math.ceil(sta[Si] / float(req[Si]))
            employee.effectiveness_theoretical = math.ceil(min(60, 60 * P) + max(0, 5*math.log2(P)) + min(30, 30 * S) + max(0, 5*math.log2(S)))
            employee.effectiveness_theoretical = min(60, 60 * P) + max(0, 5*math.log2(P)) + min(30, 30 * S) + max(0, 5*math.log2(S))

            # employee.effectiveness_theoretical = min(60, 60 * P) + math.ceil(max(0, 5*math.log2(P))) + min(30, 30 * S) + math.ceil(max(0, 5*math.log2(S)))
            employee.effectiveness_potential = 100 * (t + n) / max(t, 1)
            ws = {
                  "working_stats": employee.effectiveness_working_stats,
                  "settled_in": employee.effectiveness_settled_in,
                  "director_education": employee.effectiveness_director_education,
                  "addiction": employee.effectiveness_addiction,
                  "inactivity": employee.effectiveness_inactivity,
                  "management": employee.effectiveness_management,
                  "book_bonus": employee.effectiveness_book_bonus,
                  "effectiveness_total": employee.effectiveness_total,
                  "manager_effectiveness": manager_effectiveness,
                  "position": employee.position,
                  "director_hrm": company.director_hrm,
                  "primary_ratio": P,
                  "secondary_ratio": S
                  }

            payload["effectiveness"].append(ws)

    return JsonResponse(payload, status=200)
