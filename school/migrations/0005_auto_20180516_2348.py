# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-16 23:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20180516_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student'),
        ),
    ]
