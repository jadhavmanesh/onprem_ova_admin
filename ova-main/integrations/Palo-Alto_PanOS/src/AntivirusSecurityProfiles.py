import json
from base_PaloAlto_PanOS_action import BasePaloAltoAction
import requests
import logging


class GetAntivirusSecurityProfilesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vsys = inputs["vsys"]
        api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&vsys="+vsys
        results = self.get(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class CreateAntivirusSecurityProfilesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_name"],
                "description": inputs["entry_description"],
                "packet-capture": inputs["entry_packet-capture"]
            }
        })
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&name="+vm_name
        results = self.post(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class EditAntivirusSecurityProfilesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_name"],
                "description": inputs["entry_description"],
                "packet-capture": inputs["entry_packet-capture"]
            }
        })
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&name="+vm_name
        results = self.put(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class DeleteAntivirusSecurityProfilesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles?location="+location+"&name="+vm_name
        results = self.delete(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}


class RenameAntivirusSecurityProfilesAction(BasePaloAltoAction):
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
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles:rename?location="+location+"&vsys="+vsys_name+"&name="+vm_name+"&newname="+newname
        else:
            api_url = f"/restapi/v10.2/Objects/AntivirusSecurityProfiles:rename?location="+location+"&name="+vm_name+"&newname="+newname
        results = self.post(self.config,api_url,payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    

