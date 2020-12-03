import time
import logging
from typing import List

from spaceone.inventory.connector.aws_api_gateway_connector.schema.data import RestAPI, Resource, HTTPWebsocket, Tags
from spaceone.inventory.connector.aws_api_gateway_connector.schema.resource import RestAPIResource, \
    HTTPWebsocketResource, RestAPIResponse, HTTPWebsocketResponse
from spaceone.inventory.connector.aws_api_gateway_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


# Collect REST API
class APIGatewayConnector(SchematicAWSConnector):
    rest_service_name = 'apigateway'
    websocket_service_name = 'apigatewayv2'

    def get_resources(self):
        print("** API Gateway START **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_rest_api_data,
                'resource': RestAPIResource,
                'response_schema': RestAPIResponse,
                'service_name': 'apigateway'
            },
            {
                'request_method': self.request_websocket_data,
                'resource': HTTPWebsocketResource,
                'response_schema': HTTPWebsocketResponse,
                'service_name': 'apigatewayv2'
            }
        ]

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ APIGateway {region_name} ]')
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(collect_resource['service_name'],
                                                             region_name,
                                                             collect_resource))

        print(f' API Gateway Finished {time.time() - start_time} Seconds')
        return resources

    def request_rest_api_data(self, region_name) -> List[RestAPI]:
        # Get REST API
        rest_client = self.set_client(self.rest_service_name)

        paginator = rest_client.get_paginator('get_rest_apis')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('items', []):
                _res = self.client.get_resources(restApiId=raw.get('id'), limit=500)
                raw.update({
                    'protocol': 'REST',
                    'endpoint_type': self.get_endpoint_type(raw.get('endpointConfiguration', {}).get('types')),
                    'resources': list(map(lambda _resource_raw: self.set_rest_api_resource(_resource_raw),
                                          _res.get('items', []))),
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.rest_service_name, region=region_name,
                                             account_id="", resource_type='restapis',
                                             resource_id=f"{raw.get('id')}/*"),
                    'tags': list(map(lambda tag: Tags(tag, strict=False),
                                     self.convert_tags(raw.get('tags', {}))))
                })

                yield RestAPI(raw, strict=False)

    def request_websocket_data(self, region_name) -> List[HTTPWebsocket]:
        # Get HTTP or WebSocket
        websocket_client = self.set_client(self.websocket_service_name)

        paginator = websocket_client.get_paginator('get_apis')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Items', []):
                raw.update({
                    'protocol': raw.get('ProtocolType'),
                    'endpoint_type': 'Regional',
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.websocket_service_name, region=region_name,
                                             account_id="", resource_type='api',
                                             resource_id=raw.get('ApiId')),
                    'tags': self.convert_tags(raw.get('tags', {}))
                })

                yield HTTPWebsocket(raw, strict=False)

    def set_rest_api_resource(self, resource):
        resource.update({
            'display_methods': self.get_methods_in_resources(resource.get('resourceMethods', {}))
        })
        return Resource(resource, strict=False)

    @staticmethod
    def get_methods_in_resources(resource_methods):
        return list(map(lambda method: method, resource_methods))

    @staticmethod
    def get_endpoint_type(endpoint_types):
        if endpoint_types:
            return endpoint_types[0]
        else:
            return ''
