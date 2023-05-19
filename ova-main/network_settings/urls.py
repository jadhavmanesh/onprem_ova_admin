from django.urls import path
from . import views

urlpatterns = [
    path('proxy/', views.proxy, name="proxy"),
    path('hostname/', views.hostname, name="hostname"),
    path('network_details/', views.network_details, name="network_details"),
    path('interface/', views.interface, name="interface"),
]