# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .utils import needs_setup
from .forms import SetupForm


@login_required
def overview(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return redirect('account:login')


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