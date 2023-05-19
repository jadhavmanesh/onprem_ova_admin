import requests
import logging
import json


class BaseDsmAction:
    def __init__(self):
        self.ipaddr = ""
        self.username = ""
        self.password = ""
        self.port = ""
        self.urlbase = ""

    # Login / Logout Handlers
    def login(self, config):
        """
        Log in to FortiGate with info provided in during class instantiation
        :param config: configuration file
        :return: Open Session
        """
        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}/rest/"

        session = requests.session()
        url = self.urlbase + "authentication/login/"
        params = {
            "dsCredentials": {
                "tenantName": "",
                "userName": self.username,
                "password": self.password,
            }
        }
        # Login
        response = session.post(url, json=params, verify=False)
        if response.status_code == 200:
            for x in response:
                session_id = x
                session_id = str(session_id, 'UTF-8')
                params = {
                    "sID": session_id
                }
            print("Login success")
            return session, params
        else:
            print("Login fail")
            params = {
                    "sID": "Login fail"
                }
            return response.status_code

        

    def logout(self, session, params):
        """
        Log out of device
        :param session: Session created by login method
        :return: None
        """
        url = self.urlbase + "authentication/logout"
        response = session.delete(url, params=params, verify=False)
        print("Session delete and logged out.")
        logging.info("Session logged out.")

    # API Interaction Methods

    def get(self, config, url):
        """
        Perform GET operation on provided URL
        :param config: configuration file
        :param url: Target of GET operation
        :return: Request result if successful (type list), HTTP status code otherwise (type int)
        """
        print(config)
        session, params = self.login(config)
        api_url = f"{self.urlbase}{url}"
        response = session.get(api_url, verify=False, params=params)
        self.logout(session, params)
        if response.status_code == 200:
            #print("Antimalware Events Fetched")
            return json.loads(response.content)
        else:
            return response.status_code

    def put(self, config, url, data):
        """
        Perform PUT operation on provided URL
        :param config: configuration file
        :param url: Target of PUT operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
        :return: Result from put operation
        """
        session = self.login(config)
        api_url = f"{self.urlbase}{url}"
        result = session.put(
            api_url,
            json=data,
            verify=False,
            timeout=self.timeout,
            params="vdom=" + self.vdom,
        )
        self.logout(session)
        return result.json()

    def post(self, config, url, data):
        """
        Perform POST operation on provided URL
        :param config: configuration file
        :param url: Target of POST operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
        :return: result from post operation
        """
        session = self.login(config)
        api_url = f"{self.urlbase}{url}"
        result = session.post(
            api_url,
            json=data,
            verify=False,
            timeout=self.timeout,
            params="vdom=" + self.vdom,
        )
        self.logout(session)
        return result.json()

    def delete(self, config, url):
        """
        Perform DELETE operation on provided URL
        :param config: configuration file
        :param url: Target of DELETE operation
        :return: result from delete operation
        """
        session = self.login(config)
        api_url = f"{self.urlbase}{url}"
        result = session.delete(
            api_url, verify=False, timeout=self.timeout, params="vdom=" + self.vdom
        )
        self.logout(session)
        return result.json()
