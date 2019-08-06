"""
ims URL Configuration
"""

from django.conf.urls import url, include
from django.shortcuts import redirect
from django.contrib import admin
from ui.utils import needs_setup


# Redirect Index to ui or run first setup
def index(request):
    if needs_setup():
        return redirect('ui:setup')
    else:
        return redirect('ui:overview')


urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^', include(('ui.urls', 'ui'), namespace='ui')),
    url(r'^', include(('account.urls', 'account'), namespace='account')),
    url(r'^admin/', admin.site.urls),
]
