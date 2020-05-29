from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_filesystem = CloudServiceTypeResource()
cst_filesystem.name = 'FileSystem'
cst_filesystem.provider = 'aws'
cst_filesystem.group = 'EFS'
cst_filesystem.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-File-System_EFS.svg',
    'spaceone:is_major': 'true',
}

cst_filesystem._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('ID', 'data.file_system_id'),
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('State', 'data.life_cycle_state', default_state={
        'safe': ['available'],
        'warning': ['creating', 'updating', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Metered Sizes (Bytes)', 'data.size_in_bytes.value'),
    TextDyField.data_source('Mount Targets', 'data.number_of_mount_targets'),
    DateTimeDyField.data_source('Creation date', 'data.creation_time'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_filesystem}),
]
