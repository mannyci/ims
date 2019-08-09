# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, Http404
from django.urls import reverse
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Count
from .utils import needs_env
from .models import Host, Environment, HostFacts
from .forms import NewHostForm, HostUpdateForm, NewEnvForm, EnvUpdateForm, NewHostGroupForm


class HostCreate(CreateView):
    model = Host
    form_class = NewHostForm
    template_name = 'host/new.html'

    def get(self, request):
        if needs_env():
            messages.warning(self.request, 'Please add an environment before.')
            return redirect('ui:newenv')
        return super(HostCreate, self).get(request)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.save()
        return super(HostCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Host addedd successfully')
        return reverse('ui:hosts')


class HostList(ListView):
    model = Host
    template_name = 'host/list.html'
    paginate_by = 2
    context_object_name = 'hosts'

    def get(self, request, *args, **kwagrs):
        env = request.GET.get('env')
        self.object_list = self.get_queryset().order_by('id')
        if env:
            self.object_list = self.object_list.filter(environment_id=env)
        context = self.get_context_data()
        return self.render_to_response(context)


class HostDetail(UpdateView):
    model = Host
    form_class = HostUpdateForm
    template_name = 'host/update.html'

    def get_object(self, **kwargs):
        self.id = self.kwargs.get("id")
        if self.id is None:
            raise Http404
        return get_object_or_404(Host, id__iexact=self.id)

    def get_success_url(self):
        messages.success(self.request, 'Host %s updated successfully' % self.object.name)
        return reverse('ui:hosts')


class HostDelete(DeleteView):
    model = Host
    template_name = 'host/delete.html'

    def get_object(self, **kwargs):
        self.name = self.kwargs.get("name")
        if self.name is None:
            raise Http404
        return get_object_or_404(Host, name__iexact=self.name)

    def get_success_url(self):
        messages.success(self.request, 'Host %s deleted successfully' % self.name)
        return reverse('ui:hosts')


class EnvNew(View):
    template = loader.get_template('env/new.html')

    def get(self, request):
        form = NewEnvForm()
        return HttpResponse(self.template.render({'form': form}, request))

    def post(self, request):
        form = NewEnvForm(request.POST)
        form.instance.added_by = self.request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Env created successfully')
            return redirect('ui:envs')

        return HttpResponse(self.template.render({'form': form}, request), status=400)


class EnvList(ListView):
    template_name = 'env/list.html'
    model = Environment
    queryset = Environment.objects.all().annotate(host_count=Count('host'))


class EnvUpdate(UpdateView):
    model = Environment
    form_class = EnvUpdateForm
    template_name = 'env/update.html'

    def get_object(self, **kwargs):
        self.id = self.kwargs.get("id")
        if self.id is None:
            raise Http404
        return get_object_or_404(Environment, id__iexact=self.id)

    def get_success_url(self):
        messages.success(self.request, 'Environment updated successfully')
        return reverse('ui:envs')


class HostGroupNew(View):
    """
    Create new hostgroup
    """
    template = loader.get_template('hostgroup/new.html')

    def get(self, request):
        form = NewHostGroupForm
        return HttpResponse(self.template.render({'form': form}, request))

    def post(self, request):
        form = NewHostGroupForm(request.POST)
        form.instance.added_by = self.request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Hostgroup created successfully')
            return redirect('ui:envs')

        return HttpResponse(self.template.render({'form': form}, request), status=400)

class HostFacts(ListView):
    template_name = 'host/tasks.html'
    model = HostFacts
    queryset = HostFacts.objects.all()
    context_object_name = 'tasks'
    paginate_by = 25
    ordering = ['-created_at']

    def get(self, request, *args, **kwagrs):
        host = request.GET.get('host')
        self.object_list = self.get_queryset()
        if host:
            self.object_list = self.object_list.filter(host=host)
        
        context = self.get_context_data()
        return self.render_to_response(context)