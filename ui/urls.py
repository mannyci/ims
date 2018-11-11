from django.conf.urls import url

from .views import overview, SetupView, DashboardView
from core.views import HostCreate, HostList, HostDetail, HostDelete, EnvNew, EnvList, EnvUpdate, HostGroupNew

urlpatterns = [
    url(r'^setup', view=SetupView.as_view(), name='setup'),
    url(r'^overview', view=DashboardView.as_view(), name='overview'),
    url(r'^host/new$', view=HostCreate.as_view(), name='newhost'),
    url(r'^hosts$', view=HostList.as_view(), name='hosts'),
    url(r'^host/(?P<name>[\w-]+)$', view=HostDetail.as_view(), name='updatehost'),
    url(r'^host/delete/(?P<name>[\w-]+)$', view=HostDelete.as_view(), name='deletehost'),
    url(r'^env/new$', view=EnvNew.as_view(), name='newenv'),
    url(r'^envs$', view=EnvList.as_view(), name='envs'),
    url(r'^env/(?P<id>[\w-]+)$', view=EnvUpdate.as_view(), name='updateenv'),
    url(r'^hostgroup/new$', view=HostGroupNew.as_view(), name='newhostgroup'),
]
