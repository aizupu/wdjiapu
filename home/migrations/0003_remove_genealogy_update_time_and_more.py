# Generated by Django 4.1.2 on 2022-10-07 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genealogy',
            name='update_time',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='update_time',
        ),
        migrations.AlterField(
            model_name='genealogy',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间'),
        ),
    ]