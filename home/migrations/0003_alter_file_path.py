# Generated by Django 3.2.16 on 2022-10-14 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.CharField(max_length=100, verbose_name=''),
        ),
    ]