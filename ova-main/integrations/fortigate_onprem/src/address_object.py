import json
from base_fortigate_action import BaseFortigateAction
import requests
import logging

class CreateNewAddressObject(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        address_name = inputs["address_name"]
        address = inputs["address"]
        mask = inputs["mask"]
        fqdn = inputs["fqdn"]
        
        api_url = 'api/v2/cmdb/firewall/address/'
        print(api_url)
        if address:
            subnet = address + " " + mask
            payload = {
                'name': address_name,
                'subnet': subnet
            }
        elif fqdn:
            payload = {
                'name': address_name,
                "type": "fqdn",
                "fqdn": fqdn
            }
        data = payload
        print(data)
        response = self.post(self.config,api_url,data)
        print(response)
        return {"results" : response}
    
class DeleteAddressObject(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        address_name = inputs["address_name"]
        api_url = 'api/v2/cmdb/firewall/addrgrp/' + address_name
        print(api_url)
        response = self.delete(self.config,api_url)
        print(response)
        return {"results" : response}