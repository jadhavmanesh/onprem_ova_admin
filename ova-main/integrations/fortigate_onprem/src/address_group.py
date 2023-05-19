import json
from base_fortigate_action import BaseFortigateAction
import requests
import logging


class GetAddressGroupsAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        address_group_name = inputs["address_group_name"]
        
        api_url = 'api/v2/cmdb/firewall/addrgrp/' + address_group_name
        print(api_url)
        response = self.get(self.config,api_url)
        print(response)
        return {"results" : response}
        #api_url = f"api/v2/cmdb/firewall/addrgrp/"
        #results = self.get(self.config, api_url)
        #return {"results": results}

class UpdateAddressGroupAction(BaseFortigateAction):

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        group_name = inputs["group_name"]
        action = inputs["action"]
        address = inputs["address"]

        get_api_url = 'api/v2/cmdb/firewall/addrgrp/' + group_name
        print(get_api_url)
        get_response = self.get(self.config,get_api_url)
        print(get_response)

        api_url = 'api/v2/cmdb/firewall/addrgrp/' + group_name
        print(api_url)
        get_address_group_info = get_response
        print(get_address_group_info)
        get_address_group_info_output = get_address_group_info[0]
        new_address_group_members = []
        address_group_members_list = get_address_group_info_output.get('member')
        if action == 'add':
            address_group_members_list.append({'name': address})
            new_address_group_members = address_group_members_list
            print(new_address_group_members)
        if action == 'remove':
            for address_group_member in address_group_members_list:
                if address_group_member.get('name') != address:
                    new_address_group_members.append(address_group_member) 
                    print(new_address_group_members)
    
        payload = {
            'member': new_address_group_members
        }
        data = payload
        if not self.does_exist(self.config, api_url):
            logging.error(
                f'Requested address group "{group_name}" does not exist in Firewall config.'
            )
            raise Exception(f"{group_name} does not exist")
        response = self.put(self.config,api_url,data)
        print(response)
        return {"results" : response}
    
        #data = inputs["data"]
        #if isinstance(data, str):
            #data = json.loads(data)

        #api_url = "api/v2/cmdb/firewall/addrgrp/" + requests.utils.quote(
            #group_name, safe=""
        #)
        #if not self.does_exist(self.config, api_url):
            #logging.error(
                #f'Requested address group "{group_name}" does not exist in Firewall config.'
            #)
            #raise Exception(f"{group_name} does not exist")
        #result = self.put(self.config, api_url, data)
        #return result

class CreateAddressGroupAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self,  **inputs):
        group_name = inputs["group_name"]
        address = inputs["address"]
        
        api_url = "api/v2/cmdb/firewall/addrgrp/"
        print(api_url)
        payload = {
            'name': group_name, 'member': [{'name': address}]
        }
        data = payload
        if self.does_exist(self.config, api_url + group_name):
            raise Exception(f"{group_name} already exists")
        response = self.post(self.config,api_url,data)
        print(response)
        return {"results" : response}

        #data = inputs["data"]
        #if isinstance(data, str):
            #data = json.loads(data)

        #api_url = "api/v2/cmdb/firewall/addrgrp/"
        #if self.does_exist(self.config, api_url + group_name):
            #raise Exception(f"{group_name} already exists")
        #result = self.post(self.config, api_url, data)
        #return result


class DeleteAddressGroupAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        group_name = inputs["group_name"]
        api_url = 'api/v2/cmdb/firewall/addrgrp/' + group_name
        print(api_url)
        response = self.delete(self.config,api_url)
        print(response)
        return {"results" : response}

        #api_url = "api/v2/cmdb/firewall/addrgrp/" + group_name
        #result = self.delete(self.config, api_url)
        #return result