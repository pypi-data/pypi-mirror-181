"""File for Exception classes."""


class RRIOTException(Exception):
    """Base python-rriot exception class."""


class NoDataException(RRIOTException):
    """Exception when a response has no data."""


class InvalidCredentialsException(RRIOTException):
    """Exception when the provided credentials were invalid."""


class InvalidEmailFormatException(RRIOTException):
    """Exception when the provided email was in the wrong format."""


class InvalidTokenException(RRIOTException):
    """Exception when the provided auth token was invalid."""


class RequestFrequencyException(RRIOTException):
    """Exception when the API has been accessed too frequently."""
