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
    connection_response_schema = ConnectionResponse
    dcgw_response_schema = DirectConnectGatewayResponse
    vpgw_response_schema = VirtualPrivateGatewayResponse
    lag_response_schema = LAGResponse

    service_name = 'directconnect'

    def get_resources(self):
        print("** Direct Connect START **")
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            for data in self.connection_request_data(region_name):
                yield self.connection_response_schema(
                    {'resource': ConnectionResource({'data': data,
                                                     'reference': ReferenceModel(data.reference)})})

            for data in self.virtual_private_gateway_request_data(region_name):
                yield self.vpgw_response_schema(
                    {'resource': VirtualPrivateGatewayResource({'data': data,
                                                                'reference': ReferenceModel(data.reference)})})

            for data in self.lag_request_data(region_name):
                yield self.lag_response_schema(
                    {'resource': LAGResource({'data': data,
                                              'reference': ReferenceModel(data.reference)})})

        for data in self.direct_connect_gateway_request_data():
            yield self.dcgw_response_schema(
                {'resource': DirectConnectGatewayResource({'data': data,
                                                           'reference': ReferenceModel(data.reference)})})

    def connection_request_data(self, region_name) -> List[Connection]:
        response = self.client.describe_connections()

        for raw in response.get('connections', []):
            raw.update({
                'region_name': region_name,
                'account_id': self.account_id
            })
            yield Connection(raw, strict=False)

    def direct_connect_gateway_request_data(self) -> List[Connection]:
        response = self.client.describe_direct_connect_gateways()

        for raw in response.get('directConnectGateways', []):
            raw.update({
                'region_name': '',
                'account_id': self.account_id
            })
            yield DirectConnecGateway(raw, strict=False)

    def virtual_private_gateway_request_data(self, region_name) -> List[Connection]:
        response = self.client.describe_virtual_gateways()

        for raw in response.get('virtualGateways', []):
            raw.update({
                'region_name': region_name,
                'account_id': self.account_id
            })
            yield VirtualPrivateGateway(raw, strict=False)

    def lag_request_data(self, region_name) -> List[Connection]:
        response = self.client.describe_lags()

        for raw in response.get('lags', []):
            raw.update({
                'region_name': region_name,
                'account_id': self.account_id
            })
            yield LAG(raw, strict=False)