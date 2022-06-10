import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

topic_total_count_conf = os.path.join(current_dir, 'widget/topic_total_count.yaml')
subscription_total_count_conf = os.path.join(current_dir, 'widget/subscription_total_count.yaml')
topic_count_by_region_conf = os.path.join(current_dir, 'widget/topic_count_by_region.yaml')
topic_count_by_account_conf = os.path.join(current_dir, 'widget/topic_count_by_account.yaml')
subscription_count_by_account_conf = os.path.join(current_dir, 'widget/subscription_count_by_account.yaml')

cst_topic = CloudServiceTypeResource()
cst_topic.name = 'Topic'
cst_topic.provider = 'aws'
cst_topic.group = 'SNS'
cst_topic.labels = ['Application Integration']
cst_topic.is_primary = True
cst_topic.service_code = 'AmazonSNS'
cst_topic.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-SNS.svg',
}

cst_topic._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ARN', 'data.topic_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Display Name', 'data.display_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subscription Confirmed', 'data.subscription_confirmed', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subscription Pending', 'data.subscriptions_pending', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subscription Deleted', 'data.subscription_deleted', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS ID', 'data.kms.kms_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS ARN', 'data.kms.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Alias', 'data.kms.alias', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Topic ARN', key='data.topic_arn'),
        SearchField.set(name='Subscription ARN', key='data.subscriptions.subscription_arn'),
        SearchField.set(name='Endpoint', key='data.subscriptions.endpoint'),
        SearchField.set(name='Protocol', key='data.subscriptions.protocol')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(topic_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(subscription_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(topic_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(topic_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(subscription_count_by_account_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_topic}),
]
