from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_rest_api = CloudServiceTypeResource()
cst_rest_api.name = 'RestAPI'
cst_rest_api.provider = 'aws'
cst_rest_api.group = 'APIGateway'
cst_rest_api.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-API-Gateway.svg',
    'spaceone:is_major': 'true',
}

cst_rest_api._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.id'),
        TextDyField.data_source('Name', 'data.name'),
        ListDyField.data_source('Endpoint Type', 'data.endpoint_configuration.types', default_badge={'type': 'outline'}),
        TextDyField.data_source('Description', 'data.description')
    ],
    search=[
        SearchField.set(name='Rest API ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='API Key Source', key='data.api_key_source'),
        SearchField.set(name='Creation Time', key='data.created_date', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_web_socket = CloudServiceTypeResource()
cst_web_socket.name = 'HTTPWebsocket'
cst_web_socket.provider = 'aws'
cst_web_socket.group = 'APIGateway'
cst_web_socket.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-API-Gateway.svg',
    'spaceone:is_major': 'true',
}

cst_web_socket._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.api_id'),
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Protocol', 'data.protocol_type'),
        TextDyField.data_source('Description', 'data.description'),
    ],
    search=[
        SearchField.set(name='API ID', key='data.api_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='API Endpoint', key='data.api_endpoint'),
        SearchField.set(name='Creation Time', key='data.created_date', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_rest_api}),
    CloudServiceTypeResponse({'resource': cst_web_socket}),
]
