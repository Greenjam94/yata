# Generated by Django 3.0.8 on 2020-09-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0021_auto_20200801_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='targetinfo',
            name='color',
            field=models.IntegerField(default=0),
        ),
    ]
