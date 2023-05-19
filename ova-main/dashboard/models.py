from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class SetupStatic(models.Model):
    class Meta:
        verbose_name = 'Setup Static'
        verbose_name_plural = 'Setup Static'
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    ip_address = models.CharField(max_length=255,blank=True,null=True)
    gateway = models.CharField(max_length=255,blank=True,null=True)
    subnet_mask = models.CharField(max_length=255,blank=True,null=True)

# class Proxy(models.Model):

class LogCollector(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    udp_port = models.IntegerField(default=0,blank=True,null=True)
    sporact_webhook_url = models.CharField(max_length=255,blank=True,null=True)
    sporact_webhook_key = models.CharField(max_length=255,blank=True,null=True)

class DeepSecurity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    secret_key_sub_config = models.CharField(max_length=255,blank=True,null=True)

class LogCollectionModule(models.Model):
    class Meta:
        verbose_name = 'Log Collection'
        verbose_name_plural = 'Log Collection'
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    api_url = models.CharField(max_length=255,blank=True,null=True)    
    app_id = models.CharField(max_length=255,blank=True,null=True) 
    api_key = models.CharField(max_length=255,blank=True,null=True) 

class OnPremKey(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    sporact_api_key = models.CharField(max_length=255,blank=True,null=True)


class OnpremModule(models.Model):
    class Meta:
        verbose_name = 'Onprem Module'
        verbose_name_plural = 'Onprem Module'
        
    product = (
    
        ('Checkpoint',"Checkpoint"),
         ('Cisco AsIa',"Cisco ASA"),
          ('Deep Security',"Deep Security"),
           ('PalaAlto',"PalaAlto"),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    device_prodcut = models.CharField(max_length=255,choices=product,blank=True,null=True)
    api_key = models.CharField(max_length=255,blank=True,null=True)
    hostname = models.CharField(max_length=255,blank=True,null=True)
    port = models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=255,blank=True,null=True)
    device_password = models.CharField(max_length=255,blank=True,null=True) 
    sporact_webhook_url = models.CharField(max_length=255,blank=True,null=True) 
    
class ProxySetting(models.Model):
    class Meta:
        verbose_name = 'Proxy'
        verbose_name_plural = 'Proxy'
        
    product = (
    
        ('checkpoint',"Checkpoint"),
         ('ciscoasa',"Cisco ASA"),
          ('deepsecurity',"Deep Security"),
           ('Ppalaalto',"PalaAlto"),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    ip_address = models.CharField(max_length=255,blank=True,null=True)
    
    
    
class SetupHost(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    setup_hostname = models.CharField(max_length=255,blank=True,null=True)






