from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_sqs_connector.schema.data import QueData
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

sqs = ItemDynamicLayout.set_fields('Queue', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('URL', 'data.url'),
    EnumDyField.data_source('FIFO Queue', 'data.fifo_queue', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Content Based Deduplication', 'data.content_based_duplication', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Approximate Number Of Messages', 'data.approximate_number_of_messages'),
    TextDyField.data_source('Approximate Number Of Messages Delayed', 'data.approximate_number_of_messages_delayed'),
    TextDyField.data_source('Approximate Number Of Messages Not Visible', 'data.approximate_number_of_messages_not_visible'),
    TextDyField.data_source('Delay Seconds', 'data.delay_seconds'),
    TextDyField.data_source('Maximum Message Size', 'data.maximum_message_size'),
    TextDyField.data_source('Message Retention Period', 'data.message_retention_period'),
    TextDyField.data_source('Receive Message Wait Time Seconds', 'data.receive_message_wait_time_seconds'),
    TextDyField.data_source('Visibility Timeout', 'data.visibility_timeout'),
    DateTimeDyField.data_source('Created Time', 'data.created_timestamp', options={
        'source_type': 'timestamp',
        'source_format': 'seconds'
    }),
    DateTimeDyField.data_source('Last Modified Time', 'data.last_modified_timestamp', options={
        'source_type': 'timestamp',
        'source_format': 'seconds'
    }),
])

metadata = CloudServiceMeta.set_layouts(layouts=[sqs])


class SQSResource(CloudServiceResource):
    cloud_service_group = StringType(default='SQS')


class QueResource(SQSResource):
    cloud_service_type = StringType(default='Queue')
    data = ModelType(QueData)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class SQSResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(QueResource)
