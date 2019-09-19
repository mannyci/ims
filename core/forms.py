from django import forms
from django.forms.widgets import TextInput, Select, SelectMultiple
from django.forms import ValidationError
from django.utils.safestring import mark_safe
from .models import Host, Environment, Hostgroup
from network.models import Networks

from ipaddress import IPv4Network, IPv4Address


class NewHostForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Host name', 'autofocus': 'true'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    ip = forms.GenericIPAddressField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'IP'}))
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(required=False, queryset=Hostgroup.objects.all(), widget=SelectMultiple(attrs={'class': 'form-control'}), help_text='Select multiple groups')
    network = forms.ModelChoiceField(queryset=Networks.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Host
        fields = ['name', 'description', 'ip', 'environment', 'groups', 'network']

    def clean(self):
        network = self.cleaned_data['network']
        ip = self.cleaned_data['ip']
        name = self.cleaned_data['name']
        error_messages = []

        # Check if IP belongs to the network
        net = IPv4Network('{0}/{1}'.format(network.ip, network.prefix))
        if not IPv4Address(ip) in net:
            print(network.ip, network.prefix)
            self._errors["network"] = mark_safe(('IP {0} is not part of the network selected <strong>{1}</strong>.').format(ip, net))

        # Check if IP belongs to other host
        if Host.objects.filter(ip=ip, ip__iexact=ip).exists():
            host = Host.objects.get(ip=ip)
            self._errors["ip"] = mark_safe(('Host with this IP exists, click <a href="{0}">here</a>').format(host.id))

        # Check if host already exists
        if Host.objects.filter(name=name, name__iexact=name).exists():
            self._errors["name"] = mark_safe(('Host with this name exists.').format(name))

        return self.cleaned_data



class HostUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    ip = forms.GenericIPAddressField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(required=False, queryset=Hostgroup.objects.all(), widget=SelectMultiple(attrs={'class': 'form-control'}))
    network = forms.ModelChoiceField(queryset=Networks.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Host
        fields = ['name', 'description', 'ip', 'environment', 'groups', 'network']


class NewEnvForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Env name'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))

    class Meta:
        model = Environment
        fields = ['name', 'description']


class EnvUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Environment
        fields = ['name', 'description']

class NewHostGroupForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Hostgroup name'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))

    class Meta:
        model = Hostgroup
        fields = ['name', 'description']
