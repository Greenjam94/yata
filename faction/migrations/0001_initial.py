# Generated by Django 3.0.1 on 2020-01-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0030_auto_20200118_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tId', models.IntegerField(default=0, unique=True)),
                ('name', models.CharField(default='MyFaction', max_length=32)),
                ('respect', models.IntegerField(default=0)),
                ('nKeys', models.IntegerField(default=0)),
                ('masterKeys', models.ManyToManyField(blank=True, to='player.Key')),
            ],
        ),
    ]
