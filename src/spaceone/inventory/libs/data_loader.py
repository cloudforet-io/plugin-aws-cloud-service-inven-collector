import logging
from dataclasses import dataclass

from boto3 import Session

_LOGGER = logging.getLogger(__name__)


@dataclass
class DataLoader:
    session: Session
    data = {}

    def fetch_data(self, resource_id):
        raise NotImplementedError('add fetch data logic')

    def _get_data(self, resource_id):
        try:
            data = self.fetch_data(resource_id)
        except Exception as e:
            _LOGGER.debug(e)
        return data or {}

    def get(self, resource_id) -> {}:
        if resource_id not in self.data:
            self.data[resource_id] = self._get_data(resource_id)
        return self.data[resource_id]
