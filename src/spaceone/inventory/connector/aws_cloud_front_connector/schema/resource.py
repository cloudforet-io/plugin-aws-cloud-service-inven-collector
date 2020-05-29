from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_cloud_front_connector.schema.data import DistributionData
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeItemDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

# TAB - BASE
meta_base = ItemDynamicLayout.set_fields('Distributions', fields=[
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('ARN', 'data.arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['Deployed'],
    }),
    TextDyField.data_source('Domain Name', 'data.domain_name'),
    ListDyField.data_source('CNAME', 'data.alias_icp_recordals', default_badge={
        'type': 'outline', 'sub_key': 'cname',
    }),
    TextDyField.data_source('Origins quantity', 'data.distribution_config.origin_groups.quantity'),
    TextDyField.data_source('Origin Groups quantity', 'data.distribution_config.origin_groups.quantity'),
])

alias_icp_recordals = SimpleTableDynamicLayout.set_fields('Alias ICP Recordals', 'data.alias_icp_recordals', fields=[
    TextDyField.data_source('CNAME', 'cname'),
    EnumDyField.data_source('Status', 'icp_recordal_status', default_state={
        'safe': ['APPROVED'],
        'alert': ['SUSPENDED'],
        'warning': ['PENDING']
    }),
])

origin = TableDynamicLayout.set_fields('Origins', 'data.distribution_config.origin_groups.items', fields=[
    TextDyField.data_source('Id', 'id'),
    TextDyField.data_source('DomainName', 'domain_name'),
    TextDyField.data_source('OriginPath', 'origin_path'),
])

origin_group = TableDynamicLayout.set_fields('Origin Groups', 'data.distribution_config.origin_groups.items', fields=[
    TextDyField.data_source('ID', 'id'),
    ListDyField.data_source('Members', 'members.items', default_badge={
        'type': 'outline',
        'sub_key': 'cname',
    })
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts([meta_base, alias_icp_recordals, origin, origin_group, tags])


class CloudFrontResource(CloudServiceResource):
    cloud_service_group = StringType(default='CloudFront')


class DistributionResource(CloudFrontResource):
    cloud_service_type = StringType(default='Distribution')
    data = ModelType(DistributionData)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class CloudFrontResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(DistributionResource)
