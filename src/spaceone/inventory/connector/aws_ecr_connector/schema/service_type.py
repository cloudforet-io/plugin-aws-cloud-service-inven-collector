from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_ecr_repo = CloudServiceTypeResource()
cst_ecr_repo.name = 'Repository'
cst_ecr_repo.provider = 'aws'
cst_ecr_repo.group = 'ECR'
cst_ecr_repo.labels = ['Container']
cst_ecr_repo.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Container-Registry.svg',
    'spaceone:is_major': 'true',
}

cst_ecr_repo._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Repository name', 'data.repository_name'),
        TextDyField.data_source('URI', 'data.repository_uri'),
        DateTimeDyField.data_source('Created', 'data.created_at'),
    ],
    search=[
        SearchField.set(name='Repository ID', key='data.registry_id'),
        SearchField.set(name='Name', key='data.repository_name'),
        SearchField.set(name='ARN', key='data.repository_arn'),
        SearchField.set(name='URI', key='data.repository_uri'),
        SearchField.set(name='Image URI', key='data.images.image_uri'),
        SearchField.set(name='Created Time', key='data.created_at', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecr_repo}),
]
