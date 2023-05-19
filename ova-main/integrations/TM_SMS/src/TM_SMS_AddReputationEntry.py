import requests
import json
from base_TM_SMS_action import BaseTMSMSAction
import logging


class Tm_SmsAction(BaseTMSMSAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        ip = inputs["ip"]
        api_url = "repEntries/add?ip={}".format(ip)
        results = self.get(self.config, api_url)
        return results
