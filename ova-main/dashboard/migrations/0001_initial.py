# Generated by Django 4.0.3 on 2022-03-17 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SetupStatic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('gateway', models.CharField(blank=True, max_length=255, null=True)),
                ('subnet_mask', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OnpremModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sporact_api_key', models.CharField(blank=True, max_length=255, null=True)),
                ('device_prodcut', models.CharField(blank=True, choices=[('checkpoint', 'Checkpoint'), ('ciscoasa', 'Cisco ASA'), ('deepsecurity', 'Deep Security'), ('Ppalaalto', 'PalaAlto')], max_length=255, null=True)),
                ('api_key', models.CharField(blank=True, max_length=255, null=True)),
                ('hostname', models.CharField(blank=True, max_length=255, null=True)),
                ('port', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogCollectionModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deep_security', models.CharField(blank=True, choices=[('enable', 'Enable'), ('disable', 'disable')], max_length=255, null=True)),
                ('secret_key_sub_config', models.CharField(blank=True, max_length=255, null=True)),
                ('udp_port', models.IntegerField(blank=True, default=0, null=True)),
                ('sporact_webhook_url', models.CharField(blank=True, max_length=255, null=True)),
                ('sporact_webhook_key', models.CharField(blank=True, max_length=255, null=True)),
                ('apex_one', models.CharField(blank=True, choices=[('enable', 'Enable'), ('disable', 'disable')], max_length=255, null=True)),
                ('api_url', models.CharField(blank=True, max_length=255, null=True)),
                ('app_id', models.CharField(blank=True, max_length=255, null=True)),
                ('api_key', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
