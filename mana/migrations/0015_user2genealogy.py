# Generated by Django 4.1.2 on 2022-11-10 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_userip_last_visit'),
        ('mana', '0014_userinfo_is_del'),
    ]

    operations = [
        migrations.CreateModel(
            name='User2Genealogy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.CharField(default='0', max_length=32, verbose_name='是否公开')),
                ('gene', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.genealogy')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mana.userinfo')),
            ],
        ),
    ]
