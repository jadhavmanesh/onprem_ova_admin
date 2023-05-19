import json
import os
import traceback
import xml.etree.cElementTree as ET
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from typing import Optional


def urljoin(url, suffix=""):
    """
        Will join url and its suffix

        Example:
        "https://google.com/", "/"   => "https://google.com/"
        "https://google.com", "/"   => "https://google.com/"
        "https://google.com", "api"   => "https://google.com/api"
        "https://google.com", "/api"  => "https://google.com/api"
        "https://google.com/", "api"  => "https://google.com/api"
        "https://google.com/", "/api" => "https://google.com/api"

        :type url: ``string``
        :param url: URL string (required)

        :type suffix: ``string``
        :param suffix: the second part of the url

        :rtype: ``string``
        :return: Full joined url
    """
    if url[-1:] != "/":
        url = url + "/"

    if suffix.startswith("/"):
        suffix = suffix[1:]
        return url + suffix

    return url + suffix


def skip_proxy():
    """
    The function deletes the proxy environment vars in order to http requests to skip routing through proxy

    :return: None
    :rtype: ``None``
    """
    for k in ('HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy'):
        if k in os.environ:
            del os.environ[k]


def skip_cert_verification():
    """
    The function deletes the self signed certificate env vars in order to http requests to skip certificate validation.

    :return: None
    :rtype: ``None``
    """
    for k in ('REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE'):
        if k in os.environ:
            del os.environ[k]


