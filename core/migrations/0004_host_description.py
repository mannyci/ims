# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-09 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20181109_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]