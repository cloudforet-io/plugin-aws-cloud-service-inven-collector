from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_que = CloudServiceTypeResource()
cst_que.name = 'Queue'
cst_que.provider = 'aws'
cst_que.group = 'SQS'
cst_que.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-SQS.svg',
    'spaceone:is_major': 'true',
}

cst_que._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('name', 'data.name'),
        TextDyField.data_source('url', 'data.url'),
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='URL', key='data.url'),
        SearchField.set(name='Maximum Message Size', key='data.maximum_message_size', data_type='integer'),
        SearchField.set(name='Approximate Number of Messages', key='data.approximate_number_of_messages',
                        data_type='integer'),
        SearchField.set(name='Created Time', key='data.created_timestamp', data_type='datetime'),
        SearchField.set(name='Last Modified Time', key='data.last_modified_timestamp', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_que}),
]
