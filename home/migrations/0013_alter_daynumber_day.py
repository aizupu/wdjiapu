# Generated by Django 4.1.2 on 2022-11-04 08:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_daynumber_userip_visitnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daynumber',
            name='day',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日期'),
        ),
    ]