class BaseClient(object):
    """Client to use in integrations with powerful _http_request
    :type base_url: ``str``
    :param base_url: Base server address with suffix, for example: https://example.com/api/v2/.

    :type verify: ``bool``
    :param verify: Whether the request should verify the SSL certificate.

    :type proxy: ``bool``
    :param proxy: Whether to run the integration using the system proxy.

    :type ok_codes: ``tuple``
    :param ok_codes:
        The request codes to accept as OK, for example: (200, 201, 204).
        If you specify "None", will use requests.Response.ok

    :type headers: ``dict``
    :param headers:
        The request headers, for example: {'Accept`: `application/json`}.
        Can be None.

    :type auth: ``dict`` or ``tuple``
    :param auth:
        The request authorization, for example: (username, password).
        Can be None.

    :return: No data returned
    :rtype: ``None``
    """

    def __init__(self, base_url, verify=True, proxy=False, ok_codes=tuple(), headers=None, auth=None):
        self._base_url = base_url
        self._verify = verify
        self._ok_codes = ok_codes
        self._headers = headers
        self._auth = auth
        self._session = requests.Session()
        if not proxy:
            skip_proxy()

        if not verify:
            skip_cert_verification()

    def __del__(self):
        try:
            self._session.close()
        except Exception:
            traceback.print_exc()

    def _implement_retry(self, retries=0,
                         status_list_to_retry=None,
                         backoff_factor=5,
                         raise_on_redirect=False,
                         raise_on_status=False):
        """
        Implements the retry mechanism.
        In the default case where retries = 0 the request will fail on the first time

        :type retries: ``int``
        :param retries: How many retries should be made in case of a failure. when set to '0'- will fail on the first time

        :type status_list_to_retry: ``iterable``
        :param status_list_to_retry: A set of integer HTTP status codes that we should force a retry on.
            A retry is initiated if the request method is in ['GET', 'POST', 'PUT']
            and the response status code is in ``status_list_to_retry``.

        :type backoff_factor ``float``
        :param backoff_factor:
            A backoff factor to apply between attempts after the second try
            (most errors are resolved immediately by a second try without a
            delay). urllib3 will sleep for::

                {backoff factor} * (2 ** ({number of total retries} - 1))

            seconds. If the backoff_factor is 0.1, then :func:`.sleep` will sleep
            for [0.0s, 0.2s, 0.4s, ...] between retries. It will never be longer
            than :attr:`Retry.BACKOFF_MAX`.

            By default, backoff_factor set to 5

        :type raise_on_redirect ``bool``
        :param raise_on_redirect: Whether, if the number of redirects is
            exhausted, to raise a MaxRetryError, or to return a response with a
            response code in the 3xx range.

        :type raise_on_status ``bool``
        :param raise_on_status: Similar meaning to ``raise_on_redirect``:
            whether we should raise an exception, or return a response,
            if status falls in ``status_forcelist`` range and retries have
            been exhausted.
        """
        try:
            method_whitelist = "allowed_methods" if hasattr(Retry.DEFAULT_ALLOWED_METHODS, "allowed_methods") else "method_whitelist"
            whitelist_kawargs = {
                method_whitelist: frozenset(['GET', 'POST', 'PUT'])
            }
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=backoff_factor,
                status=retries,
                status_forcelist=status_list_to_retry,
                raise_on_status=raise_on_status,
                raise_on_redirect=raise_on_redirect,
                **whitelist_kawargs
            )
            adapter = HTTPAdapter(max_retries=retry)
            self._session.mount('http://', adapter)
            self._session.mount('https://', adapter)
        except NameError:
            pass

    def _http_request(self, method, url_suffix='', full_url=None, headers=None, auth=None, json_data=None,
                      params=None, data=None, files=None, timeout=10, resp_type='json', ok_codes=None,
                      return_empty_response=False, retries=0, status_list_to_retry=None,
                      backoff_factor=5, raise_on_redirect=False, raise_on_status=False,
                      error_handler=None, empty_valid_codes=None, **kwargs):
        """A wrapper for requests lib to send our requests and handle requests and responses better.

        :type method: ``str``
        :param method: The HTTP method, for example: GET, POST, and so on.

        :type url_suffix: ``str``
        :param url_suffix: The API endpoint.

        :type full_url: ``str``
        :param full_url:
            Bypasses the use of self._base_url + url_suffix. This is useful if you need to
            make a request to an address outside of the scope of the integration
            API.

        :type headers: ``dict``
        :param headers: Headers to send in the request. If None, will use self._headers.

        :type auth: ``tuple``
        :param auth:
            The authorization tuple (usually username/password) to enable Basic/Digest/Custom HTTP Auth.
            if None, will use self._auth.

        :type params: ``dict``
        :param params: URL parameters to specify the query.

        :type data: ``dict``
        :param data: The data to send in a 'POST' request.

        :type json_data: ``dict``
        :param json_data: The dictionary to send in a 'POST' request.

        :type files: ``dict``
        :param files: The file data to send in a 'POST' request.

        :type timeout: ``float`` or ``tuple``
        :param timeout:
            The amount of time (in seconds) that a request will wait for a client to
            establish a connection to a remote machine before a timeout occurs.
            can be only float (Connection Timeout) or a tuple (Connection Timeout, Read Timeout).

        :type resp_type: ``str``
        :param resp_type:
            Determines which data format to return from the HTTP request. The default
            is 'json'. Other options are 'text', 'content', 'xml' or 'response'. Use 'response'
             to return the full response object.

        :type ok_codes: ``tuple``
        :param ok_codes:
            The request codes to accept as OK, for example: (200, 201, 204). If you specify
            "None", will use self._ok_codes.

        :return: Depends on the resp_type parameter
        :rtype: ``dict`` or ``str`` or ``requests.Response``

        :type retries: ``int``
        :param retries: How many retries should be made in case of a failure. when set to '0'- will fail on the first time

        :type status_list_to_retry: ``iterable``
        :param status_list_to_retry: A set of integer HTTP status codes that we should force a retry on.
            A retry is initiated if the request method is in ['GET', 'POST', 'PUT']
            and the response status code is in ``status_list_to_retry``.

        :type backoff_factor ``float``
        :param backoff_factor:
            A backoff factor to apply between attempts after the second try
            (most errors are resolved immediately by a second try without a
            delay). urllib3 will sleep for::

                {backoff factor} * (2 ** ({number of total retries} - 1))

            seconds. If the backoff_factor is 0.1, then :func:`.sleep` will sleep
            for [0.0s, 0.2s, 0.4s, ...] between retries. It will never be longer
            than :attr:`Retry.BACKOFF_MAX`.

            By default, backoff_factor set to 5

        :type raise_on_redirect ``bool``
        :param raise_on_redirect: Whether, if the number of redirects is
            exhausted, to raise a MaxRetryError, or to return a response with a
            response code in the 3xx range.

        :type raise_on_status ``bool``
        :param raise_on_status: Similar meaning to ``raise_on_redirect``:
            whether we should raise an exception, or return a response,
            if status falls in ``status_forcelist`` range and retries have
            been exhausted.

        :type error_handler ``callable``
        :param error_handler: Given an error entery, the error handler outputs the
            new formatted error message.

        :type empty_valid_codes: ``list``
        :param empty_valid_codes: A list of all valid status codes of empty responses (usually only 204, but
            can vary)

        """
        try:
            # Replace params if supplied
            address = full_url if full_url else urljoin(self._base_url, url_suffix)
            headers = headers if headers else self._headers
            auth = auth if auth else self._auth
            if retries:
                self._implement_retry(retries, status_list_to_retry, backoff_factor, raise_on_redirect, raise_on_status)
            # Execute
            res = self._session.request(
                method,
                address,
                verify=self._verify,
                params=params,
                data=data,
                json=json_data,
                files=files,
                headers=headers,
                auth=auth,
                timeout=timeout,
                **kwargs
            )
            # Handle error responses gracefully
            if not self._is_status_code_valid(res, ok_codes):
                if error_handler:
                    error_handler(res)
                else:
                    err_msg = 'Error in API call [{}] - {}' \
                        .format(res.status_code, res.reason)
                    try:
                        # Try to parse json error response
                        error_entry = res.json()
                        err_msg += '\n{}'.format(json.dumps(error_entry))
                        raise Exception(err_msg)
                    except ValueError:
                        err_msg += '\n{}'.format(res.text)
                        raise Exception(err_msg)

            if not empty_valid_codes:
                empty_valid_codes = [204]
            is_response_empty_and_successful = (res.status_code in empty_valid_codes)
            if is_response_empty_and_successful and return_empty_response:
                return res

            resp_type = resp_type.lower()
            try:
                if resp_type == 'json':
                    return res.json()
                if resp_type == 'text':
                    return res.text
                if resp_type == 'content':
                    return res.content
                if resp_type == 'xml':
                    ET.parse(res.text)
                return res
            except ValueError as exception:
                raise Exception('Failed to parse json object from response: {}'
                                .format(res.content), exception)
        except requests.exceptions.ConnectTimeout as exception:
            err_msg = 'Connection Timeout Error - potential reasons might be that the Server URL parameter' \
                      ' is incorrect or that the Server is not accessible from your host.'
            raise Exception(err_msg, exception)
        except requests.exceptions.SSLError as exception:
            # in case the "Trust any certificate" is already checked
            if not self._verify:
                raise
            err_msg = 'SSL Certificate Verification Failed - try selecting \'Trust any certificate\' checkbox in' \
                      ' the integration configuration.'
            raise Exception(err_msg, exception)
        except requests.exceptions.ProxyError as exception:
            err_msg = 'Proxy Error - if the \'Use system proxy\' checkbox in the integration configuration is' \
                      ' selected, try clearing the checkbox.'
            raise Exception(err_msg, exception)
        except requests.exceptions.ConnectionError as exception:
            # Get originating Exception in Exception chain
            error_class = str(exception.__class__)
            err_type = '<' + error_class[error_class.find('\'') + 1: error_class.rfind('\'')] + '>'
            err_msg = 'Verify that the server URL parameter' \
                      ' is correct and that you have access to the server from your host.' \
                      '\nError Type: {}\nError Number: [{}]\nMessage: {}\n' \
                .format(err_type, exception.errno, exception.strerror)
            raise Exception(err_msg, exception)
        except requests.exceptions.RetryError as exception:
            try:
                reason = 'Reason: {}'.format(exception.args[0].reason.args[0])
            except Exception:  # noqa: disable=broad-except
                reason = ''
            err_msg = 'Max Retries Error- Request attempts with {} retries failed. \n{}'.format(retries, reason)
            raise Exception(err_msg, exception)

    def _is_status_code_valid(self, response, ok_codes=None):
        """If the status code is OK, return 'True'.

        :type response: ``requests.Response``
        :param response: Response from API after the request for which to check the status.

        :type ok_codes: ``tuple`` or ``list``
        :param ok_codes:
            The request codes to accept as OK, for example: (200, 201, 204). If you specify
            "None", will use response.ok.

        :return: Whether the status of the response is valid.
        :rtype: ``bool``
        """
        # Get wanted ok codes
        status_codes = ok_codes if ok_codes else self._ok_codes
        if status_codes:
            return response.status_code in status_codes
        return response.ok


