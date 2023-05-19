from base_dsm_action import BaseDsmAction
import requests
import json
import logging

class AppControlEventAction(BaseDsmAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self,  **inputs):
        api_url = f"events/appcontrol"
        results = self.get(self.config, api_url)
        return {"results": results}


