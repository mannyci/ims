# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .utils import needs_env
from .models import Host, Environment
from .forms import NewHostForm, HostUpdateForm, NewEnvForm

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
	paginated_by = 2
	template_name = 'host/list.html'

class HostDetail(UpdateView):
	model = Host
	form_class = HostUpdateForm
	template_name = 'host/update.html'

	def get_object(self, **kwargs):
		self.name = self.kwargs.get("name")
		if self.name is None:
			raise Http404
		return get_object_or_404(Host, name__iexact=self.name)

	def get_success_url(self):
		messages.success(self.request, 'Host updated successfully')
		return reverse('ui:updatehost', kwargs={'name':self.name})

class HostDelete(DeleteView):
	model = Host
	template_name ='host/delete.html'
	def get_object(self, **kwargs):
		self.name = self.kwargs.get("name")
		if self.name is None:
			raise Http404
		return get_object_or_404(Host, name__iexact=self.name)

	def get_success_url(self):
		messages.success(self.request, 'Host deleted successfully')
		return reverse('ui:hosts')

class EnvNew(View):
	template = loader.get_template('env/new.html')

	def get(self, request):
		form = NewEnvForm()
		return HttpResponse(self.template.render({'form': form}, request))

	def post(self, request):
		form = NewEnvForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Env created successfully')
			return redirect('ui:envs')

		return HttpResponse(self.template.render({'form': form}, request), status=400)

class EnvList(ListView):
	template_name = 'env/list.html'
	model = Environment
