from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SearchField, \
    SizeField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_filesystem = CloudServiceTypeResource()
cst_filesystem.name = 'FileSystem'
cst_filesystem.provider = 'aws'
cst_filesystem.group = 'EFS'
cst_filesystem.is_primary = True
cst_filesystem.is_major = True
cst_filesystem.labels = ['Storage']
cst_filesystem.service_code = 'AmazonEFS'
cst_filesystem.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-File-System_EFS.svg'
}

cst_filesystem._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        EnumDyField.data_source('State', 'data.life_cycle_state', default_state={
            'safe': ['available'],
            'warning': ['creating', 'updating', 'deleting'],
            'disable': ['deleted']
        }),
        SizeField.data_source('Metered Sizes', 'size'),
        TextDyField.data_source('Mount Targets', 'data.number_of_mount_targets'),

        TextDyField.data_source('ID', 'data.file_system_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Throughput Mode', 'data.throughput_mode', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Mode', 'data.performance_mode', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encrypted', 'data.encrypted', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ARN', 'data.kms_key_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Mount Target IDs', 'data.mount_targets', options={
            'sub_key': 'mount_target_id',
            'is_optional': True
        }),
        ListDyField.data_source('Mount Target IP', 'data.mount_targets', options={
            'sub_key': 'ip_address',
            'is_optional': True
        }),
        ListDyField.data_source('Mount Target State', 'data.mount_targets', options={
            'sub_key': 'life_cycle_state',
            'is_optional': True
        }),
        ListDyField.data_source('Mount Target AZ', 'data.mount_targets', options={
            'sub_key': 'availability_zone_name',
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='File System ID', key='data.file_system_id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='State', key='data.life_cycle_state',
                        enums={
                            'available': {'label': 'available', 'icon': {'color': 'green.500'}},
                            'creating': {'label': 'creating', 'icon': {'color': 'yellow.500'}},
                            'updating': {'label': 'updating', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'deleted', 'icon': {'color': 'gray.400'}},
                        }),
        SearchField.set(name='Metered Size (Bytes)', key='size', data_type='integer'),
        SearchField.set(name='Performance Mode', key='data.performance_mode',
                        enums={
                            'generalPurpose': {'label': 'General Purpose'},
                            'maxIO': {'label': 'Max IO'},
                        }),
        SearchField.set(name='Throughput Mode', key='data.throughput_mode',
                        enums={
                            'bursting': {'label': 'Bursting'},
                            'provisioned': {'label': 'Provisioned'},
                        }),
        SearchField.set(name='Mount Target ID', key='data.mount_targets.mount_target_id'),
        SearchField.set(name='Mount Target Counts', key='data.number_of_mount_targets', data_type='integer'),
        SearchField.set(name='IP Address', key='data.mount_targets.ip_address'),
        SearchField.set(name='Availability Zone', key='data.mount_targets.availability_zone_name'),
        SearchField.set(name='Subnet ID', key='data.mount_targets.subnet_id'),
        SearchField.set(name='Security Group ID', key='data.mount_targets.security_groups')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_filesystem}),
]
