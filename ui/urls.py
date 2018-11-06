from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import overview, SetupView
from core.views import HostCreate, HostList, HostDetail, HostDelete, EnvNew, EnvList

urlpatterns = [
    url(r'^setup',view=SetupView.as_view(), name='setup'),
    url(r'^overview',view=overview, name='overview'),
    url(r'^host/new$',view=HostCreate.as_view(), name='newhost'),
    url(r'^hosts$',view=HostList.as_view(), name='hosts'),
    url(r'^host/(?P<name>[\w-]+)$',view=HostDetail.as_view(), name='updatehost'),
    url(r'^host/delete/(?P<name>[\w-]+)$',view=HostDelete.as_view(), name='deletehost'),
    url(r'^env/new$',view=EnvNew.as_view(), name='newenv'),
    url(r'^envs$',view=EnvList.as_view(), name='envs'),
]