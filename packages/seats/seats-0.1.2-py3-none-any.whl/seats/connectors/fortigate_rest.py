import requests
import json
from seats.connectors.connector import ConnectorAPI


class FortigateREST(ConnectorAPI):
    def __init__(self):
        self.hostname: str = ""
        self._url_prefix: str = ""
        self._debug: bool = False
        self._http_debug: bool = False
        self._https: bool = True
        self._session: requests.session = requests.session()
        self._auth_token: str = ""
        self.log_session_id: str = ""

    def __str__(self):
        return self.hostname

    def debug(self, status):
        if status == "on":
            self._debug = True
        if status == "off":
            self._debug = False

    def http_debug(self, status):
        if status == "on":
            self._http_debug = True
        if status == "off":
            self._http_debug = False

    def https(self, status):
        if status == "on":
            self._https = True
        if status == "off":
            self._https = False

    def update_csrf(self):
        # Retrieve server csrf and update session's headers
        for cookie in self._session.cookies:
            if cookie.name == "ccsrftoken":
                csrftoken = cookie.value[1:-1]  # token stored as a list
                self._session.headers.update({"X-CSRFTOKEN": csrftoken})

    def url_prefix(self, host):
        if self._https is True:
            self._url_prefix = "https://" + host
        else:
            self._url_prefix = "http://" + host

    def login_token(self, host, token):
        self._auth_token = token
        self._session.headers.update({"Authorization": "Bearer {}".format(token)})
        self._session.verify = False
        self.url_prefix(host)

    def login(self, host, username, password, timeout=None, path="/logincheck"):
        self.url_prefix(host)
        url = self._url_prefix + path
        res = self._session.post(
            url,
            data="username=" + username + "&secretkey=" + password,
            verify=False,
            timeout=timeout,
        )
        # Update session's csrftoken
        self.update_csrf()
        return res

    def logout(self, path="/logout"):
        url = self._url_prefix + path
        res = self._session.post(url)
        return res

    api_get_path = "/api/v2/"
    valid_apis = {"monitor", "cmdb", "log"}

    def get_url(self, api, path, name, action, mkey):
        # Check for valid api
        if api not in self.valid_apis:
            print("Unknown API {0}. Ignore.".format(api))
            return

        # Construct URL request, action and mkey are optional
        url_postfix = self.api_get_path + api + "/" + path + "/" + name
        if action:
            url_postfix += "/" + action
        if mkey:
            url_postfix = url_postfix + "/" + str(mkey)
        url = self._url_prefix + url_postfix
        return url

    def get(self, api, path, name, action=None, mkey=None, parameters=None):
        url = self.get_url(api, path, name, action, mkey)
        res = self._session.get(url, params=parameters)
        return res

    def post(self, api, path, name, action=None, mkey=None, parameters=None, data=None):
        url = self.get_url(api, path, name, action, mkey)
        res = self._session.post(url, params=parameters, data=json.dumps(data))
        return res

    def put(self, api, path, name, action=None, mkey=None, parameters=None, data=None):
        url = self.get_url(api, path, name, action, mkey)
        res = self._session.put(url, params=parameters, data=json.dumps(data))
        return res

    def delete(
        self, api, path, name, action=None, mkey=None, parameters=None, data=None
    ):
        url = self.get_url(api, path, name, action, mkey)
        res = self._session.delete(url, params=parameters, data=json.dumps(data))
        return res
