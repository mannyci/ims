from django.conf.urls import url
from .views import LoginView, LogoutView, SignupView, ProfileView

urlpatterns = [
    url(r'^login$', view=LoginView, name='login'),
    url(r'^register$', view=SignupView, name='register'),
    url(r'^logout$', view=LogoutView, name='logout'),
    url(r'^profile/(?P<username>[\w-]+)$', view=ProfileView.as_view(), name='profile'),
]
