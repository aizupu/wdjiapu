# Generated by Django 4.1.2 on 2022-11-09 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_daynumber_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='userip',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 9, 15, 9, 52, 30059), verbose_name='最近一次访问'),
        ),
    ]