# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-07 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professor', models.CharField(max_length=12)),
                ('class_name', models.CharField(max_length=32)),
                ('class_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('regDate', models.DateTimeField(auto_now_add=True)),
                ('students', models.ManyToManyField(blank=True, null=True, to='school.Student')),
            ],
        ),
    ]
