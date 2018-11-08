from django import forms
from django.forms.widgets import TextInput, Select
from django.forms import ValidationError
from .models import Host, Environment, Hostgroup


class NewHostForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Host name', 'autofocus': 'true'}))
    ip = forms.GenericIPAddressField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'IP'}))
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    hostgroup = forms.ModelChoiceField(required=False, queryset=Hostgroup.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Host
        fields = ['name', 'ip', 'environment']

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if Host.objects.filter(ip=ip, ip__iexact=ip).exists():
            host = Host.objects.get(ip=ip)
            raise ValidationError("Host %s with this ip already exists" % host)
        return ip


class HostUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    ip = forms.GenericIPAddressField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Host
        fields = ['name', 'ip', 'environment']


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
