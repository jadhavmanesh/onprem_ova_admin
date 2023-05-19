import json
from base_PaloAlto_PanOS_action import BasePaloAltoAction
import requests
import logging


class ListSecurity(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vsys = inputs["vsys"]
        api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&vsys="+vsys
        results = self.get(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    
class CreateSecurity(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
                "entry": {
                    "@name": inputs["entry_policysecurityrules"],
                    "from": {
                    "member": [
                        inputs["entry_from"]
                    ]
                    },
                    "to": {
                    "member": [
                        inputs["entry_to"]
                    ]
                    },
                    "source": {
                    "member": [
                        inputs["entry_source"]
                    ]
                    },
                    "destination": {
                    "member": [
                        inputs["entry_destination"]
                    ]
                    },
                    "service": {
                    "member": [
                        inputs["entry_service"]
                    ]
                    },
                    "application": {
                    "member": [
                        inputs["entry_application"]
                    ]
                    },
                    "action": inputs["entry_action"]
                }
        })
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&name="+vm_name
        results = self.post(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    
class EditSecurity(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
                "entry": {
                    "@name": inputs["entry_policysecurityrules"],
                    "from": {
                    "member": [
                        inputs["entry_from"]
                    ]
                    },
                    "to": {
                    "member": [
                        inputs["entry_to"]
                    ]
                    },
                    "source": {
                    "member": [
                        inputs["entry_source"]
                    ]
                    },
                    "destination": {
                    "member": [
                        inputs["entry_destination"]
                    ]
                    },
                    "service": {
                    "member": [
                        inputs["entry_service"]
                    ]
                    },
                    "application": {
                    "member": [
                        inputs["entry_application"]
                    ]
                    },
                    "action": inputs["entry_action"]
                }
        })
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&name="+vm_name
        results = self.put(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    
class DeleteSecurity(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Policies/SecurityRules?location="+location+"&name="+vm_name
        results = self.delete(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    
class RenameSecurity(BasePaloAltoAction):
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
            api_url = f"/restapi/v10.2/Policies/SecurityRules:rename?location="+location+"&vsys="+vsys_name+"&name="+vm_name+"&newname="+newname
        else:
            api_url = f"/restapi/v10.2/Policies/SecurityRules:rename?location="+location+"&name="+vm_name+"&newname="+newname
        results = self.post(self.config, api_url,payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    
class MoveSecurity(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        where = inputs["where"]
        payload = {}
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Policies/SecurityRules:move?location="+location+"&vsys="+vsys_name+"&name="+vm_name+"&where="+where
        else:
            api_url = f"/restapi/v10.2/Policies/SecurityRules:move?location="+location+"&name="+vm_name+"&where="+where
        results = self.post(self.config, api_url,payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}