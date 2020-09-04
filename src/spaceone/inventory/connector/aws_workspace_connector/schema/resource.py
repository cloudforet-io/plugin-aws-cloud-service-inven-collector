from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_cloud_front_connector.schema.data import DistributionData
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

# meta data details
# base_detail = ItemDynamicView({'name': "Base Information"})
# base_detail.data_source = [
#     TextDyField.data_source('Id', 'data.id'),
#     TextDyField.data_source('ARN', 'data.arn'),
#     TextDyField.data_source('Status', 'data.status'),
#     TextDyField.data_source('Domain Name', 'data.domain_name'),
#     ListDyField.data_source('CNAME', 'data.alias_icp_recordals',
#                             view_option=ListViewOption({
#                                 'item': TextDyField(),
#                                 'sub_key': 'cname',
#                             })),
#     TextDyField.data_source('Origins quantity', 'data.distribution_config.origin_groups.quantity'),
#     TextDyField.data_source('Origin Groups quantity', 'data.distribution_config.origin_groups.quantity'),
#
# ]
#
# alias_icp_recordals = SimpleTableDynamicView({
#     'name': "Alias ICP Recordals",
#     'key_path': "data.alias_icp_recordals"
# })
# alias_icp_recordals.data_source = [
#     TextDyField.data_source('CNAME', 'cname'),
#     TextDyField.data_source('Status', 'icp_recordal_status'),
# ]
# metadata = BaseMetaData()
# metadata.details = [base_detail, alias_icp_recordals, ]
#
# # metadata sub_data
# origins = TableDynamicView({'name': 'Origins', 'key_path': 'data.distribution_config.origins.items'})
# origins.data_source = [
#     TextDyField.data_source('Id', 'id'),
#     TextDyField.data_source('DomainName', 'domain_name'),
#     TextDyField.data_source('OriginPath', 'origin_path'),
# ]
# origin_groups = TableDynamicView({'name': 'Origin Groups', 'key_path': 'data.distribution_config.origin_groups.items'})
# origin_groups.data_source = [
#     TextDyField.data_source('Id', 'id'),
#     ListDyField.data_source('Members', 'members.items',
#                             view_option=ListViewOption({
#                                 'item': TextDyField(),
#                                 'sub_key': 'cname',
#                             })),
# ]
#
# metadata.sub_data = [origins, origin_groups]

meta = CloudServiceMeta.set()


class CloudFrontResource(CloudServiceResource):
    cloud_service_group = StringType(default='CloudFront')


class DistributionResource(CloudFrontResource):
    cloud_service_type = StringType(default='Distribution')
    data = ModelType(DistributionData)
    cloud_service_meta = ModelType(CloudServiceMeta, default=meta)


class CloudFrontResponse(CloudServiceResponse):
    resource = PolyModelType(DistributionResource)
