from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_kms_cluster = CloudServiceTypeResource()
cst_kms_cluster.name = 'Key'
cst_kms_cluster.provider = 'aws'
cst_kms_cluster.group = 'KMS'
cst_kms_cluster.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Key-Management-Service.svg',
    'spaceone:is_major': 'true',
}

cst_kms_cluster._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('ID', 'data.key_id'),
    TextDyField.data_source('Alias', 'data.alias_name'),
    EnumDyField.data_source('Status', 'data.key_state', default_state={
        'safe': ['Enabled'],
        'warning': ['PendingDeletion', 'PendingImport'],
        'disable': ['Disabled'],
        'alert': ['Unavailable']
    }),
    EnumDyField.data_source('Enabled', 'data.enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    })
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_kms_cluster}),
]
