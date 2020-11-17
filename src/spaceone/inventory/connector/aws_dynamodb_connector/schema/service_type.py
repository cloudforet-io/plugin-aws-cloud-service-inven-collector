from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_table = CloudServiceTypeResource()
cst_table.name = 'Table'
cst_table.provider = 'aws'
cst_table.group = 'DynamoDB'
cst_table.labels = ['Database']
cst_table.is_primary = True
cst_table.is_major = True
cst_table.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DynamoDB.svg',
}
cst_table._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
    ],
    search=[
        SearchField.set(name='Table Name', key='data.table_name'),
        SearchField.set(name='Table ARN', key='data.table_arn'),
        SearchField.set(name='Table Status', key='data.table_status',
                        enums={
                            'ACTIVE': {'label': 'ACTIVE', 'icon': {'color': 'green.500'}},
                            'CREATING': {'label': 'CREATING', 'icon': {'color': 'yellow.500'}},
                            'UPDATING': {'label': 'UPDATING', 'icon': {'color': 'yellow.500'}},
                            'DELETING': {'label': 'DELETING', 'icon': {'color': 'yellow.500'}},
                            'ARCHIVING': {'label': 'ARCHIVING', 'icon': {'color': 'yellow.500'}},
                            'INACCESSIBLE_ENCRYPTION_CREDENTIALS': {'label': 'INACCESSIBLE_ENCRYPTION_CREDENTIALS',
                                                                    'icon': {'color': 'red.500'}},
                            'ARCHIVED': {'label': 'ARCHIVED', 'icon': {'color': 'red.500'}}
                        }),
        SearchField.set(name='Storage Size', key='data.table_size_bytes', data_type='integer'),
        SearchField.set(name='Item Count', key='data.item_count', data_type='integer'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_table}),
]
