# Generated by Django 4.1.2 on 2022-11-04 08:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_file_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default=datetime.date(2022, 11, 4), verbose_name='日期')),
                ('count', models.IntegerField(default=0, verbose_name='网站访问次数')),
            ],
            options={
                'verbose_name': '网站日访问量统计',
                'verbose_name_plural': '网站日访问量统计',
            },
        ),
        migrations.CreateModel(
            name='UserIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30, verbose_name='IP 地址')),
                ('end_point', models.CharField(default='/', max_length=30, verbose_name='访问端点')),
                ('count', models.IntegerField(default=0, verbose_name='访问次数')),
            ],
            options={
                'verbose_name': '访问用户信息',
                'verbose_name_plural': '访问用户信息',
            },
        ),
        migrations.CreateModel(
            name='VisitNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='网站访问总次数')),
            ],
            options={
                'verbose_name': '网站访问总次数',
                'verbose_name_plural': '网站访问总次数',
            },
        ),
    ]