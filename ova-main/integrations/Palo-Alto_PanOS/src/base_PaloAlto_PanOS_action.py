import requests
import logging
import xml.etree.ElementTree as ET


class BasePaloAltoAction:
    def __init__(self):
        self.timeout = 10
        self.vdom = "root"
        self.ipaddr = ""
        self.username = ""
        self.password = ""
        self.port = ""
        self.urlbase = ""

    # Login / Logout Handlers
    def login(self, config):
        
        print(config)
        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}"
        login_url = '/api/?type=keygen&user='+self.username + '&password='+self.password
        session = requests.session()
        api_token = session.get(self.urlbase + login_url , verify=False)
        print(api_token.text)
        # Parse the XML data
        root = ET.fromstring(api_token.text)
        # Find the value of the 'key' element
        key_value = root.find(".//key").text
        # Print the key value
        return session,key_value
    
    # API Interaction Methods
    def get(self, config, url):
        
        session,key_value = self.login(config)
        api_url = f"{self.urlbase}{url}"
        print(api_url)
        headers = {"X-PAN-KEY":key_value}
        request = session.get(
            api_url, verify=False, headers=headers,timeout=self.timeout
        )
        if request.status_code == 200:
            return request.json()
        else:
            return request.status_code

    def put(self, config, url, payload):
        
        session,key_value = self.login(config)
        api_url = f"{self.urlbase}{url}"
        print(api_url)
        headers = {"X-PAN-KEY":key_value}
        request = session.put(
            api_url, verify=False, headers=headers,timeout=self.timeout,data = payload
        )
        if request.status_code == 200:
            return request.json()
        else:
            print(request.content)
            return request.status_code

    def post(self, config, url , payload):
        
        session,key_value = self.login(config)
        api_url = f"{self.urlbase}{url}"
        print(api_url)
        headers = {"X-PAN-KEY":key_value}
        request = session.post(
            api_url, verify=False, headers=headers,timeout=self.timeout , data = payload
        )
        if request.status_code == 200:
            return request.json()
        else:
            print(request.content)
            return request.status_code


    def delete(self, config, url):
        
        session,key_value = self.login(config)
        api_url = f"{self.urlbase}{url}"
        print(api_url)
        headers = {"X-PAN-KEY":key_value}
        request = session.delete(
            api_url, verify=False, headers=headers,timeout=self.timeout
        )
        if request.status_code == 200:
            return request.json()
        else:
            print(request.content)
            return request.status_code