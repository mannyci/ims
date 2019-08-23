# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Account
admin.site.site_header = 'Admin'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Apps'
admin.site.register(Account, UserAdmin)
