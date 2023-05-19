import requests
import logging


class BaseFortigateAction:
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
        """
        Log in to FortiGate with info provided in during class instantiation
        :param config: configuration file
        :return: Open Session
        """
        self.ipaddr = config.get("hostname")
        self.username = config.get("username")
        self.password = config.get("device_password")
        self.port = config.get("port")

        self.urlbase = f"https://{self.ipaddr}:{self.port}/"

        session = requests.session()
        url = self.urlbase + "logincheck"
        print(config,url)
        # Login
        session.post(
            url,
            data="username={username}&secretkey={password}".format(
                username=self.username, password=self.password
            ),
            verify=False,
            timeout=self.timeout,
        )

        # Get CSRF token from cookies, add to headers
        for cookie in session.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # strip quotes
                session.headers.update({"X-CSRFTOKEN": csrftoken})

        # Check whether login was successful
        login_check = session.get(self.urlbase + "api/v2/cmdb/system/vdom")
        login_check.raise_for_status()
        print(login_check.status_code)
        return session

    def logout(self, session):
        """
        Log out of device
        :param session: Session created by login method
        :return: None
        """
        url = self.urlbase + "logout"
        session.get(url, verify=False, timeout=self.timeout)
        logging.info("Session logged out.")

    # General Logic Methods
    def does_exist(self, config, object_url):
        """
        GET URL to assert whether it exists within the firewall
        :param config: configuration file
        :param object_url: Object to locate
        :return: Bool - True if exists, False if not
        """
        session = self.login(config)
        api_url = f"{self.urlbase}{object_url}"
        request = session.get(
            api_url, verify=False, timeout=self.timeout, params="vdom=" + self.vdom
        )
        self.logout(session)
        if request.status_code == 200:
            return True
        else:
            return False

    # API Interaction Methods
    def get(self, config, url):
        """
        Perform GET operation on provided URL
        :param config: configuration file
        :param url: Target of GET operation
        :return: Request result if successful (type list), HTTP status code otherwise (type int)
        """
        session = self.login(config)
        api_url = f"{self.urlbase}{url}"
        request = session.get(
            api_url, verify=False, timeout=self.timeout, params="vdom=" + self.vdom
        )
        self.logout(session)
        if request.status_code == 200:
            return request.json()["results"]
        else:
            return request.status_code

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
