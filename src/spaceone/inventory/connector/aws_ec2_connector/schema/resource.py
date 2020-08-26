from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_ec2_connector.schema.data import SecurityGroup
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout

sg = ItemDynamicLayout.set_fields('Security Group', fields=[
    TextDyField.data_source('ID', 'data.group_id'),
    TextDyField.data_source('Name', 'data.group_name'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('Account ID', 'data.owner_id'),
])

inbound_rules = TableDynamicLayout.set_fields('Inbound Rules', 'data.ip_permissions', fields=[
    EnumDyField.data_source('Protocol', 'protocol_display', default_badge={
        'coral.600': ['ALL'], 'indigo.500': ['TCP'], 'peacock.500': ['UDP'], 'green.500': ['ICMP']}),
    TextDyField.data_source('Port range', 'port_display'),
    TextDyField.data_source('Source', 'source_display'),
    TextDyField.data_source('Description', 'description_display'),
])

outbound_rules = TableDynamicLayout.set_fields('Outbound Rules', 'data.ip_permissions_egress', fields=[
    EnumDyField.data_source('Protocol', 'protocol_display', default_badge={
        'coral.600': ['ALL'], 'indigo.500': ['TCP'], 'peacock.500': ['UDP'], 'green.500': ['ICMP']}),
    TextDyField.data_source('Port range', 'port_display'),
    TextDyField.data_source('Source', 'source_display'),
    TextDyField.data_source('Description', 'description_display'),
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[sg, inbound_rules, outbound_rules, tags])


class EC2Resource(CloudServiceResource):
    cloud_service_group = StringType(default='EC2')


class SecurityGroupResource(EC2Resource):
    cloud_service_type = StringType(default='SecurityGroup')
    data = ModelType(SecurityGroup)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class SecurityGroupResponse(CloudServiceResponse):
    resource = PolyModelType(SecurityGroupResource)
