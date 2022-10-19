from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_cloud_trail_connector.schema.data import Trail
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout

# TAB - BASE
meta_base = ItemDynamicLayout.set_fields('Trails', fields=[
    TextDyField.data_source('Trail Name', 'data.name'),
    TextDyField.data_source('Trail ARN', 'data.trail_arn'),
    TextDyField.data_source('Home Region', 'data.home_region'),
    EnumDyField.data_source('Multi-Region Trail', 'data.is_multi_region_trail', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Insight', 'data.has_insight_selectors', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Include Global Service Events', 'data.include_global_service_events', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Organization Trail', 'data.is_organization_trail', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('SNS Topic', 'data.sns_topic_name'),
    TextDyField.data_source('SNS Topic ARN', 'data.sns_topic_arn'),
    TextDyField.data_source('S3 Bucket', 'data.s3_bucket_name'),
    TextDyField.data_source('S3 Key Prefix', 'data.s3_key_prefix'),
    EnumDyField.data_source('Log file Validation Enabled', 'data.log_file_validation_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('CloudWatch Logs Log group', 'data.cloud_watch_logs_log_group_arn'),
    TextDyField.data_source('CloudWatch Logs Role ARN', 'data.cloud_watch_logs_role_arn'),
    TextDyField.data_source('KMS Key ID', 'data.kms_key_id'),
    EnumDyField.data_source('Custom Event Selector', 'data.has_custom_event_selectors', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

insight_table = ItemDynamicLayout.set_fields('Insight Selectors', fields=[
    TextDyField.data_source('Insight Events', 'data.insight_selectors.insight_type')
])

event_selector_table = SimpleTableDynamicLayout.set_fields('Event Selectors', 'data.event_selectors', fields=[
    EnumDyField.data_source('Read/Write Type', 'read_write_type',
                            default_outline_badge=['ReadOnly', 'WriteOnly', 'All']),
    EnumDyField.data_source('Include Management Events', 'include_management_events', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    })
])

metadata = CloudServiceMeta.set_layouts([meta_base, insight_table, event_selector_table])


class CloudTrailResource(CloudServiceResource):
    cloud_service_group = StringType(default='CloudTrail')


class TrailResource(CloudTrailResource):
    cloud_service_type = StringType(default='Trail')
    data = ModelType(Trail)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class TrailResponse(CloudServiceResponse):
    resource = PolyModelType(TrailResource)
