# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-06 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=12)),
                ('img_url', models.CharField(max_length=64)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
