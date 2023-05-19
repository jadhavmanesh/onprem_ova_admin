from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import User
from django.urls import reverse
from dashboard.forms import AddUserForm, DeepSecurityForm, LogCollectionForm, LogColletorForm, OnpremKeyForm, \
    OnpremModuleForm, ProxyModleForm, SetupHostForm, SetupStaticForm, UpdatUserForm
# from dashboard.ip_config_file import ip_Address
from dashboard.models import DeepSecurity, LogCollectionModule, LogCollector, OnPremKey, OnpremModule, ProxySetting, \
    SetupHost, SetupStatic
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.
from django.template.loader import render_to_string
from django.http import JsonResponse


class AddUserView(LoginRequiredMixin, generic.CreateView):
    template_name = 'dashboard/add_user.html'
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def get_success_url(self):
        return reverse_lazy("users")


class DisplayUserView(LoginRequiredMixin, generic.ListView):
    template_name = 'updated_dashboard/users.html'
    model = User

    def get_queryset(self):
        return self.model.objects.all().exclude(id=self.request.user.id)


class UpdateUserView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'dashboard/update_user.html'
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def get_success_url(self):
        return reverse_lazy("users")


class DeleteUserView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'dashboard/add_user.html'
    model = User

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('users')


# ! Setup static/ DHCP


