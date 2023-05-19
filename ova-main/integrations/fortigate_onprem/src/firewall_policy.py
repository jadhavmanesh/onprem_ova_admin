import json
from base_fortigate_action import BaseFortigateAction
import requests
import logging



class GetFirewallPolicyActionByID(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        #policy_id = inputs["policy_id"]
        #api_url = f"api/v2/cmdb/firewall/policy/{policy_id}"
        #results = self.get(self.config, api_url)
        #return results

        policy_id = inputs["policy_id"]
        api_url = 'api/v2/cmdb/firewall/policy/' + policy_id + '/'
        print(api_url)
        response = self.get(self.config,api_url)
        print(response)
        return {"results" : response}
    
    

'''
class GetFirewallPoliciesAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        api_url = f"api/v2/cmdb/firewall/policy/"
        results = self.get(self.config, api_url)
        return results
        '''


# TODO: Move Policy

class RelocateFirewallPolicyActions(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        position = inputs["position"]
        neighbour = inputs["neighbour"]
        policy_id = inputs["policy_id"]
        api_url = 'api/v2/cmdb/firewall/policy/'+policy_id
        print(api_url)
        params = {
        'action': 'move',
        position: neighbour
        }
        print(params)
        response = self.put(self.config,api_url,params)
        print(response)
        return {"results" : response}
        
class UpdateFirewallPolicyAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        policy_id = inputs["policy_id"]
        #data = inputs["data"]
        field_key = inputs["field_key"]
        field_value = inputs["field_value"]
        api_url = 'api/v2/cmdb/firewall/policy/' + policy_id
        payload = {
            'policyid': int(policy_id),
            'q_origin_key': int(policy_id),
            field_key : field_value
        }
       # policy_field: policy_field_value
        #data = json.dumps(payload)
        data = payload
        if not self.does_exist(self.config, api_url):
            logging.error(
                f'Requested policy "{policy_id}" does not exist in Firewall config.'
            )
        response = self.put(self.config,api_url,data)
        print(response)
        return {"results" : response}

        #if isinstance(data, str):
            #data = json.loads(data)

        #api_url = "api/v2/cmdb/firewall/policy/" + requests.utils.quote(
            #policy_id, safe=""
        #)
        #if not self.does_exist(self.config, api_url):
            #logging.error(
                #f'Requested policy "{policy_id}" does not exist in Firewall config.'
            #)
            #raise Exception(f"{policy_id} does not exist")
        #result = self.put(self.config, api_url, data)
        #return result


class CreateFirewallPolicyAction(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        policy_name = inputs["policy_name"]
        policy_srcintf = inputs["policy_srcintf"]
        policy_dstintf = inputs["policy_dstintf"]
        policy_source_address = inputs["policy_source_address"]
        policy_destination_address = inputs["policy_destination_address"]
        policy_service = inputs["policy_service"]
        policy_action = inputs["policy_action"]
        policy_log = inputs["policy_log"]
        policy_nat = inputs["policy_nat"]

        api_url = 'api/v2/cmdb/firewall/policy/'
        print(api_url)
        payload = {
        'json': {
            'name': policy_name,
            'srcintf': [{'name': policy_srcintf}],
            'dstintf': [{'name': policy_dstintf}],
            'srcaddr': policy_source_address,
            'dstaddr': policy_destination_address,
            'action': policy_action,
            'schedule': 'always',
            'service': [{'name': policy_service}],
            'logtraffic': policy_log,
            'nat': policy_nat
        }
    }   
        data = payload
        print(data)
        response = self.post(self.config,api_url,data)
        print(response)
        return {"results" : response}
    
        #data = inputs["data"]
        #if isinstance(data, str):
            #data = json.loads(data)

        #api_url = "api/v2/cmdb/firewall/policy/"
        #if self.does_exist(self.config, api_url + policy_id):
            #raise Exception(f"{policy_id} already exists")
        #result = self.post(self.config, api_url, data)
        #return result


class DeleteFirewallPolicyActionByID(BaseFortigateAction):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self, **inputs):
        policy_id = inputs["policy_id"]
        api_url = 'api/v2/cmdb/firewall/policy/' + policy_id
        print(api_url)
        response = self.delete(self.config,api_url)
        print(response)
        return {"results" : response}
        

        #api_url = "api/v2/cmdb/firewall/policy/" + policy_id
        #result = self.delete(self.config, api_url)
        #return result