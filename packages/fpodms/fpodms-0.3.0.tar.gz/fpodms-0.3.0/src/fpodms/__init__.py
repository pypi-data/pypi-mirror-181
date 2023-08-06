import inflection
import requests

from fpodms.api import API
from fpodms.export import Export


class _SessionData:
    def __init__(self, **session_data):
        for k, v in session_data.items():
            k = k.replace(".", "_")
            k = inflection.camelize(k)
            k = inflection.underscore(k)

            if isinstance(v, dict):
                self.__dict__[k] = _SessionData(**v)
            else:
                self.__dict__[k] = v


class Client:
    """An F&P ODMS session.

    :param email_address: A string, a valid login email address.
    :param password: A string, a valid login email address.
    """

    def __init__(self, email_address, password):
        self.base_url = "https://fpdms.heinemann.com"
        self.session = requests.session()

        login_response = self._request(
            method="POST",
            path="api/account/login",
            data={
                "emailAddress": email_address,
                "password": password,
            },
        )

        if login_response["state"] == "Failed":
            raise requests.exceptions.HTTPError(login_response)
        else:
            session_data = _SessionData(**login_response)

            self.preferences = session_data.preferences
            self.session_timeout_minutes = session_data.session_timeout_minutes
            self.state = session_data.state
            self.user = session_data.user
            self.api = API(self)
            self.export = Export(self)

    def _request(self, method, path, content_type="json", params={}, data={}):
        try:
            response = self.session.request(
                method=method, url=f"{self.base_url}/{path}", params=params, json=data
            )
            response.raise_for_status()

            if content_type == "json":
                return response.json()["data"]
            else:
                return response
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError from e
