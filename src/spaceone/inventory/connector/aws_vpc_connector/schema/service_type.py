from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, \
    EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_vpc = CloudServiceTypeResource()
cst_vpc.name = 'VPC'
cst_vpc.provider = 'aws'
cst_vpc.group = 'VPC'
cst_vpc.labels = ['Networking']
cst_vpc.is_primary = True
cst_vpc.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC.svg',
}

cst_vpc._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('VPC ID', 'data.vpc_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending']
        }),
        TextDyField.data_source('CIDR', 'data.cidr_block'),
        TextDyField.data_source('Main Route Table', 'data.main_route_table_id'),
        TextDyField.data_source('Main Network ACL', 'data.main_network_acl_id'),
        TextDyField.data_source('Tenancy', 'data.instance_tenancy'),
        EnumDyField.data_source('Default VPC', 'data.is_default', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        TextDyField.data_source('Owner', 'data.owner_id'),
    ],
    search=[
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                        }),
        SearchField.set(name='CIDR', key='data.cidr_block'),
        SearchField.set(name='Default VPC', key='data.is_default', data_type='boolean'),
        SearchField.set(name='Subnet ID', key='data.subnets.subnet_id'),
        SearchField.set(name='Availability Zone', key='data.subnets.availability_zone'),
        SearchField.set(name='Internet Gateway ID', key='data.internet_gateway.internet_gateway_id'),
        SearchField.set(name='Internet Gateway Name', key='data.internet_gateway.name'),
        SearchField.set(name='NAT Gateway ID', key='data.nat_gateways.nat_gateway_id'),
        SearchField.set(name='NAT Gateway Name', key='data.nat_gateways.name'),
        SearchField.set(name='Endpoint ID', key='data.endpoints.vpc_endpoint_id'),
        SearchField.set(name='Peering Connection ID', key='data.peering_connections.vpc_peering_connection_id'),
        SearchField.set(name='Egress Only Internet Gateway ID',
                        key='data.egress_only_internet_gateway.egress_only_internet_gateway_id'),
        SearchField.set(name='VPN Gateway ID', key='data.vpn_gateway.vpn_gateway_id'),
        SearchField.set(name='VPN Gateway Name', key='data.vpn_gateway.name'),
        SearchField.set(name='Transit Gateway ID', key='data.transit_gateway.transit_gateway_id'),
        SearchField.set(name='Transit Gateway Name', key='data.transit_gateway.name'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_subnet = CloudServiceTypeResource()
cst_subnet.name = 'Subnet'
cst_subnet.provider = 'aws'
cst_subnet.group = 'VPC'
cst_subnet.labels = ['Networking']
cst_subnet.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC.svg',
}

