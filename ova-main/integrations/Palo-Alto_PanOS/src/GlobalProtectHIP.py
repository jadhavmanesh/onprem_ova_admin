import json

from base_PaloAlto_PanOS_action import BasePaloAltoAction
import requests
import logging


class GetHIPObjectAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vsys = inputs["vsys"]
        api_url = f"/restapi/v10.2/Objects/GlobalProtectHIPObjects?location="+location+"&vsys="+vsys
        results = self.get(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class CreateHIPObjectAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_hipname"],
            }
        })
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/GlobalProtectHIPObjects?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/GlobalProtectHIPObjects?location="+location+"&name="+vm_name
        results = self.post(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class EditHIPObjectAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_hipname"],
            }
        })
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/GlobalProtectHIPObjects?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/GlobalProtectHIPObjects?location="+location+"&name="+vm_name
        results = self.put(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}


