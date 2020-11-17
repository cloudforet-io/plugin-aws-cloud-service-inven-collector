from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_bucket = CloudServiceTypeResource()
cst_bucket.name = 'Bucket'
cst_bucket.provider = 'aws'
cst_bucket.group = 'S3'
cst_bucket.labels = ['Storage']
cst_bucket.is_primary = True
cst_bucket.is_major = True
cst_bucket.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-S3.svg',
}

cst_bucket._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Region', 'data.region_name'),
        EnumDyField.data_source('Public Access', 'data.public_access', default_badge={
            'indigo.500': ['Private'],
            'coral.600': ['Public']
        })
    ],
    search=[
        SearchField.set(name='Bucket Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bucket}),
]
