import json
from base_PaloAlto_PanOS_action import BasePaloAltoAction
import requests
import logging


class GetApplicationAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vsys = inputs["vsys"]
        api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&vsys="+vsys
        results = self.get(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class CreateApplicationAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_applicationname"],
                "category": inputs["entry_category"],
                "subcategory" : inputs["entry_subcategory"],
                "technology" : inputs["entry_technology"],
                "risk" : inputs["entry_risk"]
            }
        })
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&name="+vm_name
        results = self.post(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class EditApplicationAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_applicationname"],
                "category": inputs["entry_category"],
                "subcategory" : inputs["entry_subcategory"],
                "technology" : inputs["entry_technology"],
                "risk" : inputs["entry_risk"]
            }
        })
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&name="+vm_name
        results = self.put(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class DeleteApplicationAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/Applications?location="+location+"&name="+vm_name
        results = self.delete(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class RenameApplicationAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        newname = inputs["newname"]
        payload = {}
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/Applications:rename?location="+location+"&vsys="+vsys_name+"&name="+vm_name+"&newname="+newname
        else:
            api_url = f"/restapi/v10.2/Objects/Applications:rename?location="+location+"&name="+vm_name+"&newname="+newname
            
        results = self.post(self.config,api_url,payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}



