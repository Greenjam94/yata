# Generated by Django 3.0.4 on 2020-05-04 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0043_auto_20200501_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainfull',
            name='perks_gym_book',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trainfull',
            name='perks_happy_book',
            field=models.IntegerField(default=0),
        ),
    ]
