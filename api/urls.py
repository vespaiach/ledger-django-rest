from django.urls import path

from . import views


urlpatterns = [
    path('token', views.token, name='exchange_for_token'),
    path('revoke', views.revoke, name='revoke_token'),
]
