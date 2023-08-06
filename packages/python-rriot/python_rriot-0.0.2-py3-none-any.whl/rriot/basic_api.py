"""File for BasicAPI class."""

from typing import Optional

import base64
import hashlib
import requests

from .rriot_data import RRIOTData
from .constants import BasicAPIConstants as BC
from .exceptions import (
    InvalidCredentialsException,
    InvalidEmailFormatException,
    InvalidTokenException,
    NoDataException,
    RequestFrequencyException,
)


class BasicAPI(object):
    """Class for communicating with the basic RRIOT API."""

    _clientid: str = ""
    _timeout: int = BC.DEFAULT_TIMEOUT
    _token: str = ""
    _url: str = BC.DEFAULT_URL

    def login(self, username: str, password: str) -> RRIOTData:
        """Login and retrieve RRIOTData."""
        # Update ClientID
        self._clientid = self._generate_clientid(username)

        # Update URL
        self._url = self.get_url_for_email(username)

        # Login
        login_data = self.post(
            BC.PATH_LOGIN,
            {
                "username": username,
                "password": password,
                "needtwostepauth": "false",
            },
        )
        # Update token
        self._token = login_data.get("token")

        # Get home details
        home_data = self.get(BC.PATH_HOMEDETAILS)

        # Compile and return data
        rriot = login_data.get("rriot", {})
        urls = rriot.get("r", {})
        rriot_data = RRIOTData()
        rriot_data.basic_url = self._url
        rriot_data.hawk_url = urls.get("a", "")
        rriot_data.mqtt_url = urls.get("m", "")
        rriot_data.email = username
        rriot_data.username = rriot.get("u", "")
        rriot_data.secret = rriot.get("s", "")
        rriot_data.hash = rriot.get("h", "")
        rriot_data.key = rriot.get("k", "")
        rriot_data.home_id = home_data.get("rrHomeId")
        return rriot_data

    def get_url_for_email(self, email: str) -> str:
        """Get the correct URL for a given email."""
        return self.post(BC.PATH_URL, {"email": email}).get("url")

    def set_parameters(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """Manually set parameters."""
        if url:
            self._url = url
        if username:
            self._clientid = self._generate_clientid(username)
        if token:
            self._token = token

    def get(self, path: str) -> dict:
        """Make a GET request."""
        url = self._url + path
        headers = self._get_headers(path)
        response = requests.get(
            url=url,
            headers=headers,
            timeout=self._timeout,
        )
        return self._process_response(response)

    def post(self, path: str, params: dict) -> dict:
        """Make a POST request."""
        url = self._url + path
        headers = self._get_headers(path)
        response = requests.post(
            url=url,
            headers=headers,
            data=params,
            timeout=self._timeout,
        )
        return self._process_response(response)

    def _get_headers(self, path: str) -> dict:
        """Get headers required for a given path."""
        if (path == BC.PATH_LOGIN) or (path == BC.PATH_URL):
            return {"header_clientid": self._clientid}
        else:
            return {"Authorization": self._token}

    def _generate_clientid(self, username: str) -> str:
        """Generate a clientid for a given username."""
        id_hash = hashlib.md5()
        id_hash.update(str.encode(username))
        id_hash.update(str.encode(BC.UNIQUE_IDENTIFIER))
        return base64.b64encode(id_hash.digest()).decode()

    def _process_response(self, response: requests.Response) -> dict:
        """Check a response is valid and extract data."""
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.status_code, response)
        data = response.json()
        if data is None:
            raise NoDataException(response)
        if ("data" not in data) or (data.get("data") is None):
            if "code" in data:
                code = data.get("code")
                msg = data.get("msg") if ("msg" in data) else "No Message"
                if code == 2003:
                    raise InvalidEmailFormatException(code, msg)
                if code == 2010:
                    raise InvalidTokenException(code, msg)
                if code == 2012:
                    raise InvalidCredentialsException(code, msg)
                if code == 9002:
                    raise RequestFrequencyException(code, msg)
                raise NoDataException(code, msg)
            raise NoDataException(response)
        inner_data = data.get("data")

        return inner_data
