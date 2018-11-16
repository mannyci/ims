from django import forms
from django.forms.widgets import TextInput, Select, SelectMultiple
from django.forms import ValidationError
from django.utils.safestring import mark_safe
from .models import Host, Environment, Hostgroup


class NewHostForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Host name', 'autofocus': 'true'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    ip = forms.GenericIPAddressField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'IP'}))
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(required=False, queryset=Hostgroup.objects.all(), widget=SelectMultiple(attrs={'class': 'form-control'}), help_text='Select multiple groups')

    class Meta:
        model = Host
        fields = ['name', 'description', 'ip', 'environment', 'groups']

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if Host.objects.filter(ip=ip, ip__iexact=ip).exists():
            host = Host.objects.get(ip=ip)
            raise ValidationError(
                mark_safe(('Host {0} with that ip already exists, click <a href="{0}">here</a>').format(host))
            )
        return ip


class HostUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    ip = forms.GenericIPAddressField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(required=False, queryset=Hostgroup.objects.all(), widget=SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Host
        fields = ['name', 'description', 'ip', 'environment', 'groups']


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
