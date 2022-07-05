from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

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
        TextDyField.data_source('Home Region', 'data.home_region'),
        TextDyField.data_source('Multi-Region Trail', 'data.is_multi_region_trail'),
        TextDyField.data_source('Insight', 'data.has_insight_selectors'),
        TextDyField.data_source('Organization Trail', 'data.is_organization_trail'),
        TextDyField.data_source('S3 Bucket', 'data.s3_bucket_name'),
        TextDyField.data_source('Log file Prefix', 'data.s3_key_prefix'),
        # For Dynamic Table
        TextDyField.data_source('Trail ARN', 'data.trail_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Log file Validation Enabled', 'data.log_file_validation_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('CloudWatch Logs Log group', 'data.cloud_watch_logs_log_group_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('SNS Topic name', 'data.sns_topic_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('SNS Topic ARN', 'data.sns_topic_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Include Global Service Events', 'data.include_global_service_events', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='ARN', key='data.trail_arn'),
        SearchField.set(name='Home Region', key='data.home_region'),
        SearchField.set(name='Multi-Region Trail', key='data.is_multi_region_trail', data_type='boolean'),
        SearchField.set(name='S3 Bucket', key='data.s3_bucket_name'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_trail}),
]
