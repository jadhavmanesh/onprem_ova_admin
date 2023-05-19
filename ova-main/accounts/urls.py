from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views  import PasswordResetView , PasswordResetConfirmView , PasswordResetCompleteView,PasswordResetDoneView
urlpatterns = [
    
    # path('sign-up/', views.SignUp.as_view(), name="sign_up"),
    path('', views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('email-sent/', views.EmailSentView.as_view(), name="email_sent"),
    path('<uuid:activate_user>/', views.ActivateUser.as_view(), name="confirm_user"),
    # Forget Reset
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset_request", views.password_reset_request, name="password_reset_request"),
    path("change_password/<int:id>/",views.PasswordReset.as_view(), name='change_password'),
    path("change_password/login/<int:id>/",views.PasswordResetOnLogin.as_view(), name='password_reset_on_login'),



]
