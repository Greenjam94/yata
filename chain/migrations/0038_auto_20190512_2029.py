# Generated by Django 2.0.5 on 2019-05-12 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0037_auto_20190512_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='member',
        ),
        migrations.RemoveField(
            model_name='faction',
            name='crontab',
        ),
        migrations.AddField(
            model_name='crontab',
            name='faction',
            field=models.ManyToManyField(to='chain.Faction'),
        ),
        migrations.DeleteModel(
            name='Target',
        ),
    ]