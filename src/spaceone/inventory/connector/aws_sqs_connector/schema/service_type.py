from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_que = CloudServiceTypeResource()
cst_que.name = 'Queue'
cst_que.provider = 'aws'
cst_que.group = 'SQS'
cst_que.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-SQS.svg',
    'spaceone:is_major': 'true',
}

cst_que._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('name', 'data.name'),
    TextDyField.data_source('url', 'data.url'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_que}),
]
