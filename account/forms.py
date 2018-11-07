from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Account
from django.forms.widgets import PasswordInput, TextInput, EmailInput, CheckboxInput


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': 'true'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': 'true'}))
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and Account.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'A user with that email already exists.')
        return email


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, widget=TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control'}))
    is_admin = forms.BooleanField(required=False, widget=CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'is_admin']
