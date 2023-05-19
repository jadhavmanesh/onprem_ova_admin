import json
import traceback
import threading
from flask import Blueprint, request, jsonify, send_from_directory, copy_current_request_context
from scripts.constants.app_constants import FlaskService, Api
from scripts.handlers.device_management import DeviceManagement
from scripts.logging import logger_util

LOG = logger_util.get_logger()

serv = Blueprint(FlaskService.service_api, __name__)


@serv.route(Api.login, methods=['POST'])
def login():
    try:
        if request.method == FlaskService.POST:
            try:
                input_data = json.loads(request.data)
                LOG.info("input_data: {}".format(input_data))
                response = DeviceManagement().user_login(input_data)
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify({"status": "failed", "message": str(e)})


@serv.route(Api.viewNetworkSettings, methods=['GET'])
def view_network_settings():
    try:
        if request.method == FlaskService.GET:
            try:
                response = DeviceManagement().view_network_details()
                print(response)
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify({"status": "failed", "message": str(e)})


@serv.route(Api.editNetworkSettings, methods=['POST'])
def edit_network_settings():
    try:
        if request.method == FlaskService.POST:
            try:
                input_data = json.loads(request.data)

                @copy_current_request_context
                def execute_command():
                    LOG.info("input_data: {}".format(input_data))
                    DeviceManagement().edit_network_details(input_data)

                threading.Thread(target=execute_command).start()
                return {"status": 'success', "message": "network configuration in-progress.."}
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify({"status": "failed", "message": str(e)})


@serv.route(Api.viewProxySettings, methods=['GET'])
def view_proxy_settings():
    try:
        if request.method == FlaskService.GET:
            try:
                response = DeviceManagement().view_proxy()
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify({"status": "failed", "message": str(e)})


@serv.route(Api.editProxySettings, methods=['POST'])
def edit_proxy_settings():
    try:
        if request.method == FlaskService.POST:
            try:
                input_data = json.loads(request.data)
                LOG.info("input_data: {}".format(input_data))
                response = DeviceManagement().edit_proxy(input_data)
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify({"status": "failed", "message": str(e)})


@serv.route(Api.getInterface, methods=['GET'])
def get_interface():
    try:
        if request.method == FlaskService.GET:
            try:
                response = DeviceManagement().get_interface_details()
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify


@serv.route(Api.viewHostName, methods=['GET'])
def get_hostname():
    try:
        if request.method == FlaskService.GET:
            try:
                response = DeviceManagement().view_host_name()
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify


@serv.route(Api.editHostName, methods=['POST'])
def edit_hostname():
    try:
        if request.method == FlaskService.POST:
            try:
                input_data = json.loads(request.data)
                LOG.info("input_data: {}".format(input_data))
                response = DeviceManagement().edit_host_name(input_data)
                return jsonify(response)
            except Exception as e:
                traceback.print_exc()
                LOG.exception(e)
                return jsonify({"status": "failed", "message": str(e)})
    except Exception as e:
        traceback.print_exc()
        LOG.exception(e)
        return jsonify
