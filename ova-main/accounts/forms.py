from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class WebSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

   
