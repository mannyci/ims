# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Host, Environment, Hostgroup

admin.site.register(Host)
admin.site.register(Hostgroup)