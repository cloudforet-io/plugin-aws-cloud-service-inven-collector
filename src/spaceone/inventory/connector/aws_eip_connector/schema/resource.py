from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_eip_connector.schema.data import ElasticIPAddress
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout


base = ItemDynamicLayout.set_fields('Elastic IPs', fields=[
    TextDyField.data_source('Public IPv4 Address', 'data.public_ip'),
    TextDyField.data_source('Associated Instance ID', 'data.instance_id'),
    TextDyField.data_source('Public DNS', 'data.public_dns'),
    TextDyField.data_source('Allocation ID', 'data.allocation_id'),
    TextDyField.data_source('Private IP Address', 'data.private_ip_address'),
    TextDyField.data_source('NAT Gateway ID', 'data.nat_gateway_id'),
    TextDyField.data_source('Association ID', 'data.association_id'),
    TextDyField.data_source('Network Interface ID', 'data.network_interface_id'),
    BadgeDyField.data_source('Address Pool', 'data.public_ipv4_pool'),
    EnumDyField.data_source('Scope', 'data.domain', default_outline_badge=['vpc', 'standard']),
    TextDyField.data_source('Network Interface Owner Account ID', 'data.network_interface_owner_id'),
    TextDyField.data_source('Customer owned IP Address', 'data.customer_owned_ip'),
    TextDyField.data_source('Customer owned IP Address Pool', 'data.customer_owned_ipv4_pool'),
])

eip_tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[base, eip_tags])


class EC2Resource(CloudServiceResource):
    cloud_service_group = StringType(default='EC2')


class EIPResource(EC2Resource):
    cloud_service_type = StringType(default='EIP')
    data = ModelType(ElasticIPAddress)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class EIPResponse(CloudServiceResponse):
    resource = PolyModelType(EIPResource)
