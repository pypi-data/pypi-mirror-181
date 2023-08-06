"""File for HawkAPI class."""

import base64
import hashlib
from hmac import HMAC
import secrets
import time

from requests import Session
from requests.exceptions import HTTPError

from .constants import HawkAPIConstants as HC
from .exceptions import (
    NoDataException,
    InvalidCredentialsException,
    InvalidTokenException,
)


class HawkAPI(Session):
    """Class for communicating with the Hawk-Auth RRIOT API."""

    _base_url: str = ""
    _timeout: int = HC.DEFAULT_TIMEOUT
    _home_id: int = 0

    _username: str = ""
    _secret: str = ""
    _hash: str = ""

    def setup(
        self,
        base_url: str,
        username: str,
        secret: str,
        hmac_hash: str,
        home_id: int,
    ) -> None:
        """Set variables for future requests."""
        self._base_url = base_url
        self._username = username
        self._secret = secret
        self._hash = hmac_hash
        self._home_id = home_id
        self.auth = self._build_auth

    def request(self, method, url, *args, timeout=None, **kwargs):
        """Override to modify the request and pass it along."""
        # Prepend base URL
        url = self._base_url + url

        # Substitute URL variables
        url = str.format(url, home_id=self._home_id)

        # Set timeout
        if timeout is None:
            timeout = self._timeout

        # Make request
        response = super().request(
            method, url, *args, timeout=timeout, **kwargs
        )

        # Process and return response
        return self._process_response(response)

    def _build_auth(self, request):
        """Modify the request by injecting auth header."""
        timestamp = str(int(time.time()))
        nonce = secrets.token_hex(16)
        path_hash = hashlib.md5(str.encode(request.path_url)).digest().hex()
        mac_contents = ":".join(
            [
                self._username,
                self._secret,
                nonce,
                timestamp,
                path_hash,
                "",
                "",
            ]
        )
        mac_hash = base64.b64encode(
            HMAC(
                key=str.encode(self._hash),
                msg=str.encode(mac_contents),
                digestmod=hashlib.sha256,
            ).digest()
        ).decode()
        request.headers["authorization"] = str.format(
            'Hawk id="{u}", s="{s}", ts="{ts}", nonce="{n}", mac="{m}"',
            u=self._username,
            s=self._secret,
            ts=timestamp,
            n=nonce,
            m=mac_hash,
        )
        return request

    def _process_response(self, response):
        """Check a response is valid and extract data."""
        # Check for unexpected HTTP status
        if response.status_code not in [200, 401]:
            raise HTTPError(response.status_code, response)

        # Get JSON data
        data = response.json()
        if data is None:
            raise NoDataException(response)

        # Get data parts
        code = data.get("code", "")
        msg = data.get("msg", "")
        status = data.get("status", "")
        result = data.get("result", None)

        # Handle codes
        if code == "auth.err":
            if msg == "auth.err.invalid.token":
                raise InvalidTokenException(code, data)
            raise InvalidCredentialsException(code, data)

        # Handle statuses
        if status != "ok":
            raise Exception("UNKNOWN_NOT_OK", data)

        # Handle null data
        if result is None:
            raise NoDataException(data)

        # return data
        return result
