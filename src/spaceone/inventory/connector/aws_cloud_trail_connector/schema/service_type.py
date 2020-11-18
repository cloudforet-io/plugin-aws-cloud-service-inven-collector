from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_trail = CloudServiceTypeResource()
cst_trail.name = 'Trail'
cst_trail.provider = 'aws'
cst_trail.group = 'CloudTrail'
cst_trail.labels = ['Management']
cst_trail.is_primary = True
cst_trail.service_code = 'AWSCloudTrail'
cst_trail.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudtrail.svg',
}

cst_trail._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.trail_arn'),
        SearchField.set(name='Home Region', key='data.home_region'),
        SearchField.set(name='Multi-Region Trail', key='data.is_multi_region_trail', data_type='boolean'),
        SearchField.set(name='S3 Bucket', key='data.s3_bucket_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_trail}),
]
