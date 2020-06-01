from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_ecr_repo = CloudServiceTypeResource()
cst_ecr_repo.name = 'Repository'
cst_ecr_repo.provider = 'aws'
cst_ecr_repo.group = 'ECR'
cst_ecr_repo.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Container-Registry.svg',
    'spaceone:is_major': 'true',
}

cst_ecr_repo._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Repository name', 'data.repository_name'),
    TextDyField.data_source('URI', 'data.repository_uri'),
    DateTimeDyField.data_source('Created', 'data.created_at'),

])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecr_repo}),
]
