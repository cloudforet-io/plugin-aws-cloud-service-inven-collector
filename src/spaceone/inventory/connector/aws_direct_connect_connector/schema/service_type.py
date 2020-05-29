from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

'''
CONNECTION
'''
cst_connection = CloudServiceTypeResource()
cst_connection.name = 'Connection'
cst_connection.provider = 'aws'
cst_connection.group = 'DirectConnect'
cst_connection.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'true',
}

cst_connection_meta = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Id', 'data.connection_id'),
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

])
cst_connection._metadata = cst_connection_meta

'''
DIRECT CONNECT GATEWAY
'''
cst_dc_gw = CloudServiceTypeResource()
cst_dc_gw.name = 'DirectConnectGateway'
cst_dc_gw.provider = 'aws'
cst_dc_gw.group = 'DirectConnect'
cst_dc_gw.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'false',
}
cst_dc_gw_meta = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Id', 'data.direct_connect_gateway_id'),
    TextDyField.data_source('Name', 'data.direct_connect_gateway_name'),
    EnumDyField.data_source('State', 'data.direct_connect_gateway_state', default_state={
        'safe': ['available'],
        'disable': ['deleted'],
        'warning': ['pending', 'deleting']
    }),
])
cst_dc_gw._metadata = cst_dc_gw_meta


'''
VIRTUAL PRIVATE GATEWAY
'''
cst_vp_gw = CloudServiceTypeResource()
cst_vp_gw.name = 'VirtualPrivateGateway'
cst_vp_gw.provider = 'aws'
cst_vp_gw.group = 'DirectConnect'
cst_vp_gw.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'false',
}
cst_vp_gw_meta = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Id', 'data.virtual_gateway_id'),
    EnumDyField.data_source('State', 'data.virtual_gateway_state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Region', 'data.region'),
])
cst_vp_gw._metadata = cst_vp_gw_meta


'''
LAG
'''
cst_lags = CloudServiceTypeResource()
cst_lags.name = 'LAG'
cst_lags.provider = 'aws'
cst_lags.group = 'DirectConnect'
cst_lags.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
    'spaceone:is_major': 'false',
}
cst_lags_meta = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('ID', 'data.lag_id'),
    TextDyField.data_source('Name', 'data.lag_name'),
    EnumDyField.data_source('State', 'data.lag_state', default_state={
        'available': ['requested'],
        'safe': ['available'],
        'warning': ['deleting'],
        'alert': ['down'],
        'disable': ['unknown', 'deleted']
    }),
    TextDyField.data_source('Location', 'data.location'),
    TextDyField.data_source('Region', 'data.region'),
])
cst_lags._metadata = cst_lags_meta


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_connection}),
    CloudServiceTypeResponse({'resource': cst_dc_gw}),
    CloudServiceTypeResponse({'resource': cst_vp_gw}),
    CloudServiceTypeResponse({'resource': cst_lags}),
]
