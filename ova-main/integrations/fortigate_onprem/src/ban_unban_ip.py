import json
from base_fortigate_action import BaseFortigateAction
import requests
import logging



class GetListOfBannedIps(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        api_url = 'api/v2/monitor/user/banned/select/'
        print(api_url)
        response = self.get(self.config,api_url)
        print(response)
        return {"result" :response }
        
class AddIpAddressToBannedList(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        ip_addresses_array = inputs["ip_addresses_array"]
        time_to_expire = inputs["time_to_expire"]

        api_url = 'api/v2/monitor/user/banned/add_users/'
        print(api_url)

        payload = {
            'ip_addresses': [ip_addresses_array],
            'expiry': int(time_to_expire)
        }
        data = payload
        response = self.post(self.config,api_url,data)
        print(response)
        return {"result" :response }
       

class ClearsListOfBannedAddresses(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        ip_addresses_array = inputs["ip_addresses_array"]
        api_url = 'api/v2/monitor/user/banned/clear_users/'
        print(api_url)
        payload = {
        'ip_addresses': [ip_addresses_array]
        }  
        data = payload
        response = self.post(self.config,api_url,data)
        print(response)
        return {"result" :response }
        



        