cst_subnet._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Subnet ID', 'data.subnet_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending']
        }),
        TextDyField.data_source('CIDR', 'data.cidr_block'),
        TextDyField.data_source('AZ', 'data.availability_zone'),
        EnumDyField.data_source('Type', 'data.subnet_type', default_badge={
            'indigo.500': ['public'], 'coral.600': ['private']
        }),
        TextDyField.data_source('VPC', 'data.vpc_id'),
    ],
    search=[
        SearchField.set(name='Subnet ID', key='data.subnet_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                        }),
        SearchField.set(name='Subnet Type', key='data.subnet_type',
                        enums={
                            'public': {'label': 'Public'},
                            'private': {'label': 'Private'},
                        }),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='CIDR', key='data.cidr_block'),
        SearchField.set(name='Available IP Address Count', key='data.available_ip_address_count', data_type='integer'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='Route Table ID', key='data.route_table.route_table_id'),
        SearchField.set(name='Network ACL ID', key='data.network_acl.network_acl_id'),
        SearchField.set(name='Default', key='data.default_for_az', data_type='boolean'),
        SearchField.set(name='Auto-assign Public IP', key='data.map_public_ip_on_launch', data_type='boolean'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_rt = CloudServiceTypeResource()
cst_rt.name = 'RouteTable'
cst_rt.provider = 'aws'
cst_rt.group = 'VPC'
cst_rt.labels = ['Networking']
cst_rt.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC.svg',
}

cst_rt._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Route Table ID', 'data.route_table_id'),
        ListDyField.data_source('Subnet associations', 'data.subnet_associations', default_badge={
            'type': 'outline',
            'sub_key': 'subnet_id',
        }),
        ListDyField.data_source('Edge associations', 'data.edge_associations', default_badge={
            'type': 'outline',
            'sub_key': 'gateway_id',
        }),
        EnumDyField.data_source('Main', 'data.main', default_badge={
            'indigo.500': ['Yes'], 'coral.600': ['No']
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id'),
    ],
    search=[
        SearchField.set(name='Route Table ID', key='data.route_table_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Associated Subnet ID', key='data.subnet_associations.subnet_id'),
        SearchField.set(name='Main', key='data.main',
                        enums={
                            'Yes': {'label': 'Yes'},
                            'No': {'label': 'No'},
                        }),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_igw = CloudServiceTypeResource()
cst_igw.name = 'InternetGateway'
cst_igw.provider = 'aws'
cst_igw.group = 'VPC'
cst_igw.labels = ['Networking']
cst_igw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Internet-Gateway_light-bg.svg',
}

cst_igw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Internet Gateway ID', 'data.internet_gateway_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'available': ['available'],
            'safe': ['attached'],
            'warning': ['attaching', 'detaching'],
            'disable': ['detached']
        }),
        ListDyField.data_source('VPC ID', 'data.attachments', default_badge={
            'type': 'outline',
            'sub_key': 'vpc_id',
        })
    ],
    search=[
        SearchField.set(name='Internet Gateway ID', key='data.internet_gateway_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'blue.400'}},
                            'attached': {'label': 'Attached', 'icon': {'color': 'green.500'}},
                            'attaching': {'label': 'Attaching', 'icon': {'color': 'yellow.500'}},
                            'detaching': {'label': 'Detaching', 'icon': {'color': 'yellow.500'}},
                            'detached': {'label': 'Detached', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_eoigw = CloudServiceTypeResource()
cst_eoigw.name = 'EgressOnlyInternetGateway'
cst_eoigw.provider = 'aws'
cst_eoigw.group = 'VPC'
cst_eoigw.labels = ['Networking']
cst_eoigw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Internet-Gateway_light-bg.svg',
}
cst_eoigw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Egress Only Internet Gateway ID', 'data.egress_only_internet_gateway_id'),
        ListDyField.data_source('State', 'data.attachments', default_badge={
            'type': 'outline',
            'sub_key': 'state',
        }),
        ListDyField.data_source('VPC ID', 'data.attachments', default_badge={
            'type': 'outline',
            'sub_key': 'vpc_id',
        }),
    ],
    search=[
        SearchField.set(name='Egress Only Gateway ID', key='data.egress_only_internet_gateway_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.attachments.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'blue.400'}},
                            'attached': {'label': 'Attached', 'icon': {'color': 'green.500'}},
                            'attaching': {'label': 'Attaching', 'icon': {'color': 'yellow.500'}},
                            'detaching': {'label': 'Detaching', 'icon': {'color': 'yellow.500'}},
                            'detached': {'label': 'Detached', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='VPC ID', key='data.attachments.vpc_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_natgw = CloudServiceTypeResource()
cst_natgw.name = 'NATGateway'
cst_natgw.provider = 'aws'
cst_natgw.group = 'VPC'
cst_natgw.labels = ['Networking']
cst_natgw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_NAT-Gateway_light-bg.svg',
}
cst_natgw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('NAT Gateway ID', 'data.nat_gateway_id'),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'deleting', ],
            'alert': ['failed'],
            'disable': ['deleted']
        }),
        ListDyField.data_source('Elastic IP', 'data.nat_gateway_addresses', default_badge={
            'type': 'outline',
            'sub_key': 'public_ip',
            'delimiter': '  '
        }),
        ListDyField.data_source('Private IP', 'data.nat_gateway_addresses', default_badge={
            'type': 'outline',
            'sub_key': 'private_ip',
            'delimiter': '  '
        }),
        ListDyField.data_source('Network Interface', 'data.nat_gateway_addresses', default_badge={
            'type': 'outline',
            'sub_key': 'network_interface_id',
            'delimiter': '  '
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id'),
        TextDyField.data_source('Subnet', 'data.subnet_id'),
        DateTimeDyField.data_source('Created', 'data.create_time'),
    ],
    search=[
        SearchField.set(name='NAT Gateway ID', key='data.nat_gateway_id'),
        SearchField.set(name='Status', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'failed': {'label': 'Failed', 'icon': {'color': 'red.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Elastic IP', key='data.nat_gateway_addresses.public_ip'),
        SearchField.set(name='Private IP', key='data.nat_gateway_addresses.private_ip'),
        SearchField.set(name='Network Interface ID', key='data.nat_gateway_addresses.network_interface_id'),
        SearchField.set(name='Subnet ID', key='data.subnet_id'),
        SearchField.set(name='Created Time', key='data.create_time', data_type='datetime'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_peerconn = CloudServiceTypeResource()
cst_peerconn.name = 'PeeringConnection'
cst_peerconn.provider = 'aws'
cst_peerconn.group = 'VPC'
cst_peerconn.labels = ['Networking']
cst_peerconn.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Peering_light-bg.svg',
}
cst_peerconn._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Peering Connection ID', 'data.vpc_peering_connection_id'),
        EnumDyField.data_source('Status', 'data.status.code', default_state={
            'safe': ['active'],
            'warning': ['initiating-request', 'pending-acceptance', 'provisioning', 'deleting'],
            'disable': ['deleted'],
            'alert': ['rejected', 'failed', 'expired']
        }),
        TextDyField.data_source('Requester VPC', 'data.requester_vpc_info.vpc_id'),
        TextDyField.data_source('Requester VPC CIDR', 'data.requester_vpc_info.cidr_block'),
        TextDyField.data_source('Requester Owner', 'data.requester_vpc_info.owner_id'),
        TextDyField.data_source('Accepter VPC', 'data.accepter_vpc_info.vpc_id'),
        TextDyField.data_source('Accepter VPC CIDR', 'data.accepter_vpc_info.cidr_block'),
        TextDyField.data_source('Accepter Owner', 'data.accepter_vpc_info.owner_id'),
    ],
    search=[
        SearchField.set(name='Peering Connection ID', key='data.vpc_peering_connection_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Status', key='data.status.code',
                        enums={
                            'active': {'label': 'Active', 'icon': {'color': 'green.500'}},
                            'initiating-request': {'label': 'Initiating Request', 'icon': {'color': 'yellow.500'}},
                            'pending-acceptance': {'label': 'Pending Acceptance', 'icon': {'color': 'yellow.500'}},
                            'provisioning': {'label': 'Provisioning', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'failed': {'label': 'Failed', 'icon': {'color': 'red.500'}},
                            'rejected': {'label': 'Rejected', 'icon': {'color': 'red.500'}},
                            'expired': {'label': 'Expired', 'icon': {'color': 'red.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Requester VPC ID', key='data.requester_vpc_info.vpc_id'),
        SearchField.set(name='Accepter VPC Id', key='data.accepter_vpc_info.vpc_id'),

        SearchField.set(name='Expiration Time', key='data.expiration_time', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_nacl = CloudServiceTypeResource()
cst_nacl.name = 'NetworkACL'
cst_nacl.provider = 'aws'
cst_nacl.group = 'VPC'
cst_nacl.labels = ['Networking']
cst_nacl.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_NACL_light-bg.svg',
}
cst_nacl._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Network ACL ID', 'data.network_acl_id'),
        EnumDyField.data_source('Default', 'data.is_default', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id'),
    ],
    search=[
        SearchField.set(name='Network ACL ID', key='data.network_acl_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Default', key='data.is_default', data_type='boolean'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Inbound Protocol', key='data.inbound_entries.protocol'),
        SearchField.set(name='Inbound Port From', key='data.inbound_entries.port_range.port_from'),
        SearchField.set(name='Inbound Port To', key='data.inbound_entries.port_range.port_to'),
        SearchField.set(name='Inbound Source', key='data.inbound_entries.cidr_block'),
        SearchField.set(name='Inbound Allow/Deny', key='data.inbound_entries.rule_action',
                        enums={
                            'allow': {'label': 'Allow'},
                            'deny': {'label': 'Deny'},
                        }),
        SearchField.set(name='Outbound Protocol', key='data.outbound_entries.protocol'),
        SearchField.set(name='Outbound Port From', key='data.outbound_entries.port_range.port_from'),
        SearchField.set(name='Outbound Port To', key='data.outbound_entries.port_range.port_to'),
        SearchField.set(name='Outbound Source', key='data.outbound_entries.cidr_block'),
        SearchField.set(name='Outbound Allow/Deny', key='data.outbound_entries.rule_action',
                        enums={
                            'allow': {'label': 'Allow'},
                            'deny': {'label': 'Deny'},
                        }),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_endpoint = CloudServiceTypeResource()
cst_endpoint.name = 'Endpoint'
cst_endpoint.provider = 'aws'
cst_endpoint.group = 'VPC'
cst_endpoint.labels = ['Networking']
cst_endpoint.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Endpoints_light-bg.svg',
}
cst_endpoint._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Endpoint ID', 'data.vpc_endpoint_id'),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pendingAcceptance', 'pending', 'deleting'],
            'disable': ['deleted'],
            'alert': ['rejected', 'failed', 'expired']
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id'),
        TextDyField.data_source('Service Name', 'data.service_name'),
        EnumDyField.data_source('Endpoint Type', 'data.vpc_endpoint_type', default_outline_badge=['Interface', 'Gateway']),
        DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
    ],
    search=[
        SearchField.set(name='Endpoint ID', key='data.vpc_endpoint_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Status', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pendingAcceptance': {'label': 'Pending Acceptance', 'icon': {'color': 'yellow.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'rejected': {'label': 'Rejected', 'icon': {'color': 'red.500'}},
                            'failed': {'label': 'Failed', 'icon': {'color': 'red.500'}},
                            'expired': {'label': 'Expired', 'icon': {'color': 'red.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Service Name', key='data.service_name'),
        SearchField.set(name='Endpoint Type', key='data.vpc_endpoint_type',
                        enums={
                            'Interface': {'label': 'Interface'},
                            'Gateway': {'label': 'Gateway'}
                        }),
        SearchField.set(name='DNS Name', key='data.dns_entries.dns_name'),
        SearchField.set(name='Private DNS Names enabled', key='data.private_dns_enabled', data_type='boolean'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_transitgw = CloudServiceTypeResource()
cst_transitgw.name = 'TransitGateway'
cst_transitgw.provider = 'aws'
cst_transitgw.group = 'VPC'
cst_transitgw.labels = ['Networking']
cst_transitgw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Transit_Gateway.svg',
}
cst_transitgw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Transit Gateway ID', 'data.transit_gateway_id'),
        TextDyField.data_source('Owner ID', 'data.owner_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'modifying', 'deleting'],
            'disable': ['deleted']
        })
    ],
    search=[
        SearchField.set(name='Transit Gateway ID', key='data.transit_gateway_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'modifying': {'label': 'Modifying', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Associated Route Table ID',
                        key='data.transit_gateway_route_table.transit_gateway_route_table_id'),
        SearchField.set(name='VPN Connection ID', key='data.vpn_connections.vpn_connection_id'),
        SearchField.set(name='VPN Connection Name', key='data.vpn_connections.name'),
        SearchField.set(name='Customer Gateway ID', key='data.vpn_connections.customer_gateway_id'),
        SearchField.set(name='VPN Gateway ID', key='data.vpn_connections.vpn_gateway_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_customgw = CloudServiceTypeResource()
cst_customgw.name = 'CustomerGateway'
cst_customgw.provider = 'aws'
cst_customgw.group = 'VPC'
cst_customgw.labels = ['Networking']
cst_customgw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Customer-Gateway_dark-bg.svg',
}
cst_customgw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('ID', 'data.customer_gateway_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'deleting'],
            'disable': ['deleted']
        }),
        TextDyField.data_source('Type', 'data.type'),
        TextDyField.data_source('IP Address', 'data.ip_address'),
        TextDyField.data_source('BGP ASN', 'data.bgp_asn'),
    ],
    search=[
        SearchField.set(name='Customer Gateway ID', key='data.customer_gateway_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Type', key='data.type'),
        SearchField.set(name='IP Address', key='data.ip_address'),
        SearchField.set(name='BGP ASN', key='data.bgp_asn'),
        SearchField.set(name='Device', key='data.device_name'),
        SearchField.set(name='VPN Connection ID', key='data.vpn_connection.vpn_connection_id'),
        SearchField.set(name='VPN Connection Name', key='data.vpn_connection.name'),
        SearchField.set(name='VPN Connection State', key='data.vpn_connection.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_vpnconn = CloudServiceTypeResource()
cst_vpnconn.name = 'VPNConnection'
cst_vpnconn.provider = 'aws'
cst_vpnconn.group = 'VPC'
cst_vpnconn.labels = ['Networking']
cst_vpnconn.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Connection_dark-bg.svg',
}
cst_vpnconn._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('VPN ID', 'data.vpn_connection_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'deleting'],
            'disable': ['deleted']
        }),
        TextDyField.data_source('Virtual Private Gateway', 'data.vpn_gateway_id'),
        TextDyField.data_source('Transit Gateway', 'data.transit_gateway_id'),
        TextDyField.data_source('Customer Gateway', 'data.customer_gateway_id'),
        TextDyField.data_source('Customer Gateway Address', 'data.customer_gateway_address'),
        TextDyField.data_source('Type', 'data.type'),
        EnumDyField.data_source('Category', 'data.category', default_badge={
            'indigo.500': ['VPN'], 'coral.500': ['VPN-Classic']
        }),
    ],
    search=[
        SearchField.set(name='VPN Connection ID', key='data.vpn_connection_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Virtual Private Gateway ID', key='data.vpn_gateway_id'),
        SearchField.set(name='Customer Gateway ID', key='data.customer_gateway_id'),
        SearchField.set(name='Transit Gateway ID', key='data.transit_gateway_id'),
        SearchField.set(name='Type', key='data.type'),
        SearchField.set(name='Category', key='data.category',
                        enums={
                            'VPN': {'label': 'VPN'},
                            'VPN-Classic': {'label': 'VPN Classic'},
                        }),
        SearchField.set(name='VPN Tunnel IP', key='data.vgw_telemetry.outside_ip_address'),
        SearchField.set(name='VPN Tunnel Status', key='data.vgw_telemetry.status',
                        enums={
                            'UP': {'label': 'UP'},
                            'DOWN': {'label': 'DOWN'},
                        }),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_vpngw = CloudServiceTypeResource()
cst_vpngw.name = 'VPNGateway'
cst_vpngw.provider = 'aws'
cst_vpngw.group = 'VPC'
cst_vpngw.labels = ['Networking']
cst_vpngw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Gateway_dark-bg.svg',
}
cst_vpngw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('ID', 'data.vpn_gateway_id'),
        TextDyField.data_source('State', 'data.state'),
        TextDyField.data_source('Type', 'data.type'),
        ListDyField.data_source('VPC', 'data.vpc_attachments', default_badge={
            'type': 'outline',
            'sub_key': 'vpc_id',
        }),
        TextDyField.data_source('ASN (Amazon side)', 'data.amazon_side_asn'),
    ],
    search=[
        SearchField.set(name='Virtual Private Gateway ID', key='data.vpn_gateway_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Type', key='data.type'),
        SearchField.set(name='VPC ID', key='data.vpc_attachments.vpc_id'),
        SearchField.set(name='ASN', key='data.amazon_side_asn'),
        SearchField.set(name='VPN Connection ID', key='data.vpn_connection.vpn_connection_id'),
        SearchField.set(name='VPN Connection Name', key='data.vpn_connection.name'),
        SearchField.set(name='VPN Connection Status', key='data.vpn_connection.state',
                        enums={
                            'available': {'label': 'Available', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'Pending', 'icon': {'color': 'yellow.500'}},
                            'deleting': {'label': 'Deleting', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'Deleted', 'icon': {'color': 'grey.500'}},
                        }),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_vpc}),
    CloudServiceTypeResponse({'resource': cst_subnet}),
    CloudServiceTypeResponse({'resource': cst_rt}),
    CloudServiceTypeResponse({'resource': cst_igw}),
    CloudServiceTypeResponse({'resource': cst_eoigw}),
    CloudServiceTypeResponse({'resource': cst_natgw}),
    CloudServiceTypeResponse({'resource': cst_peerconn}),
    CloudServiceTypeResponse({'resource': cst_nacl}),
    CloudServiceTypeResponse({'resource': cst_endpoint}),
    CloudServiceTypeResponse({'resource': cst_transitgw}),
    CloudServiceTypeResponse({'resource': cst_customgw}),
    CloudServiceTypeResponse({'resource': cst_vpnconn}),
    CloudServiceTypeResponse({'resource': cst_vpngw}),
]
