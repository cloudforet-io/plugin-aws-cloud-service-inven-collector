import time
import logging
from typing import List

from spaceone.inventory.connector.aws_api_gateway_connector.schema.data import RestAPI, Resource, HTTPWebsocket
from spaceone.inventory.connector.aws_api_gateway_connector.schema.resource import RestAPIResource, \
    HTTPWebsocketResource, RestAPIResponse, HTTPWebsocketResponse
from spaceone.inventory.connector.aws_api_gateway_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


# Collect REST API
class APIGatewayConnector(SchematicAWSConnector):
    response_schema = RestAPIResponse
    service_name = 'apigateway'

    def get_resources(self):
        print("** API Gateway START **")
        resources = []
        start_time = time.time()

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ APIGateway {region_name} ]')
            self.reset_region(region_name)

            for data in self.request_data(region_name):
                resources.append(self.response_schema(
                    {'resource': RestAPIResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

        print(f' API Gateway Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[RestAPI]:
        paginator = self.client.get_paginator('get_rest_apis')
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
                    'resources': list(map(lambda _resource_raw: self.set_rest_api_resource(_resource_raw),
                                          _res.get('items', []))),
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.service_name, region=region_name,
                                             account_id="", resource_type='restapis',
                                             resource_id=f"{raw.get('id')}/*")
                })

                yield RestAPI(raw, strict=False)

    def set_rest_api_resource(self, resource):
        resource.update({
            'display_methods': self.get_methods_in_resources(resource.get('resourceMethods', {}))
        })
        return Resource(resource, strict=False)

    @staticmethod
    def get_methods_in_resources(resource_methods):
        return list(map(lambda method: method, resource_methods))


# Collect HTTP or WebSocket
class APIGatewayV2Connector(SchematicAWSConnector):
    response_schema = HTTPWebsocketResponse
    service_name = 'apigatewayv2'

    def get_resources(self):
        resources = []
        print("** API Gateway V2 START **")
        start_time = time.time()

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ APIGatewayV2 {region_name} ]')
            self.reset_region(region_name)

            for data in self.request_data(region_name):
                resources.append(self.response_schema(
                    {'resource': HTTPWebsocketResource({'data': data,
                                                        'reference': ReferenceModel(data.reference)})}))

        print(f' API Gateway V2 Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[HTTPWebsocket]:
        paginator = self.client.get_paginator('get_apis')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('Items', []):
                raw.update({
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.service_name, region=region_name,
                                             account_id="", resource_type='api',
                                             resource_id=raw.get('api_id'))
                })
                yield HTTPWebsocket(raw, strict=False)
