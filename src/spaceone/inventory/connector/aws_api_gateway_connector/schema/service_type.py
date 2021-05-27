from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_api = CloudServiceTypeResource()
cst_api.name = 'API'
cst_api.provider = 'aws'
cst_api.group = 'APIGateway'
cst_api.labels = ['Networking']
cst_api.is_primary = True
cst_api.is_major = True
cst_api.service_code = 'AmazonApiGateway'
cst_api.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-API-Gateway.svg',
}

cst_api._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.id'),
        TextDyField.data_source('Name', 'data.name'),
        EnumDyField.data_source('Protocol', 'data.protocol', default_outline_badge=['REST', 'WEBSOCKET', 'HTTP']),
        TextDyField.data_source('Endpoint Type', 'data.endpoint_type'),
        DateTimeDyField.data_source('Creation Time', 'data.created_date'),
        # For Dynamic Table
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('API Key Source', 'data.api_key_source', options={
            'is_optional': True
        }),
        ListDyField.data_source('Resource Paths', 'data.resources.path', options={
            'is_optional': True,
            'delimiter': '<br>'
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Protocol', key='data.protocol'),
        SearchField.set(name='Endpoint Type', key='data.endpoint_type'),
        SearchField.set(name='AWS Account ID', key='data.account_id')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_api}),
]
