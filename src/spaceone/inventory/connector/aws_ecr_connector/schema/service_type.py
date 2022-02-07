import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
image_total_count_conf = os.path.join(current_dir, 'widget/image_total_count.yaml')
image_total_size_conf = os.path.join(current_dir, 'widget/image_total_size.yaml')
repository_count_by_region_conf = os.path.join(current_dir, 'widget/repository_count_by_region.yaml')
repository_count_by_account_conf = os.path.join(current_dir, 'widget/repository_count_by_account.yaml')
image_total_size_by_repository_conf = os.path.join(current_dir, 'widget/image_total_size_by_repository.yaml')

cst_ecr_repo = CloudServiceTypeResource()
cst_ecr_repo.name = 'Repository'
cst_ecr_repo.provider = 'aws'
cst_ecr_repo.group = 'ECR'
cst_ecr_repo.labels = ['Container', 'Compute']
cst_ecr_repo.is_primary = True
cst_ecr_repo.service_code = 'AmazonECR'
cst_ecr_repo.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Container-Registry.svg',
}

cst_ecr_repo._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Repository name', 'name'),
        TextDyField.data_source('URI', 'data.repository_uri'),
        TextDyField.data_source('Registry ARN ', 'data.repository_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Image Tag Mutability ', 'data.image_tag_mutability', options={
            'is_optional': True
        }),
        TextDyField.data_source('Image Scanning on Push ', 'data.image_scanning_configuration.scan_on_push', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Repository ID', key='data.registry_id'),
        SearchField.set(name='Name', key='name'),
        SearchField.set(name='ARN', key='data.repository_arn'),
        SearchField.set(name='URI', key='data.repository_uri'),
        SearchField.set(name='Image URI', key='data.images.image_uri')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(image_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(image_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(repository_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(repository_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(image_total_size_by_repository_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecr_repo}),
]
