from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_api_gateway_connector.schema.data import RestAPI, HTTPWebsocket
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
REST API
'''
# TAB - BASE
rest_api_meta_base = ItemDynamicLayout.set_fields('REST API', fields=[
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Description', 'data.description'),
    ListDyField.data_source('Endpoint Type', 'data.endpoint_configuration.types', default_badge={'type': 'outline'})
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
    TextDyField.data_source('Id', 'data.api_id'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Endpoint', 'data.api_endpoint'),
    TextDyField.data_source('Description', 'data.description'),
    BadgeDyField.data_source('Protocol Type', 'data.protocol_type'),
])

websocket_meta = CloudServiceMeta.set_layouts([websocket_meta_base, ])


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
