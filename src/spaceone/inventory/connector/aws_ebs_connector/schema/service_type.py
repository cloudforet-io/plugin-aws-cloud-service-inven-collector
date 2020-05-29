from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField, \
    DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_ebs = CloudServiceTypeResource()
cst_ebs.name = 'Volume'
cst_ebs.provider = 'aws'
cst_ebs.group = 'EBS'
cst_ebs.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Block-Store-EBS.svg',
    'spaceone:is_major': 'true',
}
cst_ebs._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Volume ID', 'data.volume_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['in-use'],
        'available': ['available'],
        'warning': ['deleting', 'creating'],
        'disable': ['deleted'],
        'alert': ['error']
    }),
    TextDyField.data_source('Size (GB)', 'data.size'),
    EnumDyField.data_source('Volume Type', 'data.volume_type',
                            default_outline_badge=['standard', 'io1', 'gp2', 'sc1', 'st1']),
    TextDyField.data_source('IOPS', 'data.iops'),
    TextDyField.data_source('From Snapshot', 'data.snapshot_id'),
    TextDyField.data_source('Availablity Zone', 'data.availability_zone'),
    DateTimeDyField.data_source('Created', 'data.create_time'),
])


cst_snapshot = CloudServiceTypeResource()
cst_snapshot.name = 'Snapshot'
cst_snapshot.provider = 'aws'
cst_snapshot.group = 'EBS'
cst_snapshot.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Block-Store-EBS.svg',
    'spaceone:is_major': 'false',
}
cst_snapshot._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Snapshot ID', 'data.snapshot_id'),
    TextDyField.data_source('Size (GB)', 'data.volume_size'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'safe': ['completed'],
        'warning': ['pending'],
        'alert': ['error']
    }),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Progress', 'data.progress'),
    EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Start Time', 'data.start_time'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ebs}),
    CloudServiceTypeResponse({'resource': cst_snapshot}),
]
