# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-19 22:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='active',
        ),
    ]