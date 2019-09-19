from django import forms
from django.forms.widgets import TextInput, NumberInput
from django.forms import ValidationError
from django.utils.safestring import mark_safe
from .models import Networks

class NewNetworkForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Netwroks Name', 'autofocus': 'true'}))
    description = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    ip = forms.GenericIPAddressField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'IP'}))
    prefix = forms.IntegerField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Network Prefix'}))

    
    class Meta:
        model = Networks
        fields = ['name', 'description', 'ip', 'prefix']

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if Networks.objects.filter(ip=ip, ip__iexact=ip).exists():
            network = Networks.objects.get(ip=ip)
            raise ValidationError(
                mark_safe(('Network with that ip already exists, click <a href="{0}">here</a>').format(network.id))
            )
        return ip

    def clean_prefix(self):
        prefix = self.cleaned_data['prefix']
        if (prefix < 8 or prefix > 30):
            raise ValidationError(
                mark_safe('Network prefix must be within range <strong>8-30</strong>.')
            )
        return prefix