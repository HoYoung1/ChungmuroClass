# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-16 23:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='school.Student'),
        ),
    ]
