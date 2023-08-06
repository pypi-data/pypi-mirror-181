"""Constants for python-rriot."""


class CommonConstants(object):
    """Constants for use across the whole module."""


class BasicAPIConstants(object):
    """Constants for use in the BasicAPI class."""

    DEFAULT_URL: str = "https://euiot.roborock.com"

    PATH_HOMEDETAILS: str = "/api/v1/getHomeDetail"
    PATH_LOGIN: str = "/api/v1/login"
    PATH_URL: str = "/api/v1/getUrlByEmail"

    UNIQUE_IDENTIFIER: str = "python-rriot"

    DEFAULT_TIMEOUT: int = 3
