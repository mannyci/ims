# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Host, Environment, Hostgroup

class HostResource(resources.ModelResource):

    class Meta:
        model = Host
        fields = ('id', 'name', 'description', 'ip', 'created_at', 'environment__name', 'added_by')

    def before_import_row(self, row, **kwargs):
        row['added_by'] = kwargs['user'].id
        # print(row['environment__name'].id)


class HostAdmin(ImportExportModelAdmin):
    resource_class = HostResource


admin.site.register(Host, HostAdmin)
# @admin.register(Host, Environment, Hostgroup)
