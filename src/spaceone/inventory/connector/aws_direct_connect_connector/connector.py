import time
import logging
from typing import List

from spaceone.inventory.connector.aws_direct_connect_connector.schema.data import Connection, DirectConnecGateway, \
    VirtualPrivateGateway, LAG
from spaceone.inventory.connector.aws_direct_connect_connector.schema.resource import ConnectionResource, \
    ConnectionResponse, DirectConnectGatewayResource, DirectConnectGatewayResponse, VirtualPrivateGatewayResource, \
    VirtualPrivateGatewayResponse, LAGResource, LAGResponse
from spaceone.inventory.connector.aws_direct_connect_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class DirectConnectConnector(SchematicAWSConnector):
    service_name = 'directconnect'
    cloud_service_group = 'DirectConnect'

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: Direct Connect")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.connection_request_data,
                'resource': ConnectionResource,
                'response_schema': ConnectionResponse
            },
            {
                'request_method': self.direct_connect_gateway_request_data,
                'resource': DirectConnectGatewayResource,
                'response_schema': DirectConnectGatewayResponse
            },
            {
                'request_method': self.virtual_private_gateway_request_data,
                'resource': VirtualPrivateGatewayResource,
                'response_schema': VirtualPrivateGatewayResponse
            },
            {
                'request_method': self.lag_request_data,
                'resource': LAGResource,
                'response_schema': LAGResponse
            },
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: Direct Connect ({time.time() - start_time} sec)')
        return resources

    def connection_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'Connection'

        response = self.client.describe_connections()

        for raw in response.get('connections', []):
            try:
                raw.update({
                    'account_id': self.account_id
                })
                yield Connection(raw, strict=False), raw.get('connectionName', '')

            except Exception as e:
                resource_id = raw.get('connectionId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response, ''

    def direct_connect_gateway_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'DirectConnectGateway'

        response = self.client.describe_direct_connect_gateways()

        for raw in response.get('directConnectGateways', []):
            try:
                raw.update({
                    'account_id': self.account_id
                })
                yield DirectConnecGateway(raw, strict=False), raw.get('directConnectGatewayName', '')
            except Exception as e:
                resource_id = raw.get('directConnectGatewayId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response, ''

    def virtual_private_gateway_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'VirtualPrivateGateway'

        response = self.client.describe_virtual_gateways()

        for raw in response.get('virtualGateways', []):
            try:
                raw.update({
                    'account_id': self.account_id
                })
                yield VirtualPrivateGateway(raw, strict=False), ''
            except Exception as e:
                resource_id = raw.get('virtualGatewayId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response, ''

    def lag_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'LAG'

        response = self.client.describe_lags()

        for raw in response.get('lags', []):
            try:
                raw.update({
                    'account_id': self.account_id
                })
                yield LAG(raw, strict=False), raw.get('lagName', '')
            except Exception as e:
                resource_id = raw.get('lagId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response, ''
