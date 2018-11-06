from django import forms
from django.forms.widgets import TextInput, CheckboxInput, Select
from .models import Host, Environment

class NewHostForm(forms.ModelForm):
	name = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Host name', 'autofocus': 'true'}))
	ip = forms.GenericIPAddressField(widget=TextInput(attrs={'class':'form-control','placeholder': 'IP'}))
	environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class':'form-control'}))
	class Meta:
		model = Host
		fields = ['name', 'ip', 'environment']

class HostUpdateForm(forms.ModelForm):
	name = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control'}))
	ip = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control'}))
	environment = forms.ModelChoiceField(queryset=Environment.objects.all(), widget=Select(attrs={'class':'form-control'}))
	class Meta:
		model = Host
		fields = ['name', 'ip', 'environment']

class NewEnvForm(forms.ModelForm):
	name = forms.CharField(required=True, widget=TextInput(attrs={'class':'form-control','placeholder': 'Env name'}))
	description = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control','placeholder': 'Description'}))
	class Meta:
		model = Environment
		fields = ['name', 'description']