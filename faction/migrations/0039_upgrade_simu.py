# Generated by Django 2.0.7 on 2020-02-04 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faction', '0038_auto_20200204_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='upgrade',
            name='simu',
            field=models.BooleanField(default=False),
        ),
    ]
