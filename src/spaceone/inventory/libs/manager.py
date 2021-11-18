import json
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.schema.resource import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class AWSManager(BaseManager):
    connector_name = None

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector = self.locator.get_connector(self.connector_name, secret_data=secret_data)
        connector.verify()

    def collect_resources(self, **kwargs) -> list:
        try:
            connector = self.locator.get_connector(self.connector_name, **kwargs)
            return connector.collect_data()
        except Exception as e:
            _LOGGER.error(f'[collect_resources] {e}')

            if type(e) is dict:
                return [
                    ErrorResourceResponse(
                        {'message': json.dumps(e),
                         'resource': {'cloud_service_group': connector.cloud_service_group,
                                      'cloud_service_type': connector.cloud_service_type}}
                    )]
            else:
                return [
                    ErrorResourceResponse(
                        {'message': str(e),
                         'resource': {'cloud_service_group': connector.cloud_service_group,
                                      'cloud_service_type': connector.cloud_service_type}}
                    )]
            
