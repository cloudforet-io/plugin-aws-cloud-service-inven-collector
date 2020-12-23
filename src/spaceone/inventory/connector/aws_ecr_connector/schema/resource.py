from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_ecr_connector.schema.data import Repository
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

base = ItemDynamicLayout.set_fields('Repositories', fields=[
    TextDyField.data_source('Repository ID', 'data.registry_id'),
    TextDyField.data_source('Repository name', 'data.repository_name'),
    TextDyField.data_source('Repository ARN', 'data.repository_arn'),
    TextDyField.data_source('URI', 'data.repository_uri'),
    TextDyField.data_source('Created', 'data.created_at'),
    EnumDyField.data_source('Tag Immutability', 'data.image_tag_mutability', default_badge={
        'indigo.500': ['MUTABLE'], 'coral.600': ['IMMUTABLE']
    }),
    EnumDyField.data_source('Scan On Push', 'data.image_scanning_configuration.scan_on_push', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

images = TableDynamicLayout.set_fields('Images', 'data.images', fields=[
    ListDyField.data_source('Image Tag', 'image_tags_display', options={
        'delimiter': ', '
    }),
    TextDyField.data_source('Image URI', 'image_uri'),
    SizeField.data_source('Image Size', 'image_size_in_bytes'),
    TextDyField.data_source('Digest', 'image_digest'),
    EnumDyField.data_source('Scan status', 'image_scan_status.status', default_state={
        'safe': ['COMPLETE'],
        'warning': ['IN_PROGRESS'],
        'alert': ['FAILED']
    }),
    DateTimeDyField.data_source('Pushed at', 'image_pushed_at'),
])

metadata = CloudServiceMeta.set_layouts(layouts=[base, images])


class ECRResource(CloudServiceResource):
    cloud_service_group = StringType(default='ECR')


class ECRRepositoryResource(ECRResource):
    cloud_service_type = StringType(default='Repository')
    data = ModelType(Repository)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class ECRResponse(CloudServiceResponse):
    resource = PolyModelType(ECRRepositoryResource)
