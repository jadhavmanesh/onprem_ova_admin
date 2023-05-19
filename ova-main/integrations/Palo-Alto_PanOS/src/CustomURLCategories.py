import json
from base_PaloAlto_PanOS_action import BasePaloAltoAction
import requests
import logging


class GetCustomURLCategoriesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vsys = inputs["vsys"]
        api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&vsys="+vsys
        results = self.get(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class CreateCustomURLCategoriesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_urlname"],
                "type": "URL List"
            }
        })
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&name="+vm_name
        results = self.post(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class EditCustomURLCategoriesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        payload = json.dumps({
            "entry": {
                "@name": inputs["entry_urlname"],
                "type": "URL List"
            }
        })
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&name="+vm_name
        results = self.put(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}
    

class DeleteCustomURLCategoriesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&vsys="+vsys_name+"&name="+vm_name
        else:
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories?location="+location+"&name="+vm_name
        results = self.delete(self.config, api_url)
        results = json.dumps(results)
        print(results)
        return {"results": results}

class RenameCustomURLCategoriesAction(BasePaloAltoAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        location = inputs["location"]
        vm_name = inputs["name"]
        newname = inputs["newname"]
        payload = {}
        print(payload)
        if location == "vsys":
            vsys_name = inputs["vsys"]
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories:rename?location="+location+"&vsys="+vsys_name+"&name="+vm_name+"&newname="+newname
        else:
            api_url = f"/restapi/v10.2/Objects/CustomURLCategories:rename?location="+location+"&name="+vm_name+"&newname="+newname
        results = self.put(self.config, api_url , payload)
        results = json.dumps(results)
        print(results)
        return {"results": results}


