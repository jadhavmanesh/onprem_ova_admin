import json
from base_fortigate_action import BaseFortigateAction
import requests
import logging

class GetServiceGroupsAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        name = inputs["name"]
        get_api_url = 'api/v2/cmdb/firewall.service/group/' + name
        print(get_api_url)
        response = self.get(self.config,get_api_url)
        print(response)
        return {"results" : response}
        
class UpdateServiceGroupAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        group_name = inputs["group_name"]
        action = inputs["action"]
        service_name = inputs["service_name"]

        get_api_url = 'api/v2/cmdb/firewall.service/group/' + group_name
        print(get_api_url)
        get_response = self.get(self.config,get_api_url)
        print(get_response)
        
        api_url = 'api/v2/cmdb/firewall.service/group/' + group_name
        print(api_url)

        get_service_group_info = get_response
        print(get_service_group_info)
        get_service_group_info_output = get_service_group_info[0]
      # type: list
        new_service_group_members = []
        service_group_members_list = get_service_group_info_output.get('member')
        if action == 'add':
            service_group_members_list.append({'name': service_name})
            new_service_group_members = service_group_members_list
            print(new_service_group_members)
        if action == 'remove':
            for service_group_member in service_group_members_list:
                if service_group_member.get('name') != service_name:
                    new_service_group_members.append(service_group_member) 
                    print(new_service_group_members)
        payload = {
            'member': new_service_group_members
        }
        data = payload
    
        if not self.does_exist(self.config, api_url):
            logging.error(
                f'Requested service group "{group_name}" does not exist in Firewall config.'
            )
        response = self.put(self.config,api_url,data)
        print(response)
        return {"results" : response}


class DeleteServiceGroupAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        group_name = inputs["group_name"]
        api_url = 'api/v2/cmdb/firewall.service/group/' + group_name
        print(api_url)
        response = self.delete(self.config,api_url)
        print(response)
        return {"results" : response}