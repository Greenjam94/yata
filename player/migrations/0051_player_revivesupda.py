# Generated by Django 3.0.4 on 2020-05-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0050_remove_player_awardsrank'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='revivesUpda',
            field=models.IntegerField(default=0),
        ),
    ]
