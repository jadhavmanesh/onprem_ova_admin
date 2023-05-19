from base_fortigate_action import BaseFortigateAction
import requests
import logging
import json


class GetFirewallAddressesAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        api_url = f"api/v2/cmdb/firewall/address/"
        results = self.get(self.config, api_url)
        print(json.dumps(results))
        result = results[0]
        return {"result" :result }