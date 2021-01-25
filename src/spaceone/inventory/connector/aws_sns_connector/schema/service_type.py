from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

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
        TextDyField.data_source('Name', 'data.name')
    ],
    search=[
        SearchField.set(name='Topic Name', key='data.name'),
        SearchField.set(name='Topic ARN', key='data.topic_arn'),
        SearchField.set(name='Subscription ARN', key='data.subscriptions.subscription_arn'),
        SearchField.set(name='Endpoint', key='data.subscriptions.endpoint'),
        SearchField.set(name='Protocol', key='data.subscriptions.protocol'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_topic}),
]
