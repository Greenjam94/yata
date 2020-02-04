# Generated by Django 2.0.7 on 2020-02-04 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faction', '0037_factiontree'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upgrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tId', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('branchorder', models.IntegerField(default=0)),
                ('branchmultiplier', models.IntegerField(default=0)),
                ('unlocked', models.CharField(default='branch', max_length=32)),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faction.Faction')),
            ],
        ),
        migrations.RenameField(
            model_name='factiontree',
            old_name='lvl',
            new_name='level',
        ),
    ]
