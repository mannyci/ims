from django import forms
from account.models import Account
from django.forms.widgets import PasswordInput, TextInput, EmailInput


class SetupForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': 'true'}))
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'password']
