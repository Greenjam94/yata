# Generated by Django 3.0.1 on 2020-01-04 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0087_auto_20200104_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='revivecontract',
            name='first',
            field=models.IntegerField(default=0),
        ),
    ]
