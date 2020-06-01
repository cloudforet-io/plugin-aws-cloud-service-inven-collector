from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_secret = CloudServiceTypeResource()
cst_secret.name = 'Secret'
cst_secret.provider = 'aws'
cst_secret.group = 'SecretsManager'
cst_secret.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Secrets-Manager.svg',
    'spaceone:is_major': 'true',
}

cst_secret._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Description', 'data.description'),
    DateTimeDyField.data_source('Last Retrieved', 'data.last_accessed_date'),
])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_secret}),
]
