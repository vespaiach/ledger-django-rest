from django.urls import path

from . import views


urlpatterns = [
    path('get_token', views.token, name='get_token'),
    path('revoke_token', views.revoke, name='revoke_token'),
]
