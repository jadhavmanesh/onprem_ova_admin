import json
from base_fortigate_action import BaseFortigateAction
import requests
import logging


class GetFirewallServiceAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        service_name = inputs["service_name"]
        api_url = 'api/v2/cmdb/firewall.service/custom/' + service_name
        print(api_url)
        response = self.get(self.config,api_url)
        print(response)
        return {"result" : response }

class CreateFirewallServiceAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        service_name = inputs["service_name"]
        tcp_range = inputs["tcp_range"]
        udp_range = inputs["udp_range"]
        
        api_url = "api/v2/cmdb/firewall.service/custom/"
        print(api_url)
        payload = {
            'name': service_name,
            'tcp-portrange': tcp_range,
            'udp-portrange': udp_range
        }
        data = payload
        if self.does_exist(self.config, api_url + service_name):
            raise Exception(f"{service_name} already exists")
        
        response = self.post(self.config,api_url,data)
        print(response)
        return {"result" : response }

