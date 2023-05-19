from django.urls import path
from . import views

urlpatterns = [

    path('', views.OnpremModuleView.as_view(), name="on_prem"),
    path('users/', views.DisplayUserView.as_view(), name="users"),
    path('update-user/<int:pk>/', views.UpdateUserView.as_view(), name="update_user"),
    path('user/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
    path('setup/static/', views.SetupStaticView.as_view(), name='setup_static'),
    path('log/collection/', views.LogCollectionView.as_view(), name="log_collection"),
    path('on/prem/<int:pk>/delete/', views.DeleteOnpremModuleView.as_view(), name='on_prem_delete'),
    path('on/prem/<int:pk>/', views.UpdateOnpremModuleView.as_view(), name="update_on_prem"),
    path('proxy/setting/', views.ProxyView.as_view(), name="proxy"),
    path('add/user/', views.AddUserView.as_view(), name="add_user"),
    path('on/prem/key/', views.OnpremKeyView.as_view(), name="on_prem_key"),
    path('log/collector/', views.LogCollectorView.as_view(), name="log_collector"),
    path('deep/security/', views.DeepSecurityView.as_view(), name="deep_security"),
    path('setup/host/', views.SetupHostname.as_view(), name="setup_host"),

]