from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, BadgeItemDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_trail = CloudServiceTypeResource()
cst_trail.name = 'Trail'
cst_trail.provider = 'aws'
cst_trail.group = 'CloudTrail'
cst_trail.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudtrail.svg',
    'spaceone:is_major': 'true',
}

cst_trail._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Trail Name', 'data.name'),
    TextDyField.data_source('Home Region', 'data.home_region'),
    EnumDyField.data_source('Multi-Region Trail', 'data.is_multi_region_trail', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Insight', 'data.has_insight_selectors', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Organization Trail', 'data.is_organization_trail', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('S3 Bucket', 'data.s3_bucket_name'),
    TextDyField.data_source('Log file Prefix', 'data.s3_key_prefix'),
    TextDyField.data_source('CloudWatch Logs Log group', 'data.cloud_watch_logs_log_group_arn'),
])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_trail}),
]
