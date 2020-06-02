# Generated by Django 3.0.4 on 2020-05-25 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0028_remove_abroadstocks_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifiedClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField(default=0)),
                ('author_name', models.CharField(default='Client version', max_length=16)),
                ('name', models.CharField(default='Client name', max_length=32)),
                ('version', models.CharField(default='Client version', max_length=16)),
                ('verified', models.BooleanField(default=True)),
            ],
        ),
    ]