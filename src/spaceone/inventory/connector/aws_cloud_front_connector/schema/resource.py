from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_cloud_front_connector.schema.data import DistributionData
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeItemDyField, BadgeDyField, \
    EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

# TAB - BASE
meta_base = ItemDynamicLayout.set_fields('Distributions', fields=[
    TextDyField.data_source('Distribution ID', 'data.id'),
    TextDyField.data_source('ARN', 'data.arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['Deployed'],
    }),
    TextDyField.data_source('Domain Name', 'data.domain_name'),
    TextDyField.data_source('HTTP Version', 'data.http_version'),
    TextDyField.data_source('Comment', 'data.comment'),
    TextDyField.data_source('Price Class', 'data.price_class'),
    TextDyField.data_source('AWS Web ACL', 'data.web_acl_id'),
    EnumDyField.data_source('State Enabled', 'data.enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    ListDyField.data_source('CNAME', 'data.alias_icp_recordals', options={
        'sub_key': 'cname', 'delimiter': '<br>'
    }),
    TextDyField.data_source('Domain Name', 'data.domain_name'),
    TextDyField.data_source('Custom SSL Client Support', 'data.viewer_certificate.ssl_support_method'),
    TextDyField.data_source('Security Policy', 'data.viewer_certificate.minimum_protocol_version'),
    EnumDyField.data_source('IPv6 Support', 'data.is_ipv6_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Last Modified', 'data.last_modified_time')
])

alias_icp_recordals = SimpleTableDynamicLayout.set_fields('Alias ICP Recordals', 'data.alias_icp_recordals', fields=[
    TextDyField.data_source('CNAME', 'cname'),
    EnumDyField.data_source('Status', 'icp_recordal_status', default_state={
        'safe': ['APPROVED'],
        'alert': ['SUSPENDED'],
        'warning': ['PENDING']
    }),
])

origin = TableDynamicLayout.set_fields('Origins', 'data.origins.items', fields=[
    TextDyField.data_source('Id', 'id'),
    TextDyField.data_source('DomainName', 'domain_name'),
    TextDyField.data_source('OriginPath', 'origin_path'),
    TextDyField.data_source('Origin Shield Region', 'origin_shield.origin_shield_region'),
    TextDyField.data_source('Origin Protocol Policy', 'custom_origin_config.origin_protocol_policy'),
    TextDyField.data_source('HTTPS Port', 'custom_origin_config.https_port'),
    TextDyField.data_source('HTTP Port', 'custom_origin_config.http_port'),
    TextDyField.data_source('Origin Response Timeout', 'custom_origin_config.origin_read_timeout'),
    TextDyField.data_source('Origin Keep-alive Tiemout', 'custom_origin_config.origin_keepalive_timeout'),
    TextDyField.data_source('Origin Connection Attempts', 'connection_attempts'),
    TextDyField.data_source('Origin Connection Timeout', 'connection_timeout'),
])

origin_group = TableDynamicLayout.set_fields('Origin Groups', 'data.origin_groups.items', fields=[
    TextDyField.data_source('Origin Group ID', 'id'),
    ListDyField.data_source('Origins', 'members.items', options={
        'sub_key': 'origin_id', 'delimiter': '<br>'
    }),
    ListDyField.data_source('Failover criteria', 'failover_criteria.status_codes.items', options={
        'delimiter': '<br>',
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
    resource = PolyModelType(DistributionResource)
