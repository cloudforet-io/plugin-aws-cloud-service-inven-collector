from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_direct_connect_connector.schema.data import Connection, LAG, \
    DirectConnecGateway, VirtualPrivateGateway
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField, BadgeItemDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

connection = ItemDynamicLayout.set_fields('Connections', fields=[
    TextDyField.data_source('ID', 'data.connection_id'),
    TextDyField.data_source('Name', 'data.connection_name'),
    EnumDyField.data_source('State', 'data.connection_state', default_state={
        'safe': ['available'],
        'available': ['requested'],
        'alert': ['down', 'rejected'],
        'warning': ['ordering', 'pending', 'deleting'],
        'disable': ['unknown', 'deleted']
    }),
    TextDyField.data_source('Region', 'data.region'),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Bandwidth', 'data.bandwidth'),
    TextDyField.data_source('Vlan', 'data.vlan'),
    TextDyField.data_source('Partner Name', 'data.partner_name'),
    TextDyField.data_source('Lag ID', 'data.lag_id'),
    TextDyField.data_source('AWS Device', 'data.aws_device'),
    TextDyField.data_source('Provider name', 'data.provider_name'),
    TextDyField.data_source('Owner Account', 'data.owner_account'),
])

connection_tags = SimpleTableDynamicLayout.set_tags()
connection_metadata = CloudServiceMeta.set_layouts(layouts=[connection, connection_tags])


dcgw = ItemDynamicLayout.set_fields('Direct Connect Gateway', fields=[
    TextDyField.data_source('ID', 'data.direct_connect_gateway_id'),
    TextDyField.data_source('Name', 'data.direct_connect_gateway_name'),
    EnumDyField.data_source('State', 'data.direct_connect_gateway_state', default_state={
        'safe': ['available'],
        'disable': ['deleted'],
        'warning': ['pending', 'deleting']
    }),
    TextDyField.data_source('Amazon side ASN', 'data.amazon_side_asn'),
])
dcgw_tags = SimpleTableDynamicLayout.set_tags()
dcgw_metadata = CloudServiceMeta.set_layouts(layouts=[dcgw, dcgw_tags])

vpgw = ItemDynamicLayout.set_fields('Virtual Private Gateway', fields=[
    TextDyField.data_source('ID', 'data.virtual_gateway_id'),
    TextDyField.data_source('Region', 'data.region'),
    EnumDyField.data_source('State', 'data.virtual_gateway_state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
])
vpgw_tags = SimpleTableDynamicLayout.set_tags()
vpgw_metadata = CloudServiceMeta.set_layouts(layouts=[vpgw, vpgw_tags])

lag = ItemDynamicLayout.set_fields('LAGs', fields=[
    TextDyField.data_source('ID', 'data.lag_id'),
    TextDyField.data_source('Name', 'data.lag_name'),
    EnumDyField.data_source('State', 'data.lag_state', default_state={
        'safe': ['requested', 'available'],
        'alert': ['deleting', 'deleted', 'down'],
        'disable': ['unknown']
    }),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Region', 'data.region'),
    TextDyField.data_source('Minimum Links', 'data.minimum_links'),
    TextDyField.data_source('Minimum Links', 'data.minimum_links'),
    TextDyField.data_source('AWS Device', 'data.aws_device'),
    TextDyField.data_source('AWS Device (V2)', 'data.aws_device_v2'),
    EnumDyField.data_source('Jumbo Frame Capable', 'data.jumbo_frame_capable', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),

])
lag_tags = SimpleTableDynamicLayout.set_tags()
lag_metadata = CloudServiceMeta.set_layouts(layouts=[lag, lag_tags])


class DirectConnectResource(CloudServiceResource):
    cloud_service_group = StringType(default='DirectConnect')


# CONNECTION
class ConnectionResource(DirectConnectResource):
    cloud_service_type = StringType(default='Connection')
    data = ModelType(Connection)
    _metadata = ModelType(CloudServiceMeta, default=connection_metadata, serialized_name='metadata')


class ConnectionResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.connection_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(ConnectionResource)


# DIRECT CONNECT GATEWAY
class DirectConnectGatewayResource(DirectConnectResource):
    cloud_service_type = StringType(default='DirectConnectGateway')
    data = ModelType(DirectConnecGateway)
    _metadata = ModelType(CloudServiceMeta, default=dcgw_metadata, serialized_name='metadata')


class DirectConnectGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.direct_connect_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(DirectConnectGatewayResource)


# VIRTUAL PRIVATE GATEWAY
class VirtualPrivateGatewayResource(DirectConnectResource):
    cloud_service_type = StringType(default='VirtualPrivateGateway')
    data = ModelType(VirtualPrivateGateway)
    _metadata = ModelType(CloudServiceMeta, default=vpgw_metadata, serialized_name='metadata')


class VirtualPrivateGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.virtual_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(VirtualPrivateGatewayResource)


# LAG
class LAGResource(DirectConnectResource):
    cloud_service_type = StringType(default='LAG')
    data = ModelType(LAG)
    _metadata = ModelType(CloudServiceMeta, default=lag_metadata, serialized_name='metadata')


class LAGResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.lag_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(LAGResource)
