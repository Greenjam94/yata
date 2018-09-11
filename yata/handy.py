from django.utils import timezone


def apiCall(section, id, selections, key, sub=None):
    import requests

    # if selections == "chain" and section == "faction":
    #     chain = dict({"chain": {"current": 3,
    #                             "timeout": 158,
    #                             "modifier": 0.75,
    #                             "cooldown": 18
    #                             }
    #                 })
    #     return chain[sub] if sub is not None else chain

    try:
        r = requests.get("https://api.torn.com/{}/{}?selections={}&key={}".format(section, id, selections, key))
        r.raise_for_status()

        rjson = r.json()

        if "error" in rjson:  # standard api error
            err = rjson
        else:
            if sub is not None:
                if sub in rjson:
                    return rjson[sub]
                else:  # key not found
                    err = dict({"error": {"code": "", "error": "key not found... something went wrong..."}})
            else:
                return rjson

    except requests.exceptions.HTTPError as e:
        print("[FUNCTION apiCall] API HTTPError {}".format(e))
        err = dict({"error": {"code": r.status_code, "error": "{} #blameched".format(r.reason)}})

    return dict({"apiError": "API error code {}: {}.".format(err["error"]["code"], err["error"]["error"])})


def timestampToDate(timestamp):
    import datetime
    import pytz
    return datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)


# def apiCallAttacks( factionId, beginTS, endTS, key ):
#     import requests
#
#     chain = dict({})
#
#     currentBeginTS = beginTS
#     endTS = endTS+1 # add one to get last hit
#     feedAttacks = True
#     i = 1
#     while feedAttacks:
#         url = "https://api.torn.com/faction/{}?selections=attacks&key={}&from={}&to={}".format(factionId, key, currentBeginTS, endTS)
#         print("call number {}: {}".format(i, url), end='... ')
#         attacks = requests.get(url).json()["attacks"]
#         for k, v in attacks.items():
#             chain[k] = v
#             currentBeginTS = max(v["timestamp_ended"], currentBeginTS)
#         if(len(attacks)<1000):
#             feedAttacks = False
#         print("\tNumber of attacks: {}".format(len(attacks)))
#         i+=1
#
#     # pickle.dump(chain, open('chain-{}-{}.p'.format(beginTS, endTS), 'wb'))
#     return chain

def apiCallAttacks(factionId, beginTS, endTS, key, stopAfterNAttacks=False):
    import requests

    chain = dict({})

    beginTS = beginTS
    currentEndTS = endTS + 1  # add one to get last hit
    feedAttacks = True
    i = 1
    while feedAttacks:
        url = "https://api.torn.com/faction/{}?selections=attacks&key={}&from={}&to={}".format(factionId, key, beginTS, currentEndTS)
        print("[FUNCTION apiCallAttacks] call number {}: {}".format(i, url), end='... ')
        attacks = requests.get(url).json()["attacks"]
        if len(attacks):
            for k, v in attacks.items():
                chain[k] = v
                currentEndTS = min(v["timestamp_ended"], currentEndTS)
            if(len(attacks) < 1000):
                feedAttacks = False
            print("\tNumber of attacks: {}".format(len(attacks)))
            i += 1
        else:
            print("\tNumber of attacks: {}".format(len(attacks)))
            feedAttacks = False

        if stopAfterNAttacks is not False and len(chain) >= stopAfterNAttacks:
            print("[FUNCTION apiCallAttacks] Stop after {} attacks".format(stopAfterNAttacks))
            feedAttacks = False

    # pickle.dump(chain, open('chain-{}-{}.p'.format(beginTS, endTS), 'wb'))
    return chain


def toggleMessage(request, context, key):
    if key in request.session:
        context[key] = request.session[key]
        request.session[key] = False
    return context
