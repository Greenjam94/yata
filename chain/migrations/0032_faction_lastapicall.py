# Generated by Django 2.0.5 on 2019-04-25 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0031_auto_20190425_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='faction',
            name='lastAPICall',
            field=models.IntegerField(default=0),
        ),
    ]
