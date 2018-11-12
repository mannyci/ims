# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, DetailView
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Count
from core.models import Host, Environment, Hostgroup


from .utils import needs_setup
from .forms import SetupForm


@login_required
def overview(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return redirect('account:login')


class DashboardView(DetailView):
    template = loader.get_template('index.html')

    def get(self, request):
        if needs_setup():
            return redirect('ui:setup')

        hosts = Host.objects.all().count()
        envs = Environment.objects.all().count()
        hostgroups = Hostgroup.objects.all().count()
        recentUpdatedHosts = Host.objects.all().order_by('-updated_at')[:5]
        environments = Environment.objects.all().annotate(host_count=Count('host'))
        groupdata = Hostgroup.objects.all().annotate(host_count=Count('host'))
        return HttpResponse(self.template.render({
            'hosts': hosts,
            'envs': envs,
            'hostgroups': hostgroups,
            'recentUpdatedHosts': recentUpdatedHosts,
            'environments': environments,
            'groupdata': groupdata
        }, request))


class SetupView(View):
    template = loader.get_template('setup/setup.html')

    def get(self, request):
        if not needs_setup():
            return redirect('account:login')

        form = SetupForm(initial={
            'username': 'admin',
        })

        return HttpResponse(self.template.render({'form': form}, request))

    def post(self, request):
        form = SetupForm(request.POST)
        if form.is_valid():
            get_user_model().objects.create_superuser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            messages.success(request, 'Admin setup complete.')
            return redirect('account:login')
        return HttpResponse(self.template.render({'form': form}, request), status=400)