class Client(BaseClient):
    """
    Client for CheckPoint RESTful API.
    Args:
          base_url (str): the URL of CheckPoint.
          sid (str): CheckPoint session ID of the current user session. [Optional]
          use_ssl (bool): specifies whether to verify the SSL certificate or not.
          use_proxy (bool): specifies if to use Demisto proxy settings.
    """

    def __init__(self, base_url: str, use_ssl: bool, use_proxy: bool, sid: Optional[str] = None, **kwargs):
        super().__init__(base_url, verify=use_ssl, proxy=use_proxy, **kwargs)
        self.verify = use_ssl
        self.sid = sid if sid != "None" else None
        self.has_performed_login = False  # set to True once username and password are used to login.
        """ Note that Client is "disposable", and will not be the same object on the next command,
        has_performed_login is used to decide whether to logout after running the command."""

    @property
    def headers(self):
        if self.sid is None:  # for logging in, before self.sid is set
            return {'Content-Type': 'application/json'}
        return {'Content-Type': 'application/json', 'X-chkp-sid': self.sid}

    def login(self, username: str, password: str, session_timeout: int, domain_arg: str = None):
        """login to a checkpoint admin account using username and password."""

        json_body = {'user': username, 'password': password, 'session-timeout': session_timeout}
        if domain_arg:
            json_body['domain'] = domain_arg

        response = self._http_request(method='POST', url_suffix='login', json_data=json_body, headers=self.headers)
        sid = response.get('sid', '')

        if sid:
            self.sid = sid
        return self.sid

    def test_connection(self):
        """
        Returns ok on a successful connection to the CheckPoint Firewall API.
        Otherwise, an exception should be raised by self._http_request()
        """
        response = self._http_request(method='POST', url_suffix='show-api-versions', headers=self.headers,
                                      ok_codes=(200, 500), resp_type='response', json_data={})
        if response.status_code == 500:
            return 'Server Error: make sure Server URL and Server Port are correctly set'

        if response.json() and response.json().get('message') == "Missing header: [X-chkp-sid]":
            return '\nWrong credentials! Please check the username and password you entered and try again.'

        return 'ok'

    def logout(self) -> str:
        """logout from current session, returning the response message"""
        response = self._http_request(method='POST', url_suffix='logout', headers=self.headers, json_data={})
        self.sid = ""
        message = response.get('message')
        return message

    def list_hosts(self, limit: int, offset: int):
        return self._http_request(method='POST', url_suffix='show-hosts',
                                  headers=self.headers, resp_type='json',
                                  json_data={'limit': limit, 'offset': offset})

    def get_host(self, identifier: str):
        return self._http_request(method='POST', url_suffix='show-host', headers=self.headers,
                                  json_data={'name': identifier})

    def add_host(self, name, ip_address, ignore_warnings: bool, ignore_errors: bool, groups):
        return self._http_request(method='POST', url_suffix='add-host', headers=self.headers,
                                  json_data={"name": name, "ip-address": ip_address,
                                             "ignore-warnings": ignore_warnings, "ignore-errors": ignore_errors,
                                             "groups": groups})

    def update_host(self, identifier: str, ignore_warnings: bool, ignore_errors: bool,
                    ip_address: Optional[str], new_name: Optional[str],
                    comments: Optional[str], groups):
        body = {'name': identifier,
                'ip-address': ip_address,
                'new-name': new_name,
                'comments': comments,
                'ignore-warnings': ignore_warnings,
                'ignore-errors': ignore_errors,
                'groups': groups,
                }
        response = self._http_request(method='POST', url_suffix='set-host', headers=self.headers,
                                      json_data=body)
        return response

    def delete_host(self, identifier: str, ignore_warnings: bool, ignore_errors: bool):
        return self._http_request(method='POST', url_suffix='delete-host', headers=self.headers,
                                  json_data={'name': identifier, "ignore-warnings": ignore_warnings,
                                             "ignore-errors": ignore_errors})

    def list_groups(self, limit: int, offset: int):
        return self._http_request(method='POST', url_suffix='show-groups', headers=self.headers,
                                  json_data={"limit": limit, "offset": offset})

    def get_group(self, identifier: str):
        return self._http_request(method='POST', url_suffix='show-group', headers=self.headers,
                                  json_data={'name': identifier})

    def add_group(self, name: str):
        return self._http_request(method='POST', url_suffix='add-group', headers=self.headers,
                                  json_data={"name": name})

    def update_group(self, identifier: str, ignore_warnings: bool, ignore_errors: bool, action: str, members,
                     new_name: Optional[str], comments: Optional[str]):
        # If the desired action is to add or remove members, they should be specified differently.
        members_value = {action: members} if action in ['add', 'remove'] else members
        body = {'name': identifier,
                'new-name': new_name,
                'members': members_value,
                'comments': comments,
                'ignore-warnings': ignore_warnings,
                'ignore-errors': ignore_errors}

        response = self._http_request(method='POST', url_suffix='set-group', headers=self.headers,
                                      json_data=body)
        return response

    def delete_group(self, identifier: str):
        return self._http_request(method='POST', url_suffix='delete-group',
                                  headers=self.headers, json_data={'name': identifier})

    def list_address_ranges(self, limit: int, offset: int):
        return self._http_request(method='POST', url_suffix='show-address-ranges',
                                  headers=self.headers,
                                  json_data={"limit": limit, "offset": offset})

    def get_address_range(self, identifier: str):
        return self._http_request(method='POST', url_suffix='show-address-range',
                                  headers=self.headers, json_data={'name': identifier})

    def add_address_range(self, name: str, ip_address_first: str, ip_address_last: str,
                          set_if_exists: bool, ignore_warnings: bool, ignore_errors: bool, groups):
        body = {'name': name,
                'ip-address-first': ip_address_first,
                'ip-address-last': ip_address_last,
                'set-if-exists': set_if_exists,
                'ignore-warnings': ignore_warnings,
                'ignore-errors': ignore_errors,
                'groups': groups,
                }
        return self._http_request(method='POST', url_suffix='add-address-range',
                                  headers=self.headers, json_data=body)

    def update_address_range(self, identifier: str, ignore_warnings: bool, ignore_errors: bool,
                             ip_address_first: Optional[str], ip_address_last: Optional[str],
                             new_name: Optional[str], comments: Optional[str], groups):
        body = {'name': identifier,
                'ip-address-first': ip_address_first,
                'ip-address-last': ip_address_last,
                'new-name': new_name,
                'comments': comments,
                'ignore-warnings': ignore_warnings,
                'ignore-errors': ignore_errors,
                'groups': groups,
                }
        return self._http_request(method='POST', url_suffix='set-address-range',
                                  headers=self.headers, json_data=body)

    def delete_address_range(self, identifier: str):
        return self._http_request(method='POST', url_suffix='delete-address-range',
                                  headers=self.headers, json_data={'name': identifier})

    def list_threat_indicators(self, limit: int, offset: int):
        return self._http_request(method='POST', url_suffix='show-threat-indicators',
                                  headers=self.headers,
                                  json_data={"limit": limit, "offset": offset})

    def get_threat_indicator(self, identifier):
        return self._http_request(method='POST', url_suffix='show-threat-indicator',
                                  headers=self.headers, json_data={'name': identifier})

    def add_threat_indicator(self, name: str, observables: list):
        return self._http_request(method='POST', url_suffix='add-threat-indicator',
                                  headers=self.headers,
                                  json_data={'name': name, 'observables': observables})

    def update_threat_indicator(self, identifier: str, action: str = None,
                                new_name: str = None, comments: str = None):
        body = {'name': identifier,
                'action': action,
                'new-name': new_name,
                'comments': comments
                }
        return self._http_request(method='POST', url_suffix='set-threat-indicator',
                                  headers=self.headers, json_data=body)

    def delete_threat_indicator(self, identifier: str):
        return self._http_request(method='POST', url_suffix='delete-threat-indicator',
                                  headers=self.headers, json_data={'name': identifier})

    def list_access_rule(self, identifier: str, limit: int, offset: int):
        body = {'name': identifier,
                'limit': limit,
                'offset': offset}
        return self._http_request(method='POST', url_suffix='show-access-rulebase',
                                  headers=self.headers, json_data=body)

    def add_rule(self, layer: str, position, action: str, name: Optional[str],
                 vpn: Optional[str], destination, service, source):
        body = {'layer': layer, 'position': position, 'name': name, 'action': action,
                'destination': destination, 'service': service, 'source': source, 'vpn': vpn}
        return self._http_request(method='POST', url_suffix='add-access-rule',
                                  headers=self.headers, json_data=body)

    def update_rule(self, identifier: str, layer: str, ignore_warnings: bool, ignore_errors: bool,
                    enabled: bool, action: Optional[str], new_name: Optional[str], new_position):
        body = {'name': identifier,
                'layer': layer,
                'action': action,
                'enabled': enabled,
                'new-name': new_name,
                'new-position': new_position,
                'ignore-warnings': ignore_warnings,
                'ignore-errors': ignore_errors
                }
        return self._http_request(method='POST', url_suffix='set-access-rule',
                                  headers=self.headers, json_data=body)

    def delete_rule(self, identifier: str, layer: str):
        return self._http_request(method='POST', url_suffix='delete-access-rule',
                                  headers=self.headers,
                                  json_data={'name': identifier, 'layer': layer})

    def list_application_site(self, limit: int, offset: int):
        body = {'limit': limit, 'offset': offset}
        return self._http_request(method='POST', url_suffix='show-application-sites',
                                  headers=self.headers, json_data=body)

    def add_application_site(self, name: str, primary_category: str, identifier, groups):
        body = {"name": name, "primary-category": primary_category,
                'url-list': identifier, 'groups': groups}
        return self._http_request(method='POST', url_suffix='add-application-site',
                                  headers=self.headers, json_data=body)

    def update_application_site(self, identifier: str,
                                urls_defined_as_regular_expression: bool,
                                groups, url_list, description: Optional[str],
                                new_name: Optional[str], primary_category: Optional[str],
                                application_signature: Optional[str]):
        body = {'name': identifier,
                'description': description,
                'new-name': new_name,
                'primary-category': primary_category,
                'urls-defined-as-regular-expression': urls_defined_as_regular_expression,
                'groups': groups,
                'application-signature': application_signature,
                'url-list': url_list,
                }
        return self._http_request(method='POST', url_suffix='set-application-site',
                                  headers=self.headers, json_data=body)

    def add_objects_batch(self, object_type, add_list):
        body = {'objects': [{'type': object_type, 'list': add_list}]}
        return self._http_request(method='POST', url_suffix='add-objects-batch', headers=self.headers, json_data=body)

    def delete_objects_batch(self, object_type, delete_list):
        body = {'objects': [{'type': object_type, 'list': delete_list}]}
        return self._http_request(method='POST', url_suffix='delete-objects-batch', headers=self.headers,
                                  json_data=body)

    def delete_application_site(self, identifier: str):
        return self._http_request(method='POST', url_suffix='delete-application-site',
                                  headers=self.headers, json_data={'name': identifier})

    def show_task(self, task_id):
        return self._http_request(method='POST', url_suffix='show-task',
                                  headers=self.headers, json_data={"task-id": task_id})

    def list_objects(self, limit: int, offset: int, filter_search: str,
                     ip_only: bool, object_type: str):
        body = {'limit': limit, 'offset': offset, 'filter': filter_search,
                "ip-only": ip_only, 'type': object_type}
        return self._http_request(method='POST', url_suffix='show-objects',
                                  headers=self.headers, json_data=body)

    def list_application_site_categories(self, limit: int, offset: int):
        body = {'limit': limit,
                'offset': offset}
        return self._http_request(method='POST', url_suffix='show-application-site-categories',
                                  headers=self.headers, json_data=body)

    def get_application_site_category(self, identifier: str):
        return self._http_request(method='POST', url_suffix='show-application-site-category',
                                  headers=self.headers, json_data={'name': identifier})

    def add_application_site_category(self, identifier: str, groups):
        body = {"name": identifier, 'groups': groups}
        return self._http_request(method='POST', url_suffix='add-application-site-category',
                                  headers=self.headers, json_data=body)

    def list_packages(self, limit: int, offset: int):
        response = self._http_request(method='POST', url_suffix='show-packages',
                                      headers=self.headers,
                                      json_data={'limit': limit, 'offset': offset})
        return response.get('packages')

    def list_package(self, identifier: str):
        return self._http_request(method='POST', url_suffix='show-package',
                                  headers=self.headers, json_data={'name': identifier})

    def list_gateways(self, limit: int, offset: int):
        response = self._http_request(method='POST', url_suffix='show-gateways-and-servers',
                                      headers=self.headers,
                                      json_data={'limit': limit, 'offset': offset,
                                                 'details-level': 'full'})
        return response.get('objects')

    def publish(self):
        return self._http_request(method='POST', url_suffix='publish', headers=self.headers,
                                  json_data={})

    def install_policy(self, policy_package: str, targets, access: bool):
        body = {
            'policy-package': policy_package,
            'targets': targets,
            'access': access,
        }
        return self._http_request(method='POST', url_suffix='install-policy',
                                  headers=self.headers, json_data=body)

    def verify_policy(self, policy_package: str):
        body = {'policy-package': policy_package, }
        return self._http_request(method='POST', url_suffix='verify-policy',
                                  headers=self.headers, json_data=body)

    def show_threat_protection(self, uid: str, name: str, properties: bool, profiles: bool):
        body = {
            'show-ips-additional-properties': properties,
            'show-profiles': profiles
        }
        if uid:
            body['uid'] = uid  # type: ignore

        elif name:
            body['name'] = name  # type: ignore
        return self._http_request(method='POST', url_suffix='show-threat-protection',
                                  headers=self.headers, json_data=body)

    def show_threat_protections(self, args):
        return self._http_request(method='POST', url_suffix='show-threat-protections',
                                  headers=self.headers, json_data=args)

    def add_threat_profile(self, args):
        return self._http_request(method='POST', url_suffix='add-threat-profile',
                                  headers=self.headers, json_data=args)

    def delete_threat_protections(self, args):
        return self._http_request(method='POST', url_suffix='delete-threat-protections',
                                  headers=self.headers, json_data=args)

    def set_threat_protection(self, args):
        return self._http_request(method='POST', url_suffix='set-threat-protection',
                                  headers=self.headers, json_data=args)
