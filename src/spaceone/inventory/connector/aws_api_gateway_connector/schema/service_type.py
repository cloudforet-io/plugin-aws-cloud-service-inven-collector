import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
count_by_region_widget_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_widget_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')
count_by_protocol_widget_conf = os.path.join(current_dir, 'widget/count_by_protocol.yaml')

cst_api = CloudServiceTypeResource()
cst_api.name = 'API'
cst_api.provider = 'aws'
cst_api.group = 'APIGateway'
cst_api.labels = ['Networking']
cst_api.is_primary = True
cst_api.is_major = True
cst_api.service_code = 'AmazonApiGateway'
cst_api.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-API-Gateway.svg',
}

cst_api._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.id'),
        TextDyField.data_source('Protocol', 'instance_type', default_outline_badge=['REST', 'WEBSOCKET', 'HTTP']),
        TextDyField.data_source('Endpoint Type', 'data.endpoint_type'),
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
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Protocol', key='instance_type'),
        SearchField.set(name='Endpoint Type', key='data.endpoint_type'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_protocol_widget_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_api}),
]
