from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_vpc = CloudServiceTypeResource()
cst_vpc.name = 'VPC'
cst_vpc.provider = 'aws'
cst_vpc.group = 'VPC'
cst_vpc.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC.svg',
    'spaceone:is_major': 'false',
}

cst_vpc._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])

cst_subnet = CloudServiceTypeResource()
cst_subnet.name = 'Subnet'
cst_subnet.provider = 'aws'
cst_subnet.group = 'VPC'
cst_subnet.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC.svg',
    'spaceone:is_major': 'false',
}

cst_subnet._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


cst_rt = CloudServiceTypeResource()
cst_rt.name = 'RouteTable'
cst_rt.provider = 'aws'
cst_rt.group = 'VPC'
cst_rt.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC.svg',
    'spaceone:is_major': 'false',
}

cst_rt._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


cst_igw = CloudServiceTypeResource()
cst_igw.name = 'InternetGateway'
cst_igw.provider = 'aws'
cst_igw.group = 'VPC'
cst_igw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Internet-Gateway_light-bg.svg',
    'spaceone:is_major': 'false',
}

cst_igw._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Internet Gateway ID', 'data.internet_gateway_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available', 'attached'],
        'warning': ['attaching', 'detaching'],
        'disable': ['detached']
    }),
    ListDyField.data_source('VPC ID', 'data.attachments', default_badge={
        'type': 'outline',
        'sub_key': 'vpc_id',
    })
])


cst_eoigw = CloudServiceTypeResource()
cst_eoigw.name = 'EgressOnlyInternetGateway'
cst_eoigw.provider = 'aws'
cst_eoigw.group = 'VPC'
cst_eoigw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Internet-Gateway_light-bg.svg',
    'spaceone:is_major': 'false',
}
cst_eoigw._metadata = CloudServiceTypeMeta.set_fields(fields=[
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

])


cst_natgw = CloudServiceTypeResource()
cst_natgw.name = 'NATGateway'
cst_natgw.provider = 'aws'
cst_natgw.group = 'VPC'
cst_natgw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_NAT-Gateway_light-bg.svg',
    'spaceone:is_major': 'false',
}
cst_natgw._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


cst_peerconn = CloudServiceTypeResource()
cst_peerconn.name = 'PeeringConnection'
cst_peerconn.provider = 'aws'
cst_peerconn.group = 'VPC'
cst_peerconn.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Peering_light-bg.svg',
    'spaceone:is_major': 'false',
}
cst_peerconn._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


cst_nacl = CloudServiceTypeResource()
cst_nacl.name = 'NetworkACL'
cst_nacl.provider = 'aws'
cst_nacl.group = 'VPC'
cst_nacl.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_NACL_light-bg.svg',
    'spaceone:is_major': 'false',
}
cst_nacl._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Network ACL ID', 'data.network_acl_id'),
    EnumDyField.data_source('Default', 'data.is_default', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
])

cst_endpoint = CloudServiceTypeResource()
cst_endpoint.name = 'Endpoint'
cst_endpoint.provider = 'aws'
cst_endpoint.group = 'VPC'
cst_endpoint.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Endpoints_light-bg.svg',
    'spaceone:is_major': 'false',
}
cst_endpoint._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])

cst_transitgw = CloudServiceTypeResource()
cst_transitgw.name = 'TransitGateway'
cst_transitgw.provider = 'aws'
cst_transitgw.group = 'VPC'
cst_transitgw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Transit_Gateway.svg',
    'spaceone:is_major': 'false',
}
cst_transitgw._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Transit Gateway ID', 'data.transit_gateway_id'),
    TextDyField.data_source('Owner ID', 'data.owner_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'modifying', 'deleting'],
        'disable': ['deleted']
    })
])

cst_customgw = CloudServiceTypeResource()
cst_customgw.name = 'CustomerGateway'
cst_customgw.provider = 'aws'
cst_customgw.group = 'VPC'
cst_customgw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_Customer-Gateway_dark-bg.svg',
    'spaceone:is_major': 'false',
}
cst_customgw._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])

cst_vpnconn = CloudServiceTypeResource()
cst_vpnconn.name = 'VPNConnection'
cst_vpnconn.provider = 'aws'
cst_vpnconn.group = 'VPC'
cst_vpnconn.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Connection_dark-bg.svg',
    'spaceone:is_major': 'false',
}
cst_vpnconn._metadata = CloudServiceTypeMeta.set_fields(fields=[
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

])

cst_vpngw = CloudServiceTypeResource()
cst_vpngw.name = 'VPNGateway'
cst_vpngw.provider = 'aws'
cst_vpngw.group = 'VPC'
cst_vpngw.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Gateway_dark-bg.svg',
    'spaceone:is_major': 'false',
}
cst_vpngw._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('ID', 'data.vpn_gateway_id'),
    TextDyField.data_source('State', 'data.state'),
    TextDyField.data_source('Type', 'data.type'),
    ListDyField.data_source('VPC', 'data.vpc_attachments', default_badge={
        'type': 'outline',
        'sub_key': 'vpc_id',
    }),
    TextDyField.data_source('ASN (Amazon side)', 'data.amazon_side_asn'),
])

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
