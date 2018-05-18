# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-16 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('madefor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='system.User')),
            ],
        ),
    ]
