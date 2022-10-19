from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_api_gateway_connector.schema.data import RestAPI, HTTPWebsocket
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
REST API
'''
# TAB - BASE
rest_api_meta_base = ItemDynamicLayout.set_fields('REST API', fields=[
    TextDyField.data_source('ID', 'data.id'),
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('Protocol', 'data.protocol', default_outline_badge=['REST', 'WEBSOCKET', 'HTTP']),
    TextDyField.data_source('API Key Source', 'data.api_key_source'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Endpoint Type', 'data.endpoint_type'),
    DateTimeDyField.data_source('Creation Time', 'data.created_date')
])

# TAB - RESOURCE
rest_api_meta_resources = TableDynamicLayout.set_fields('Resources', 'data.resources', fields=[
    TextDyField.data_source('ID', 'id'),
    TextDyField.data_source('Parent ID', 'parent_id'),
    TextDyField.data_source('Path', 'path'),
    ListDyField.data_source('HTTP Methods', 'display_methods', default_badge={'type': 'inline'}),
])

rest_api_meta = CloudServiceMeta.set_layouts([rest_api_meta_base,
                                              rest_api_meta_resources])


'''
WEBSOCKET & HTTP
'''
# TAB - BASE
websocket_meta_base = ItemDynamicLayout.set_fields('HTTP & Web Socket', fields=[
    TextDyField.data_source('ID', 'data.id'),
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    BadgeDyField.data_source('Protocol Type', 'data.protocol_type'),
    TextDyField.data_source('Endpoint Type', 'data.endpoint_type'),
    TextDyField.data_source('Endpoint', 'data.api_endpoint'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('API Key Selection Expression', 'data.api_key_selection_expression'),
    TextDyField.data_source('Route Selection Expression', 'data.route_selection_expression'),
    DateTimeDyField.data_source('Creation Time', 'data.created_date')
])

websocket_meta = CloudServiceMeta.set_layouts([websocket_meta_base])


class APIGatewayResource(CloudServiceResource):
    cloud_service_group = StringType(default='APIGateway')


class RestAPIResource(APIGatewayResource):
    cloud_service_type = StringType(default='API')
    data = ModelType(RestAPI)
    _metadata = ModelType(CloudServiceMeta, default=rest_api_meta, serialized_name='metadata')


class HTTPWebsocketResource(APIGatewayResource):
    cloud_service_type = StringType(default='API')
    data = ModelType(HTTPWebsocket)
    _metadata = ModelType(CloudServiceMeta, default=websocket_meta, serialized_name='metadata')


class RestAPIResponse(CloudServiceResponse):
    resource = PolyModelType(RestAPIResource)


class HTTPWebsocketResponse(CloudServiceResponse):
    resource = PolyModelType(HTTPWebsocketResource)
