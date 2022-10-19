import time
import logging
from typing import List

from spaceone.inventory.connector.aws_direct_connect_connector.schema.data import Connection, DirectConnectGateway, \
    VirtualPrivateGateway, LAG
from spaceone.inventory.connector.aws_direct_connect_connector.schema.resource import ConnectionResource, \
    ConnectionResponse, DirectConnectGatewayResource, DirectConnectGatewayResponse, VirtualPrivateGatewayResource, \
    VirtualPrivateGatewayResponse, LAGResource, LAGResponse
from spaceone.inventory.connector.aws_direct_connect_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class DirectConnectConnector(SchematicAWSConnector):
    service_name = 'directconnect'
    cloud_service_group = 'DirectConnect'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Direct Connect")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

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

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Direct Connect ({time.time() - start_time} sec)')
        return resources

    def connection_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'Connection'
        cloudwatch_namespace = 'AWS/DX'
        cloudwatch_dimension_name = 'ConnectionId'

        response = self.client.describe_connections()

        for raw in response.get('connections', []):
            try:
                bandwidth_size = self.convert_bandwidth_gbps(raw.get('bandwidth', ''))

                if bandwidth_size:
                    raw.update({'bandwidth_gbps': bandwidth_size})

                raw.update({
                    'cloudtrail': self.set_cloudtrail(region_name, None, raw['connectionId']),
                    'cloudwatch': self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                      raw['connectionId'], region_name),
                })
                connection_vo = Connection(raw, strict=False)
                yield {
                    'data': connection_vo,
                    'instance_size': bandwidth_size,
                    'name': connection_vo.connection_name,
                    'instance_type': connection_vo.location,
                    'account': self.account_id,
                    'tags': self.convert_tags_to_dict_type(raw.get('tags', []), key='key', value='value')
                }

            except Exception as e:
                resource_id = raw.get('connectionId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def direct_connect_gateway_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'DirectConnectGateway'

        response = self.client.describe_direct_connect_gateways()

        for raw in response.get('directConnectGateways', []):
            try:
                raw.update({'cloudtrail': self.set_cloudtrail('us-east-1', None, raw['directConnectGatewayId'])})
                dc_gw_vo = DirectConnectGateway(raw, strict=False)
                yield {
                    'data': dc_gw_vo,
                    'name': dc_gw_vo.direct_connect_gateway_name,
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = raw.get('directConnectGatewayId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def virtual_private_gateway_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'VirtualPrivateGateway'

        response = self.client.describe_virtual_gateways()

        for raw in response.get('virtualGateways', []):
            try:
                raw.update({'cloudtrail': self.set_cloudtrail(region_name, None, raw['virtualGatewayId'])})
                virtual_private_gw_vo = VirtualPrivateGateway(raw, strict=False)

                yield {
                    'data': virtual_private_gw_vo,
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = raw.get('virtualGatewayId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def lag_request_data(self, region_name) -> List[Connection]:
        self.cloudservice_type = 'LAG'

        response = self.client.describe_lags()
        for raw in response.get('lags', []):
            try:
                raw.update({'cloudtrail': self.set_cloudtrail(region_name, None, raw['lagId'])})

                for lag_connection in raw.get('connections', []):
                    bandwidth_size = self.convert_bandwidth_gbps(lag_connection.get('bandwidth', ''))

                    if bandwidth_size:
                        lag_connection.update({'bandwidth_gbps': bandwidth_size})

                lag_vo = LAG(raw, strict=False)

                yield {
                    'data': lag_vo,
                    'name': lag_vo.lag_name,
                    'account': self.account_id,
                    'tags': self.convert_tags_to_dict_type(raw.get('tags', []), key='key', value='value')
                }

            except Exception as e:
                resource_id = raw.get('lagId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    @staticmethod
    def convert_bandwidth_gbps(bandwidth):
        try:
            if 'Mbps' in bandwidth:
                bw_mbps = bandwidth.replace('Mbps', '')
                return float(bw_mbps/1000)
            elif 'Gbps' in bandwidth:
                return float(bandwidth.replace('Gpbs', ''))
            else:
                return float(0)
        except Exception as e:
            return float(0)
