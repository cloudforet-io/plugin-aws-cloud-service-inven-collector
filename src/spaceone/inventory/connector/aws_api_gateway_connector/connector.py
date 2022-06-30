import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_api_gateway_connector.schema.data import RestAPI, Resource, HTTPWebsocket
from spaceone.inventory.connector.aws_api_gateway_connector.schema.resource import RestAPIResource, \
    HTTPWebsocketResource, RestAPIResponse, HTTPWebsocketResponse
from spaceone.inventory.connector.aws_api_gateway_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import AWSTags

_LOGGER = logging.getLogger(__name__)


# Collect REST API
class APIGatewayConnector(SchematicAWSConnector):
    rest_service_name = 'apigateway'
    websocket_service_name = 'apigatewayv2'
    cloud_service_group = 'APIGateway'
    cloud_service_type = 'API'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: API Gateway")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

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

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(collect_resource['service_name'],
                                                             region_name,
                                                             collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: API Gateway ({time.time() - start_time} sec)')
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
                try:
                    _res = self.client.get_resources(restApiId=raw.get('id'), limit=500)
                    # for avoid to API Rate limitation.
                    time.sleep(0.5)

                    raw.update({
                        'protocol': 'REST',
                        'endpoint_type': self.get_endpoint_type(raw.get('endpointConfiguration', {}).get('types')),
                        'resources': list(map(lambda _resource_raw: self.set_rest_api_resource(_resource_raw),
                                              _res.get('items', []))),
                        'arn': self.generate_arn(service=self.rest_service_name, region=region_name,
                                                 account_id="", resource_type='restapis',
                                                 resource_id=f"{raw.get('id')}/*"),
                        'tags': list(map(lambda tag: AWSTags(tag, strict=False),
                                         self.convert_tags(raw.get('tags', {})))),
                        'cloudtrail': self.set_cloudtrail(region_name, raw['id'])
                    })
    
                    rest_api_vo = RestAPI(raw, strict=False)
                    yield {
                        'data': rest_api_vo,
                        'name': rest_api_vo.name,
                        'instance_type': rest_api_vo.protocol,
                        'account': self.account_id,
                        'launched_at': self.datetime_to_iso8601(rest_api_vo.created_date)
                    }

                except Exception as e:
                    resource_id = raw.get('id', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}
            
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
                try:
                    raw.update({
                        'protocol': raw.get('ProtocolType'),
                        'endpoint_type': 'Regional',
                        'arn': self.generate_arn(service=self.websocket_service_name, region=region_name,
                                                 account_id="", resource_type='api',
                                                 resource_id=raw.get('ApiId')),
                        'tags': self.convert_tags(raw.get('tags', {})),
                        'cloudtrail': self.set_cloudtrail(region_name, raw['ApiId'])
                    })
    
                    http_websocket_vo = HTTPWebsocket(raw, strict=False)
                    yield {
                        'data': http_websocket_vo,
                        'name': http_websocket_vo.name,
                        'instance_type': http_websocket_vo.protocol,
                        'account': self.account_id,
                        'launched_at': self.datetime_to_iso8601(http_websocket_vo.created_date)
                    }

                except Exception as e:
                    resource_id = raw.get('ApiId', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

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
