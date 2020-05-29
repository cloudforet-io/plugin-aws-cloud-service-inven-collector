from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_dynamodb_connector.schema.data import Table
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout

tables = ItemDynamicLayout.set_fields('Tables', fields=[
    TextDyField.data_source('Table Name', 'data.table_name'),
    TextDyField.data_source('ARN', 'data.table_arn'),
    EnumDyField.data_source('Status', 'data.table_status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'UPDATING', 'DELETING', 'ARCHIVING'],
        'alert': ['INACCESSIBLE_ENCRYPTION_CREDENTIALS', 'ARCHIVED']
    }),
    TextDyField.data_source('Partition Key', 'data.partition_key_display'),
    TextDyField.data_source('Primary Sort Key', 'data.sort_key_display'),
    EnumDyField.data_source('Point-in-time Recovery',
                            'data.continuous_backup.point_in_time_recovery_description.point_in_time_recovery_status',
                            default_state={
                                'safe': ['ENABLED'], 'disable': ['DISABLED']
                            }),
    EnumDyField.data_source('CloudWatch Contributor Insights', 'data.contributor_insight.contributor_insights_status',
                            default_state={
                                'safe': ['ENABLED'],
                                'warninig': ['ENABLING', 'DISABLING'],
                                'alert': ['FAILED'],
                                'disable': ['DISABLED']
                            }),
    TextDyField.data_source('Storage Size (in bytes)', 'data.table_size_bytes'),
    TextDyField.data_source('Item count', 'data.item_count'),
    TextDyField.data_source('Region', 'data.region_name'),
    DateTimeDyField.data_source('Creation date', 'data.creation_date_time'),
])

capacity = ItemDynamicLayout.set_fields('Capacity', fields=[
    EnumDyField.data_source('Read/write capacity mode', 'data.billing_mode_summary.billing_mode', default_badge={
        'indigo.500': ['PROVISIONED'], 'coral.600': ['PAY_PER_REQUEST']
    }),
    DateTimeDyField.data_source('Last change to on-demand mode',
                                'data.billing_mode_summary.last_update_to_pay_per_request_date_time'),
    TextDyField.data_source('Provisioned Read capacity units', 'data.provisioned_throughput.read_capacity_units'),
    TextDyField.data_source('Provisioned Write capacity units', 'data.provisioned_throughput.write_capacity_units'),
    DateTimeDyField.data_source('Last Increase Date Time', 'data.provisioned_throughput.last_increase_date_time'),
    DateTimeDyField.data_source('Last Decrease Date Time', 'data.provisioned_throughput.last_decrease_date_time'),
])

encryption = ItemDynamicLayout.set_fields('Encryptions', fields=[
    BadgeDyField.data_source('Encryption Type', 'data.encryption_type'),
    EnumDyField.data_source('Encryption Status', 'data.sse_description.status', default_state={
        'safe': ['ENABLED'],
        'disable': ['DISABLED'],
        'warning': ['ENABLING', 'UPDATING', 'DISABLING']
    }),
    TextDyField.data_source('KMS Master Key ARN', 'data.sse_description.kms_master_key_arn'),
])

ttl = ItemDynamicLayout.set_fields('TTL Attributes', fields=[
    EnumDyField.data_source('Status', 'data.time_to_live.time_to_live_status', default_state={
        'safe': ['ENABLED'],
        'warning': ['ENABLING', 'DISABLING'],
        'disable': ['DISABLED']
    }),
    TextDyField.data_source('Attribute', 'data.time_to_live.attribute_name'),
])

contributor_insights = ItemDynamicLayout.set_fields('CloudWatch Contributor Insights', fields=[
    EnumDyField.data_source('Status', 'data.contributor_insight.contributor_insights_status', default_state={
        'safe': ['ENABLED'],
        'warning': ['ENABLING', 'DISABLING'],
        'disable': ['DISABLED'],
        'alert': ['FAILED']
    }),
    ListDyField.data_source('Rule List', 'data.contributor_insight.contributor_insights_rule_list',
                            default_badge={'type': 'outline'}),
])

metadata = CloudServiceMeta.set_layouts(layouts=[tables, capacity, encryption, ttl, contributor_insights])


class DynamoDBResource(CloudServiceResource):
    cloud_service_group = StringType(default='DynamoDB')


class TableResource(DynamoDBResource):
    cloud_service_type = StringType(default='Table')
    data = ModelType(Table)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class TableResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.table_arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(TableResource)
