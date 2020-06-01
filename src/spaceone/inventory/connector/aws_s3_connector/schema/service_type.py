from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_bucket = CloudServiceTypeResource()
cst_bucket.name = 'Bucket'
cst_bucket.provider = 'aws'
cst_bucket.group = 'S3'
cst_bucket.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-S3.svg',
    'spaceone:is_major': 'true',
}

cst_bucket._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Region', 'data.region_name'),
    TextDyField.data_source('Access', 'data.access'),
    TextDyField.data_source('Object Count', 'data.object_count'),
    TextDyField.data_source('Total Size', 'data.object_total_size'),
])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bucket}),
]
