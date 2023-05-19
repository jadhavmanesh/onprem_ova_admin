import requests
import logging


class BaseTMSMSAction:
    def __init__(self):
        self.timeout = 10
        self.vdom = "root"
        self.ipaddr = ""
        self.username = ""
        self.password = ""
        self.port = ""
        self.urlbase = ""

    def get(self, config, url):
        """
        Perform GET operation on provided URL
        :param config: configuration file
        :param url: Target of GET operation
        :return: Request result if successful (type list), HTTP status code otherwise (type int)
        """
        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}/"

        api_url = f"{self.urlbase}{url}"

        response = requests.get(api_url, auth=(
            self.username, self.password), verify=False)

        # print(response.content)

        # print(response.text)

        # print(response)

        output = {"finalOutput": response.text}

        return output

    def put(self, config, url, data):
        """
        Perform PUT operation on provided URL
        :param config: configuration file
        :param url: Target of PUT operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
        :return: Result from put operation
        """

        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}/"

        api_url = f"{self.urlbase}{url}"

        response = requests.put(api_url, auth=(
            self.username, self.password), verify=False)

        # print(response.content)

        # print(response.text)

        # print(response)

        output = {"finalOutput": response.text}

        return output

    def post(self, config, url, data):
        """
        Perform POST operation on provided URL
        :param config: configuration file
        :param url: Target of POST operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
        :return: result from post operation
        """

        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}/"

        api_url = f"{self.urlbase}{url}"

        response = requests.post(api_url, auth=(
            self.username, self.password), verify=False)

        # print(response.content)

        # print(response.text)

        # print(response)

        output = {"finalOutput": response.text}

        return output

    def delete(self, config, url):
        """
        Perform DELETE operation on provided URL
        :param config: configuration file
        :param url: Target of DELETE operation
        :return: result from delete operation
        """
        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}/"

        api_url = f"{self.urlbase}{url}"

        response = requests.delete(api_url, auth=(
            self.username, self.password), verify=False)

        # print(response.content)

        # print(response.text)

        # print(response)

        output = {"finalOutput": response.text}

        return output
