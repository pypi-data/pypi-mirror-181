"""File for BasicAPI class."""

import base64
import hashlib
from requests import Session
from requests.exceptions import HTTPError

from .rriot_data import RRIOTData
from .constants import BasicAPIConstants as BC

from .exceptions import (
    InvalidCredentialsException,
    InvalidEmailFormatException,
    InvalidTokenException,
    NoDataException,
    RequestFrequencyException,
)


class BasicAPI(Session):
    """Class for communicating with the basic RRIOT API."""

    _base_url: str = BC.DEFAULT_URL
    _timeout: int = BC.DEFAULT_TIMEOUT

    _clientid: str = ""
    _token: str = ""

    def login(self, username: str, password: str) -> RRIOTData:
        """Login and retrieve RRIOTData."""
        # Update ClientID
        self._clientid = self._generate_clientid(username)

        # Update URL
        self._base_url = self.get_url_for_email(username)

        # Set auth handler
        self.auth = self._build_auth

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
        rriot_data.basic_url = self._base_url
        rriot_data.hawk_url = urls.get("a", "")
        rriot_data.mqtt_url = urls.get("m", "")
        rriot_data.email = username
        rriot_data.username = rriot.get("u", "")
        rriot_data.secret = rriot.get("s", "")
        rriot_data.hash = rriot.get("h", "")
        rriot_data.key = rriot.get("k", "")
        rriot_data.home_id = home_data.get("rrHomeId")
        return rriot_data

    def request(self, method, url, *args, timeout=None, **kwargs):
        """Override to modify the request and pass it along."""
        # Prepend base URL
        url = self._base_url + url

        # Set timeout
        if timeout is None:
            timeout = self._timeout

        # Make request
        response = super().request(
            method, url, *args, timeout=timeout, **kwargs
        )

        # Process and return response
        return self._process_response(response)

    def setup(self, base_url: str, username: str, token: str) -> bool:
        """Manually set parameters."""
        # Update ClientID
        self._clientid = self._generate_clientid(username)

        # Update URL
        self._base_url = base_url

        # Update token
        self._token = token

        # Set auth handler
        self.auth = self._build_auth

        # Return
        return self.test()

    def get_url_for_email(self, email: str) -> str:
        """Get the correct URL for a given email."""
        return self.post(BC.PATH_URL, {"email": email}).get("url")

    def test(self) -> bool:
        """Test whether we can make requests."""
        return isinstance(self.get(BC.PATH_HOMEDETAILS), dict)

    def _build_auth(self, request):
        """Modify the request by injecting auth header."""
        request.headers["header_clientid"] = self._clientid
        if (
            request.path_url != BC.PATH_LOGIN
            and request.path_url != BC.PATH_URL
        ):
            request.headers["authorization"] = self._token
        return request

    def _generate_clientid(self, username: str) -> str:
        """Generate a clientid for a given username."""
        return base64.b64encode(
            hashlib.md5(
                str.encode(username + BC.UNIQUE_IDENTIFIER),
            ).digest()
        ).decode()

    def _process_response(self, response) -> dict:
        """Check a response is valid and extract data."""
        # Check for unexpected HTTP status
        if response.status_code not in [200]:
            raise HTTPError(response.status_code, response)

        # Get JSON data
        data = response.json()
        if data is None:
            raise NoDataException(response)

        # Get data parts
        code = data.get("code", None)
        msg = data.get("msg", None)
        inner_data = data.get("data", None)

        # Handle codes
        if code and code != 200:
            if code == 2003:
                raise InvalidEmailFormatException(code, msg)
            if code == 2010:
                raise InvalidTokenException(code, msg)
            if code == 2012:
                raise InvalidCredentialsException(code, msg)
            if code == 9002:
                raise RequestFrequencyException(code, msg)
            raise NoDataException(code, msg)

        # Handle null data
        if inner_data is None:
            raise NoDataException(data)

        # return data
        return inner_data
