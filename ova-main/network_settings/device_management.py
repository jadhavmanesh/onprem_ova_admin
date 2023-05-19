import logging
import re
import os
import traceback
from datetime import datetime
import datetime
from os.path import exists
import socket
import netifaces
from django.conf import settings

LOG = logging.getLogger(__name__)


class DeviceManagement(object):
    @staticmethod
    def view_proxy():
        LOG.info("inside the login")
        try:
            proxy_path = settings.PROXY_PATH
            proxy_list = []
            if exists(proxy_path):
                with open(proxy_path, "r") as file:
                    data_list = file.readlines()
                if len(data_list) > 0:
                    for each_proxy in data_list:
                        each_proxy = each_proxy.strip("\n")
                        each_proxy = re.sub("export http_proxy=", "", each_proxy)
                        proxy_list.append(each_proxy)
                    final_json = {
                        "status": "success",
                        "message": "successfully fetched the proxy details",
                        "proxy_list": proxy_list,
                    }
                else:
                    final_json = {"status": "success", "message": "proxy is not set!!"}
            else:
                final_json = {"status": "success", "message": "proxy is not set!!"}
            return final_json
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json

    @staticmethod
    def edit_proxy(input_data):
        LOG.info("inside the login")
        try:
            proxy_url_list = input_data["proxy_list"]
            delete_proxy_list = input_data["delete_proxy_list"]
            proxy_path = settings.PROXY_PATH
            proxy_list = []
            if not exists(proxy_path):
                os.system("touch " + proxy_path)
            with open(proxy_path, "r") as file:
                data_list = file.readlines()
            for each_proxy in proxy_url_list:
                each_proxy = "export http_proxy=" + str(each_proxy) + "\n"
                if each_proxy not in data_list:
                    proxy_list.append(each_proxy)
            data_list.extend(proxy_list)
            if len(delete_proxy_list) > 0:
                for delete_proxy in delete_proxy_list:
                    delete_proxy = "export http_proxy=" + str(delete_proxy) + "\n"
                    if delete_proxy in data_list:
                        data_list.remove(delete_proxy)
            with open(proxy_path, "w") as file:
                file.writelines(data_list)
            return {"status": "success", "message": "successfully configured the proxy"}
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json

    @staticmethod
    def view_network_details():
        LOG.info("inside the view_network_details")
        final_json = {}
        try:
            final_list = []
            network_list = netifaces.interfaces()
            gws = netifaces.gateways()
            gws = list(gws["default"][netifaces.AF_INET])[0]
            if len(network_list) > 0:
                for each_network in network_list:
                    new_json = {}
                    ip_address_details = netifaces.ifaddresses(each_network)
                    ip_address_list = ip_address_details[netifaces.AF_INET]
                    new_json["interface"] = each_network
                    new_json["ip_address"] = ip_address_list[0]["addr"]
                    new_json["netmask"] = ip_address_list[0]["netmask"]
                    new_json["gateway"] = gws
                    final_list.append(new_json)
            final_json["interface_details"] = final_list
            final_json["message"] = "successfully fetched the interface details "
            final_json["status"] = "success"
            return final_json
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json

    @staticmethod
    def get_interface_details():
        LOG.info("inside the get_interface_details")
        final_json = {}
        try:
            network_list = netifaces.interfaces()
            final_json["interface_details"] = network_list
            final_json["message"] = "successfully fetched the interface details "
            final_json["status"] = "success"
            return final_json
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json

    @staticmethod
    def view_host_name():
        LOG.info("inside the view_host_name")
        final_json = {}
        try:
            final_json["hostname"] = str(socket.gethostname())
            final_json["message"] = "successfully fetched the hostname "
            final_json["status"] = "success"
            return final_json
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json

    @staticmethod
    def edit_host_name(input_data):
        LOG.info("inside the edit_host_name")
        final_json = {}
        try:
            host_name = str(input_data["hostname"])
            host_name_path = "/etc/hostname"
            with open(host_name_path, "w") as file:
                file.write(host_name)
            os.system("hostname -b " + host_name)
            final_json["message"] = "successfully changed the hostname "
            final_json["status"] = "success"
            return final_json
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json

    @staticmethod
    def edit_network_details(input_data):
        LOG.info("inside the view_network_details")
        try:
            interface_type = input_data["interface_type"]
            interface = input_data["interface"]
            if interface_type == "static":
                try:
                    ip_address = input_data["ip_address"]
                    subnet_mask = input_data["subnet_mask"]
                    gateway = input_data["gateway"]
                    ts = datetime.datetime.now().strftime("%Y%m%d%h%M%S")
                    os.system(
                        "mv /etc/network/interfaces /etc/network/interfaces_" + ts
                    )
                    with open("static_interfaces_template.ini", "r") as file:
                        data = file.read()
                        data = (
                            data.replace("$int$", str(interface))
                            .replace("$ip$", ip_address)
                            .replace("$mask$", subnet_mask)
                            .replace("$gw$", gateway)
                        )
                    with open("interfaces", "w") as write_data:
                        write_data.write(data)
                    data_list = [
                        "mv interfaces /etc/network/interfaces\n",
                        "ifup " + str(interface) + "\n",
                        "service networking restart\n",
                        "ifup " + str(interface),
                    ]
                    with open("interfaces.sh", "w") as write_data:
                        write_data.writelines(data_list)
                    os.system("chmod 777 interfaces.sh")
                    os.system("./interfaces.sh")
                    return {"status": "Success"}
                except Exception as e:
                    return {"status": str(e)}
            elif interface_type == "auto":
                try:
                    ts = datetime.datetime.now().strftime("%Y%m%d%h%M%S")
                    os.system(
                        "mv /etc/network/interfaces /etc/network/interfaces_" + ts
                    )
                    with open("auto_interfaces_template.ini", "r") as file:
                        data = file.read()
                    with open("interfaces", "w") as write_data:
                        write_data.write(data)
                    data_list = [
                        "mv interfaces /etc/network/interfaces\n",
                        "ifup " + str(interface) + "\n",
                        "service networking restart\n",
                        "ifup " + str(interface),
                    ]
                    with open("interfaces.sh", "w") as write_data:
                        write_data.writelines(data_list)
                    os.system("chmod 777 interfaces.sh")
                    os.system("./interfaces.sh")
                    return {"status": "success"}
                except Exception as e:
                    return {"status": str(e)}
        except Exception as e:
            final_json = {"message": str(e), "status": "failed"}
            traceback.print_exc()
            LOG.error(str(traceback.format_exc()))
            LOG.error(e)
            return final_json
