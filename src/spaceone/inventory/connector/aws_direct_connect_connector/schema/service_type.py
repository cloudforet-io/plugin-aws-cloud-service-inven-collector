import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

'''
CONNECTION
'''
connection_total_count_conf = os.path.join(current_dir, 'widget/connection_total_count.yaml')
# connection_bandwidth_total_sum_conf = os.path.join(current_dir, 'widget/connection_bandwidth_total_sum.yaml')
connection_count_by_region_widget_conf = os.path.join(current_dir, 'widget/connection_count_by_region.yaml')
connection_count_by_account_widget_conf = os.path.join(current_dir, 'widget/connection_count_by_account.yaml')

cst_connection = CloudServiceTypeResource()
cst_connection.name = 'Connection'
cst_connection.provider = 'aws'
cst_connection.group = 'DirectConnect'
cst_connection.labels = ['Networking']
cst_connection.is_primary = True
cst_connection.is_major = True
cst_connection.service_code = 'AWSDirectConnect'
cst_connection.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
}

cst_connection_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
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
        # For Dynamic Table
        TextDyField.data_source('ID', 'data.connection_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Logical Redundancy', 'data.has_logical_redundancy', options={
            'is_optional': True
        }),
        TextDyField.data_source('VLAN', 'data.vlan', options={
            'is_optional': True
        }),
        TextDyField.data_source('LAG ID', 'data.lag_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Jumbo Frame Capable', 'data.jumbo_frame_capable', options={
            'is_optional': True
        }),
        TextDyField.data_source('Partner Name', 'data.partner_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Device', 'data.aws_device', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Device V2', 'data.aws_device_v2', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Connection ID', key='data.connection_id'),
        SearchField.set(name='State', key='data.connection_state',
                        enums={'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                               'requested': {'label': 'Requested', 'icon': {'color': 'blue.400'}},
                               'down': {'label': 'Down', 'icon': {'color': 'red.500'}},
                               'rejected': {'label': 'Rejected', 'icon': {'color': 'red.500'}},
                               'ordering': {'label': 'Ordering', 'icon': {'color': 'yellow.500'}},
                               'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                               'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                               'unknown': {'label': 'Unknown', 'icon': {'color': 'gray.400'}},
                               'deleted': {'label': 'Deleted', 'icon': {'color': 'gray.400'}}
                               }),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Vlan', key='data.vlan'),
        SearchField.set(name='Partner Name', key='data.partner_name'),
        SearchField.set(name='Lag ID', key='data.lag_id'),
        SearchField.set(name='AWS Device', key='data.aws_device'),
        SearchField.set(name='Provider Name', key='data.provider_name')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(connection_total_count_conf)),
#         CardWidget.set(**get_data_from_yaml(connection_bandwidth_total_sum_conf)),
        ChartWidget.set(**get_data_from_yaml(connection_count_by_region_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(connection_count_by_account_widget_conf))
    ]
)
cst_connection._metadata = cst_connection_meta

'''
DIRECT CONNECT GATEWAY
'''
dcgw_total_count_widget_conf = os.path.join(current_dir, 'widget/dcgw_total_count.yaml')
dcgw_count_by_region_widget_conf = os.path.join(current_dir, 'widget/dcgw_count_by_region.yaml')
dcgw_count_by_account_widget_conf = os.path.join(current_dir, 'widget/dcgw_count_by_account.yaml')

cst_dc_gw = CloudServiceTypeResource()
cst_dc_gw.name = 'DirectConnectGateway'
cst_dc_gw.provider = 'aws'
cst_dc_gw.group = 'DirectConnect'
cst_dc_gw.labels = ['Networking']
cst_dc_gw.service_code = 'AWSDirectConnect'
cst_dc_gw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
}
cst_dc_gw_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.direct_connect_gateway_id'),
        TextDyField.data_source('Name', 'name'),
        EnumDyField.data_source('State', 'data.direct_connect_gateway_state', default_state={
            'safe': ['available'],
            'disable': ['deleted'],
            'warning': ['pending', 'deleting']
        }),
        # For Dynamic Table
        TextDyField.data_source('Amazon side ASN', 'data.amazon_side_asn', options={
            'is_optional': True
        }),
        TextDyField.data_source('State Change Error', 'data.state_change_error', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Direct Connect Gateway ID', key='data.direct_connect_gateway_id'),
        SearchField.set(name='State', key='data.direct_connect_gateway_state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'gray.400'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}}
                        }),
        SearchField.set(name='Amazon Side ASN', key='data.amazon_side_asn')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(dcgw_total_count_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(dcgw_count_by_region_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(dcgw_count_by_account_widget_conf))
    ]
)
cst_dc_gw._metadata = cst_dc_gw_meta


