# Generated by Django 3.2.16 on 2022-10-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.CharField(max_length=50, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='individual',
            name='idcard_no',
            field=models.CharField(blank=True, max_length=18, null=True, unique=True, verbose_name='身份编号'),
        ),
    ]
