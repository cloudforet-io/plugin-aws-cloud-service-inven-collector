import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField, SizeField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

object_total_count_conf = os.path.join(current_dir, 'widget/object_total_count.yaml')
object_total_size_conf = os.path.join(current_dir, 'widget/object_total_size.yaml')
bucket_count_per_region_conf = os.path.join(current_dir, 'widget/bucket_count_per_region.yaml')
object_count_per_region_conf = os.path.join(current_dir, 'widget/object_count_per_region.yaml')
object_total_size_per_region_conf = os.path.join(current_dir, 'widget/object_total_size_per_region.yaml')
bucket_count_per_account_conf = os.path.join(current_dir, 'widget/bucket_count_per_account.yaml')
object_count_per_account_conf = os.path.join(current_dir, 'widget/object_count_per_account.yaml')
object_total_size_per_account_conf = os.path.join(current_dir, 'widget/object_total_size_per_account.yaml')

cst_bucket = CloudServiceTypeResource()
cst_bucket.name = 'Bucket'
cst_bucket.provider = 'aws'
cst_bucket.group = 'S3'
cst_bucket.labels = ['Storage']
cst_bucket.is_primary = True
cst_bucket.is_major = True
cst_bucket.service_code = 'AmazonS3'
cst_bucket.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-S3.svg',
}

cst_bucket._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        EnumDyField.data_source('Access', 'data.public_access', default_badge={
            'indigo.500': ['Private'],
            'coral.600': ['Public']
        }),
        TextDyField.data_source('Object Total Counts', 'data.object_count'),
        SizeField.data_source('Object Total Size', 'instance_size'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Versioning Status', 'data.versioning.status', options={
            'is_optional': True
        }),
        TextDyField.data_source('Webhosting Index Document', 'data.website_hosting.index_document', options={
            'is_optional': True
        }),
        TextDyField.data_source('Webhosting Error Document', 'data.website_hosting.error_document', options={
            'is_optional': True
        }),
        TextDyField.data_source('Webhosting Error Document', 'data.website_hosting.routing_rules', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Logging Target Bucket', 'data.server_access_logging.target_bucket', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Logging Target Prefix', 'data.server_access_logging.target_prefix', options={
            'is_optional': True
        }),
        ListDyField.data_source('Webhosting Routing Rules Condition', 'data.website_hosting.routing_rules', options={
            'sub_key': 'condition',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('Object Lock Enabled', 'data.object_lock.object_lock_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Transfer Acceleration Enabled', 'data.transfer_acceleration.transfer_acceleration',
                                options={'is_optional': True}),
        ListDyField.data_source('Notification Type', 'data.notification_configurations', options={
            'sub_key': 'notification_type',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Notification ID', 'data.notification_configurations', options={
            'sub_key': 'id',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Notification ARN', 'data.notification_configurations', options={
            'sub_key': 'arn',
            'delimiter': '<br>',
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Bucket Name', key='name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Object Counts', key='data.object_count', data_type='integer'),
        SearchField.set(name='Object Total Size (Bytes)', key='instance_size', data_type='integer')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(object_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(object_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(bucket_count_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(object_count_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(object_total_size_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(bucket_count_per_account_conf)),
        ChartWidget.set(**get_data_from_yaml(object_count_per_account_conf)),
        ChartWidget.set(**get_data_from_yaml(object_total_size_per_account_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bucket}),
]
