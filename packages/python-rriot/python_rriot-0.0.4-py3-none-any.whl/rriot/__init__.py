"""File for RRIOT class."""

from .basic_api import BasicAPI
from .rriot_data import RRIOTData


class RRIOT(object):
    """Main class for interacting with RRIOT APIs."""

    _basic_api: BasicAPI = BasicAPI()
    _data: RRIOTData = RRIOTData()

    @property
    def data(self):
        """Getter for _data."""
        return self._data

    def login(self, username: str, password: str) -> RRIOTData:
        """Login to the APIs."""
        self._data = self._basic_api.login(username, password)
        self._connect_hawk()
        return self.data

    def resume(self, data: RRIOTData) -> RRIOTData:
        """Resume an existing connection."""
        self._data = data
        self._basic_api.setup(data.basic_url, data.email, data.token)
        self._connect_hawk()
        return self.data

    def _connect_hawk(self):
        """Connect to the HAWK API."""