class SetupStaticView(LoginRequiredMixin, generic.CreateView):
    template_name = 'updated_dashboard/setup_static.html'
    model = SetupStatic
    form_class = SetupStaticForm

    def get(self, request, **kwargs):
        setup_static = SetupStatic.objects.filter(user=request.user).first()
        context = {
            "object_list": setup_static,
            "form": SetupStaticForm(instance=setup_static)
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        setup_static = SetupStatic.objects.filter(user=request.user).first()
        form = SetupStaticForm(instance=setup_static, data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Request submitted Successfully!")
            return redirect("setup_static")
        messages.error(request, "something went wrong!")
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('home')


# ! Proxy Settings


class ProxyView(LoginRequiredMixin, generic.CreateView):
    template_name = 'dashboard/proxy.html'
    model = ProxySetting
    form_class = ProxyModleForm

    def get(self, request, **kwargs):
        # proxy = "192.168.18.30"
        # port = "0000"
        # ip_Address(proxy,port)
        onprem_module = ProxySetting.objects.filter(user=request.user).first()
        context = {
            "form": ProxyModleForm(instance=onprem_module)
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        onprem_module = ProxySetting.objects.filter(user=request.user).first()
        form = ProxyModleForm(instance=onprem_module, data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Request submitted Successfully!")
            return redirect("proxy")
        messages.error(request, "something went wrong!")
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('home')


# ! Log collection


class LogCollectionView(LoginRequiredMixin, generic.CreateView):
    template_name = 'updated_dashboard/log_collection.html'
    model = LogCollectionModule

    def get(self, request, **kwargs):

        log_collection = LogCollectionModule.objects.filter(
            user=request.user).first()
        log_collection_form = LogCollectionForm(instance=log_collection)
        log_collector = LogCollector.objects.filter(user=request.user).first()
        log_collector_form = LogColletorForm(instance=log_collector)
        deep_security = DeepSecurity.objects.filter(user=request.user).first()
        deep_security_form = DeepSecurityForm(instance=deep_security)
        context = {
            "object_list": log_collection,
            "log_collection_form": log_collection_form,
            "log_collector_form": log_collector_form,
            "deep_security_form": deep_security_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        if 'udp_port' in request.POST:
            obj, created = LogCollector.objects.get_or_create(
                user=request.user)
            obj.udp_port = request.POST.get("udp_port")
            obj.sporact_webhook_url = request.POST.get("sporact_webhook_url")
            obj.sporact_webhook_key = request.POST.get("sporact_webhook_key")
            obj.save()
        if 'secret_key_sub_config' in request.POST:
            obj, created = DeepSecurity.objects.get_or_create(
                user=request.user)
            obj.secret_key_sub_config = request.POST.get(
                "secret_key_sub_config")
            obj.save()

        if 'api_url' in request.POST:
            print("in the SECRET KEY", request.POST)
            obj, created = LogCollectionModule.objects.get_or_create(
                user=request.user)
            obj.api_url = request.POST.get("api_url")
            obj.app_id = request.POST.get("app_id")
            obj.api_key = request.POST.get("api_key")
            obj.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('log_collection')


class LogCollectorView(LoginRequiredMixin, generic.CreateView):
    template_name = 'dashboard/log_collection.html'
    model = LogCollector

    def get(self, request, **kwargs):
        log_collection = LogCollectionModule.objects.filter(
            user=request.user).first()
        log_collection_form = LogCollectionForm(instance=log_collection)
        log_collector = LogCollector.objects.filter(user=request.user).first()
        log_collector_form = LogColletorForm(instance=log_collector)
        deep_security = DeepSecurity.objects.filter(user=request.user).first()
        deep_security_form = DeepSecurityForm(instance=deep_security)
        context = {
            "object_list": log_collection,
            "log_collection_form": log_collection_form,
            "log_collector_form": log_collector_form,
            "deep_security_form": deep_security_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        log_collector = LogCollector.objects.filter(user=request.user).first()
        form = LogColletorForm(instance=log_collector, data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(self.get_success_url())

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('log_collection')


class DeepSecurityView(LoginRequiredMixin, generic.CreateView):
    template_name = 'dashboard/log_collection.html'
    model = DeepSecurity

    def get(self, request, **kwargs):
        log_collection = LogCollectionModule.objects.filter(
            user=request.user).first()
        log_collection_form = LogCollectionForm(instance=log_collection)
        log_collector = LogCollector.objects.filter(user=request.user).first()
        log_collector_form = LogColletorForm(instance=log_collector)
        deep_security = DeepSecurity.objects.filter(user=request.user).first()
        deep_security_form = DeepSecurityForm(instance=deep_security)
        context = {
            "object_list": log_collection,
            "log_collection_form": log_collection_form,
            "log_collector_form": log_collector_form,
            "deep_security_form": deep_security_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        deep_security_obj = DeepSecurity.objects.filter(
            user=request.user).first()
        form = DeepSecurityForm(instance=deep_security_obj, data=request.POST)
        print("ERRORS:", form.errors)
        print("post:", request.POST.get("secret_key_sub_config"))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.secret_key_sub_config = request.POST.get(
                "secret_key_sub_config")
            obj.save()
            return redirect(self.get_success_url())

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('log_collection')


# ! Onprem Ops Module
class OnpremModuleView(LoginRequiredMixin, generic.CreateView):
    template_name = 'updated_dashboard/on_prem_module.html'
    model = OnpremModule
    form_class = OnpremModuleForm

    def get(self, request, **kwargs):
        onprem_module = OnpremModule.objects.filter(
            user=request.user).order_by("-id")
        on_prem_key = OnPremKey.objects.filter(user=request.user).first()
        form = OnpremKeyForm(instance=on_prem_key)
        context = {
            "object_list": onprem_module,
            "form": form,
            "onprem_form": OnpremModuleForm
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        form = OnpremModuleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.username = form.cleaned_data['username']
            obj.device_password = make_password(
                form.cleaned_data['device_password'])
            obj.save()
            messages.success(request, "Request submitted Successfully!")
            return redirect(self.get_success_url())
        else:
            messages.error(request, "something went wrong!")
            return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('on_prem')


class OnpremKeyView(LoginRequiredMixin, generic.CreateView):
    template_name = 'dashboard/on_prem_module.html'
    model = OnPremKey

    # form_class = LogCollectionForm

    def get(self, request, **kwargs):
        on_prem_key = OnPremKey.objects.filter(user=request.user).first()
        form = OnpremKeyForm(instance=on_prem_key)
        onprem_module = OnpremModule.objects.filter(
            user=request.user).order_by("-id")

        context = {
            "object_list": onprem_module,
            "form": form,
            "onprem_form": OnpremModuleForm
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        log_collection = OnPremKey.objects.filter(user=request.user).first()
        form = OnpremKeyForm(instance=log_collection, data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.sporact_api_key = form.cleaned_data['sporact_api_key']
            obj.save()
            return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('on_prem')


class DeleteOnpremModuleView(generic.DeleteView):
    template_name = 'dashboard/on_prem_module.html'
    model = OnpremModule

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('on_prem')


class UpdateOnpremModuleView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'updated_dashboard/edit_model.html'
    model = OnpremModule
    fields = ['device_prodcut', 'username', 'device_password',
              'api_key', "hostname", 'port', 'sporact_webhook_url']

    def get(self, request, **kwargs):
        setup_static = OnpremModule.objects.filter(
            user=request.user).order_by("-id")
        obj = OnpremModule.objects.get(id=self.kwargs.get("pk"))
        context = {
            "object_list": setup_static,
            'onprem_form': OnpremModuleForm(instance=obj)
        }
        data = dict()
        data['html_page'] = render_to_string(self.template_name, context, request=request)

        return JsonResponse(data=data, status=200, safe=False)

    def get_success_url(self):
        return reverse('on_prem')


class SetupHostname(LoginRequiredMixin, generic.CreateView):
    template_name = 'updated_dashboard/setup_hostname.html'
    model = SetupHost

    def get(self, request, **kwargs):
        host_obj = SetupHost.objects.filter(user=request.user).first()
        form = SetupHostForm(instance=host_obj)
        context = {
            "form": form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        host_obj = SetupHost.objects.filter(user=request.user).first()
        form = SetupHostForm(instance=host_obj, data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('setup_host')
