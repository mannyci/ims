# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.urls import reverse
from .forms import LoginForm, SignupForm, ProfileForm
from account.models import Account


def LoginView(request):
    form = LoginForm()
    if request.GET:
        next_url = request.GET['next']

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('ui:overview')
        else:
            messages.warning(request, 'Invalid username or password.')
    return render(request, 'account/login.html', {'form': form, })


def SignupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! Please log in')
            return redirect('account:login')
    else:
        form = SignupForm()
    return render(request, 'account/register.html', {'form': form})


def LogoutView(request):
    logout(request)
    return redirect('index')


class ProfileView(UpdateView):
    model = Account
    form_class = ProfileForm
    template_name = 'profile/user.html'

    def get_object(self, **kwargs):
        self.username = self.kwargs.get("username")
        if self.username is None:
            raise Http404
        return get_object_or_404(Account, username__iexact=self.username)

    def get_success_url(self):
        messages.success(self.request, 'Profile updated successfully')
        return reverse('account:profile', kwargs={'username': self.username})
