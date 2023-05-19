import json

from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from network_settings.device_management import DeviceManagement


@csrf_exempt
def proxy(request):
    if request.method == "GET":
        return JsonResponse(DeviceManagement.view_proxy())

    elif request.method == "PUT":
        request_data = json.loads(request.body)
        request_data.pop("delete_proxy_list", [])
        return JsonResponse({"status": "success", "message": "successfully configured"})
        return JsonResponse(DeviceManagement.edit_proxy(request_data))

    elif request.method == "DELETE":
        request_data = json.loads(request.body)
        request_data.pop("proxy_list", [])
        return JsonResponse({"status": "success", "message": "successfully configured"})
        return JsonResponse(DeviceManagement.edit_proxy(request_data))


@csrf_exempt
def hostname(request):
    if request.method == "GET":
        return JsonResponse(DeviceManagement.view_host_name())

    elif request.method == "PUT":
        request_data = json.loads(request.body)
        return JsonResponse({"status": "success", "message": "successfully configured"})
        return JsonResponse(DeviceManagement.edit_host_name(request_data))


@csrf_exempt
def network_details(request):
    if request.method == "GET":
        return JsonResponse(DeviceManagement.view_network_details())

    elif request.method == "PUT":
        request_data = json.loads(request.body)
        return JsonResponse({"status": "success", "message": "successfully configured"})
        return JsonResponse(DeviceManagement.edit_network_details(request_data))


@csrf_exempt
def interface(request):
    if request.method == "GET":
        return JsonResponse(DeviceManagement.get_interface_details())
