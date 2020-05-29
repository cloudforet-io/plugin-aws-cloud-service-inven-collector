from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_table = CloudServiceTypeResource()
cst_table.name = 'Table'
cst_table.provider = 'aws'
cst_table.group = 'DynamoDB'
cst_table.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DynamoDB.svg',
    'spaceone:is_major': 'true',
}
cst_table._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.table_name'),
    EnumDyField.data_source('Status', 'data.table_status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'UPDATING', 'DELETING', 'ARCHIVING'],
        'alert': ['INACCESSIBLE_ENCRYPTION_CREDENTIALS', 'ARCHIVED']
    }),
    TextDyField.data_source('Partition Key', 'data.partition_key_display'),
    TextDyField.data_source('Sort Key', 'data.sort_key_display'),
    TextDyField.data_source('Indexes', 'data.index_count'),
    TextDyField.data_source('Total read capacity', 'data.total_read_capacity'),
    TextDyField.data_source('Total write capacity', 'data.total_write_capacity'),
    ListDyField.data_source('Auto Scaling', 'data.auto_scaling_policies', default_badge={'type': 'outline'}),
])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_table}),
]
