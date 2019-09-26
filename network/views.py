from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404, Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse
from .models import Networks
from .forms import NewNetworkForm

class NetworkCreate(CreateView):
    model = Networks
    form_class = NewNetworkForm
    template_name = 'network/new.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.save()
        # host_status(host=form.instance.id) TODO Clelry
        return super(NetworkCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Netwrok addedd successfully')
        return reverse('ui:networks')

   
class NetworkList(ListView):
    model = Networks
    template_name = 'network/list.html'
    paginate_by = 2
    context_object_name = 'networks'

class NetworkUpdate(UpdateView):
    model = Networks
    form_class = NewNetworkForm
    template_name = 'network/update.html'
    context_object_name = 'network'

    def get_object(self, **kwargs):
        self.id = self.kwargs.get("id")
        if self.id is None:
            raise Http404
        return get_object_or_404(Networks, id__iexact=self.id)

    def get_success_url(self):
        messages.success(self.request, 'Netwrok updated successfully')
        return reverse('ui:networks')

    def form_invalid(self, form):
        messages.warning(self.request, 'Please correct below errors.', extra_tags='danger')
        return self.render_to_response(self.get_context_data(form=form))