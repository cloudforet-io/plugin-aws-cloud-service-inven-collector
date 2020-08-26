from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_secret = CloudServiceTypeResource()
cst_secret.name = 'Secret'
cst_secret.provider = 'aws'
cst_secret.group = 'SecretsManager'
cst_secret.labels = ['Security']
cst_secret.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Secrets-Manager.svg',
    'spaceone:is_major': 'true',
}

cst_secret._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Description', 'data.description'),
        DateTimeDyField.data_source('Last Retrieved', 'data.last_accessed_date'),
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Last Changed Time', key='data.last_changed_date', data_type='datetime'),
        SearchField.set(name='Last Accessed Time', key='data.last_accessed_date', data_type='datetime'),
        SearchField.set(name='Rotation Enabled', key='data.rotation_enabled', data_type='boolean'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_secret}),
]
