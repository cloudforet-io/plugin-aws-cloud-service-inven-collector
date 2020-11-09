from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_ec2_connector.schema.data import SecurityGroup, Image
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
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

sg_tags = SimpleTableDynamicLayout.set_tags()
sg_metadata = CloudServiceMeta.set_layouts(layouts=[sg, inbound_rules, outbound_rules, sg_tags])


ami = ItemDynamicLayout.set_fields('AMI', fields=[
    TextDyField.data_source('AMI ID', 'data.image_id'),
    TextDyField.data_source('AMI Name', 'data.name'),
    TextDyField.data_source('Owner', 'data.owner_id'),
    TextDyField.data_source('Source', 'data.image_location'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'available': ['available'],
        'warning': ['pending', 'transient', 'deregistered', 'invalid'],
        'alert': ['error', 'failed']
    }),
    TextDyField.data_source('State Reason', 'data.state_reason.message'),
    DateTimeDyField.data_source('Creation Date', 'data.creation_date'),
    TextDyField.data_source('Platform Details', 'data.platform_details'),
    TextDyField.data_source('Architecture', 'data.architecture'),
    TextDyField.data_source('Usage Operation', 'data.usage_operation'),
    TextDyField.data_source('Image Type', 'data.image_type'),
    TextDyField.data_source('Virtualization Type', 'data.virtualization_type'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Root Device Name', 'data.root_device_name'),
    TextDyField.data_source('Root Device Type', 'data.root_device_type'),
    TextDyField.data_source('RAM Disk ID', 'data.platform'),
    TextDyField.data_source('Kernel ID', 'data.platform'),
    ListDyField.data_source('Block Devices', 'data.block_device_mappings', default_badge={
            'sub_key': 'device_name',
    }),
])

ami_permission = TableDynamicLayout.set_fields('Permission', 'data.launch_permissions', fields=[
    TextDyField.data_source('AWS Account ID', 'user_id')
])

ami_tags = SimpleTableDynamicLayout.set_tags()

ami_metadata = CloudServiceMeta.set_layouts(layouts=[ami, ami_permission, ami_tags])


class EC2Resource(CloudServiceResource):
    cloud_service_group = StringType(default='EC2')


class SecurityGroupResource(EC2Resource):
    cloud_service_type = StringType(default='SecurityGroup')
    data = ModelType(SecurityGroup)
    _metadata = ModelType(CloudServiceMeta, default=sg_metadata, serialized_name='metadata')


class SecurityGroupResponse(CloudServiceResponse):
    resource = PolyModelType(SecurityGroupResource)


class ImageResource(EC2Resource):
    cloud_service_type = StringType(default='AMI')
    data = ModelType(Image)
    _metadata = ModelType(CloudServiceMeta, default=ami_metadata, serialized_name='metadata')


class ImageResponse(CloudServiceResponse):
    resource = PolyModelType(ImageResource)
