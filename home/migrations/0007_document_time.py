# Generated by Django 3.2.16 on 2022-10-18 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_document_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='time',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name=''),
        ),
    ]
