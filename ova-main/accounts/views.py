from urllib import request
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.views import View, generic
from .forms import LoginForm, WebSignUpForm
# from .models import User
from .utils import EmailService
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
User = get_user_model()

# class SignUp(generic.CreateView):
#     form_class = WebSignUpForm
#     success_url = reverse_lazy('email_sent')
#     template_name = 'accounts/signup.html'

#     def form_valid(self, form):
#         self.object = form.save()
#         email = self.object.email
#         self.request.session['user_email'] = email
#         host = self.request.get_host
#         user_uuid = self.object.user_id
#         self.object.is_active = False
#         self.object.save()
#         EmailService().send_email(email, host, user_uuid)
#         return super().form_valid(form)
class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("on_prem")
        return render(request,"registration/login.html")

    def post(self,request,*args,**kwargs):

            username   = request.POST.get("username")
            pass1    = request.POST.get("password1")
            user = authenticate(username=username,password=pass1)
            if user :      
                req_user = User.objects.get(id=user.id)
                if req_user:
                    login(request, user)      
                else:       
                        print("else statement is running")
                login(request, user)      
                return redirect("on_prem")
            if username == "admin" and pass1 == "admin" :
                print("else statement is running in the if statement")
                user_obj = User.objects.create(username="admin")
                return redirect("password_reset_on_login",id=user_obj.id)
                   

            else:
                messages.error(request,"Invalid credentials")
                return redirect('login')                  


class EmailSentView(generic.TemplateView):
    template_name = 'accounts/confirm-mail.html'

    def get(self, request, *args, **kwargs):
        email = request.session['user_email']
        return render(request, self.template_name, {"email": email})

class ActivateUser(generic.DetailView):
    template_name = 'accounts/activate_user.html'
    model = User

    def get_object(self, queryset=None):
        object = self.model.objects.get(user_id=self.kwargs.get("activate_user"))
        object.is_active = True
        object.save()
        return object

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password_reset_done")
        messages.error(request,"email does not exist")
    password_reset_form = PasswordResetForm()

    return render(request=request, template_name="registration/password_reset_form.html", context={"password_reset_form":password_reset_form})


class PasswordReset(View):

    def get(self,request,*args,**kwargs):

        return render(request,"dashboard/changePassword.html")

    def post(self,request,*args,**kwargs):

        pre_pass = request.POST.get("pre_password")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        id = self.kwargs.get("id")
        user = get_object_or_404(User,id=id)
        if user.check_password(pre_pass) and  password1 == password2 :
            user.set_password(password1)
            user.save()
            messages.success(request,"please login with new password!")
            return redirect("logout")
            
        else:
            messages.error(request,"passwords are not matching!")
            
            return redirect("change_password",id=id)
class PasswordResetOnLogin(View):

    def get(self,request,*args,**kwargs):

        return render(request,"dashboard/reset_password.html")

    def post(self,request,*args,**kwargs):

        pre_pass = request.POST.get("pre_password")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        id = self.kwargs.get("id")
        user = get_object_or_404(User,id=id)
        if password1 == password2 :
            user.set_password(password1)
            user.save()
            messages.success(request,"please login with new password!")
            return redirect("logout")
            
        else:
            messages.error(request,"passwords are not matching!")
            
            return redirect("change_password",id=id)

