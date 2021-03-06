# Generated by Django 3.0.1 on 2020-02-14 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0027_guild_verifyfactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guild',
            name='allowedChannels',
        ),
        migrations.RemoveField(
            model_name='guild',
            name='repoModule',
        ),
        migrations.RemoveField(
            model_name='guild',
            name='repoName',
        ),
        migrations.RemoveField(
            model_name='guild',
            name='repoToken',
        ),
        migrations.RemoveField(
            model_name='guild',
            name='stockChannel',
        ),
        migrations.AddField(
            model_name='guild',
            name='apiChannels',
            field=models.CharField(blank=True, default='["*"]', max_length=64),
        ),
        migrations.AddField(
            model_name='guild',
            name='apiModule',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='guild',
            name='chainChannels',
            field=models.CharField(blank=True, default='["chain"]', max_length=64),
        ),
        migrations.AddField(
            model_name='guild',
            name='lootChannels',
            field=models.CharField(blank=True, default='["loot"]', max_length=64),
        ),
        migrations.AddField(
            model_name='guild',
            name='reviveChannels',
            field=models.CharField(blank=True, default='["revive"]', max_length=64),
        ),
        migrations.AddField(
            model_name='guild',
            name='stockChannels',
            field=models.CharField(blank=True, default='["stocks"]', max_length=64),
        ),
        migrations.AddField(
            model_name='guild',
            name='verifyChannels',
            field=models.CharField(blank=True, default='["verify-id"]', max_length=64),
        ),
        migrations.AlterField(
            model_name='guild',
            name='allowedRoles',
            field=models.CharField(blank=True, default='["*"]', max_length=64),
        ),
    ]
