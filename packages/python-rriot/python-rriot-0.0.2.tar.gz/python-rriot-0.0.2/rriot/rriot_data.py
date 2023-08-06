"""File for RRIOTData class."""


class RRIOTData(object):
    """Class for storing variables required to access the APIs."""

    basic_url: str
    hawk_url: str
    mqtt_url: str

    email: str
    username: str
    secret: str
    hash: str
    key: str

    home_id: int

    def to_dict(self) -> dict:
        """Convert to a dict."""
        return vars(self)

    @staticmethod
    def from_dict(data_dict: dict) -> "RRIOTData":
        """Create an instance from a dict."""
        rriot_data = RRIOTData()
        for key, value in data_dict.items():
            setattr(rriot_data, key, value)
        return rriot_data
