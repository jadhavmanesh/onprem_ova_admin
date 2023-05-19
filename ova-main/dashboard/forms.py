from django import forms
from .models import LogCollector, OnPremKey, OnpremModule, ProxySetting, SetupHost, SetupStatic, LogCollectionModule
from accounts.models import User


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UpdatUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }


class SetupStaticForm(forms.ModelForm):
    ip_address = forms.GenericIPAddressField()
    gateway = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Gateway Details"}))
    subnet_mask = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Subnet-mask Details"}))

    class Meta:
        model = SetupStatic
        fields = ['ip_address', 'gateway', 'subnet_mask']


class LogCollectionForm(forms.ModelForm):

    api_url = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter API Url"}), required=False)
    app_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter API Id"}), required=False)
    api_key = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter API Key"}), required=False)

    class Meta:
        model = LogCollectionModule
        fields = ['api_url', 'app_id', 'api_key']


class LogColletorForm(forms.ModelForm):

    udp_port = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': "input-field", 'placeholder': "Enter UDP Listener"}))
    sporact_webhook_url = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Webhook Url"}))
    sporact_webhook_key = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Webhook Key"}))

    class Meta:
        model = LogCollector
        fields = ['udp_port', 'sporact_webhook_url', 'sporact_webhook_key']


class DeepSecurityForm(forms.ModelForm):

    secret_key_sub_config = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Secret Key"}), required=False)

    class Meta:
        model = LogCollector
        fields = ['secret_key_sub_config',
                  'sporact_webhook_url', 'sporact_webhook_key']


class OnpremModuleForm(forms.ModelForm):

    product = (

        ('Checkpoint', "Checkpoint"),
        ('Cisco AsIa', "Cisco ASA"),
        ('Deep Security', "Deep Security"),
        ('PalaAlto', "PalaAlto"),
    )
    # deep_security = forms.ChoiceField()
    device_prodcut = forms.CharField(max_length=15, widget=forms.Select(
        choices=product, attrs={'class': "input-field"}))
    api_key = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter API Key"}))
    hostname = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Host Name"}))
    port = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': "input-field", 'placeholder': "Enter Port"}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter username"}))
    device_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "input-field", 'placeholder': "Enter password"}))
    sporact_webhook_url = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Sporact webhook url"}))

    class Meta:
        model = OnpremModule
        fields = ['device_prodcut', 'api_key',
                  'hostname', 'port', 'sporact_webhook_url']


class OnpremKeyForm(forms.ModelForm):

    sporact_api_key = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Sporact API Key"}))

    class Meta:
        model = OnPremKey
        fields = ['sporact_api_key']


class ProxyModleForm(forms.ModelForm):

    ip_address = forms.GenericIPAddressField()

    class Meta:
        model = ProxySetting
        fields = ['ip_address']


class SetupHostForm(forms.ModelForm):

    setup_hostname = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input-field", 'placeholder': "Enter Hostname"}))

    class Meta:
        model = SetupHost
        fields = ['setup_hostname']
