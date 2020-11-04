# Generated by Django 3.1.2 on 2020-11-04 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0022_targetinfo_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.IntegerField(default=0)),
                ('name', models.CharField(default='target_name', max_length=16)),
                ('rank', models.CharField(default='rank', max_length=128)),
                ('level', models.IntegerField(default=0)),
                ('age', models.IntegerField(default=0)),
                ('defendslost', models.IntegerField(default=0)),
                ('attackswon', models.IntegerField(default=0)),
                ('last_action', models.IntegerField(default=0)),
                ('last_update', models.IntegerField(default=0)),
            ],
        ),
    ]
