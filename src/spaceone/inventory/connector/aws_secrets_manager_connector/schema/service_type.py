import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')

cst_secret = CloudServiceTypeResource()
cst_secret.name = 'Secret'
cst_secret.provider = 'aws'
cst_secret.group = 'SecretsManager'
cst_secret.labels = ['Security']
cst_secret.is_primary = True
cst_secret.service_code = 'AWSSecretsManager'
cst_secret.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Secrets-Manager.svg',
}

cst_secret._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Description', 'data.description'),
        DateTimeDyField.data_source('Last Retrieved', 'data.last_accessed_date'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Rotation Enabled', 'data.rotation_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Rotation Lambda ARN', 'data.rotation_lambda_arn', options={
            'is_optional': True
        }),
        ListDyField.data_source('Rotation Rule: Automatically After Days', 'data.rotation_rules', options={
            'sub_key': 'automatically_after_days',
            'delimiter': '<br>',
            'is_optional': True
        }),
        DateTimeDyField.data_source('Last Rotated Date', 'data.last_rotated_date', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Last Changed Date', 'data.last_changed_date', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Last Accessed Date', 'data.last_accessed_date', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Last Deleted Date', 'data.deleted_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Owning Service', 'data.owning_service', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Last Changed Time', key='data.last_changed_date', data_type='datetime'),
        SearchField.set(name='Last Accessed Time', key='data.last_accessed_date', data_type='datetime'),
        SearchField.set(name='Rotation Enabled', key='data.rotation_enabled', data_type='boolean'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_secret}),
]