'''
VIRTUAL PRIVATE GATEWAY
'''
vpgw_total_count_widget_conf = os.path.join(current_dir, 'widget/vpgw_total_count.yaml')
vpgw_count_by_region_widget_conf = os.path.join(current_dir, 'widget/vpgw_count_by_region.yaml')
vpgw_count_by_account_widget_conf = os.path.join(current_dir, 'widget/vpgw_count_by_account.yaml')

cst_vp_gw = CloudServiceTypeResource()
cst_vp_gw.name = 'VirtualPrivateGateway'
cst_vp_gw.provider = 'aws'
cst_vp_gw.group = 'DirectConnect'
cst_vp_gw.labels = ['Networking']
cst_vp_gw.service_code = 'AWSDirectConnect'
cst_vp_gw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
}
cst_vp_gw_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.virtual_gateway_id'),
        EnumDyField.data_source('State', 'data.virtual_gateway_state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'deleting'],
            'disable': ['deleted']
        }),
        # For Dynamic Table
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Virtual Private Gateway ID', key='data.virtual_gateway_id'),
        SearchField.set(name='State', key='data.virtual_gateway_state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'gray.400'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}}
                        })
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(vpgw_total_count_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(vpgw_count_by_region_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(vpgw_count_by_account_widget_conf))
    ]
)
cst_vp_gw._metadata = cst_vp_gw_meta


'''
LAG
'''
lag_total_count_widget_conf = os.path.join(current_dir, 'widget/lag_total_count.yaml')
# lag_bandwidth_total_sum_conf = os.path.join(current_dir, 'widget/lag_bandwidth_total_sum.yaml')
lag_count_by_region_widget_conf = os.path.join(current_dir, 'widget/lag_count_by_region.yaml')
lag_count_by_account_widget_conf = os.path.join(current_dir, 'widget/lag_count_by_account.yaml')

cst_lags = CloudServiceTypeResource()
cst_lags.name = 'LAG'
cst_lags.provider = 'aws'
cst_lags.group = 'DirectConnect'
cst_lags.labels = ['Networking']
cst_lags.service_code = 'AWSDirectConnect'
cst_lags.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Direct-Connect.svg',
}
cst_lags_meta = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.lag_id'),
        TextDyField.data_source('Name', 'name'),
        EnumDyField.data_source('State', 'data.lag_state', default_state={
            'available': ['requested'],
            'safe': ['available'],
            'warning': ['deleting'],
            'alert': ['down'],
            'disable': ['unknown', 'deleted']
        }),
        TextDyField.data_source('Location', 'data.location'),
        # For Dynamic Table
        TextDyField.data_source('Connections Bandwidth', 'data.connections_bandwidth', options={
            'is_optional': True
        }),
        TextDyField.data_source('Number of Connections', 'data.number_of_connections', options={
            'is_optional': True
        }),
        TextDyField.data_source('Minimum Links', 'data.minimum_links', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Device', 'data.aws_device', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Device V2', 'data.aws_device_v2', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allows Hosted Connections', 'data.allows_hosted_connections', options={
            'is_optional': True
        }),
        TextDyField.data_source('Jumbo Frame Capable', 'data.jumbo_frame_capable', options={
            'is_optional': True
        }),
        TextDyField.data_source('Logical Redundancy', 'data.has_logical_redundancy', options={
            'is_optional': True
        }),
        TextDyField.data_source('Logical Redundancy', 'data.has_logical_redundancy', options={
            'is_optional': True
        }),
        TextDyField.data_source('Provider Name', 'data.provider_name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Connection IDs', 'data.connections.connection_id', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Connection Names', 'data.connections.connection_name', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Connection States', 'data.connections.connection_state', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Connection VLANs', 'data.connections.vlan', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Connection Bandwidth', 'data.connections.bandwidth', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Lag ID', key='data.lag_id'),
        SearchField.set(name='State', key='data.lag_state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'requested': {'label': 'Available', 'icon': {'color': 'blue.400'}},
                            'deleting': {'label': 'Deleted', 'icon': {'color': 'yellow.500'}},
                            'down': {'label': 'Pending', 'icon': {'color': 'red.500'}},
                            'unknown': {'label': 'Deleting', 'icon': {'color': 'gray.400'}}
                        }),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Connection Count', key='data.number_of_connections', data_type='integer'),
        SearchField.set(name='Bandwidth', key='data.connections_bandwidth'),
        SearchField.set(name='Minimum Links', key='data.minimum_links', data_type='integer'),
        SearchField.set(name='AWS Device', key='data.aws_device')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(lag_total_count_widget_conf)),
        # CardWidget.set(**get_data_from_yaml(lag_bandwidth_total_sum_conf)),
        ChartWidget.set(**get_data_from_yaml(lag_count_by_region_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(lag_count_by_account_widget_conf))
    ]
)
cst_lags._metadata = cst_lags_meta


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_connection}),
    CloudServiceTypeResponse({'resource': cst_dc_gw}),
    CloudServiceTypeResponse({'resource': cst_vp_gw}),
    CloudServiceTypeResponse({'resource': cst_lags}),
]
