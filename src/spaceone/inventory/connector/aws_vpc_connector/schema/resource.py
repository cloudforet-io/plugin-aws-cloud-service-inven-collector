from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_vpc_connector.schema.data import VPC, Subnet, RouteTable, InternetGateway, \
    EgressOnlyInternetGateway, Endpoint, NATGateway, PeeringConnection, NetworkACL, TransitGateway, CustomerGateway, \
    VPNConnection, VPNGateway
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField, \
    BadgeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout

# VPC
vpc = ItemDynamicLayout.set_fields('VPC', fields=[
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending']
    }),
    TextDyField.data_source('IPv4 CIDR', 'data.cidr_block'),
    ListDyField.data_source('IPv6 CIDR', 'data.ipv6_cidr_block_association_set', default_badge={
        'type': 'outline',
        'sub_key': 'ipv6_cidr_block'
    }),
    EnumDyField.data_source('DNS resolution', 'data.enable_dns_support', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    }),
    EnumDyField.data_source('DNS hostnames', 'data.enable_dns_hostnames', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    }),
    TextDyField.data_source('DHCP Options set', 'data.dhcp_options_id'),
    BadgeDyField.data_source('Tenancy', 'data.instance_tenancy'),
    EnumDyField.data_source('Default VPC', 'data.is_default', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Owner', 'data.owner_id'),
])

vpc_subnet = TableDynamicLayout.set_fields('Subnet', 'data.subnets', fields=[
    TextDyField.data_source('Subnet ID', 'subnet_id'),
    EnumDyField.data_source('State', 'state', default_state={
        'safe': ['available'],
        'warning': ['pending']
    }),
    TextDyField.data_source('IPv4 CIDR', 'cidr_block'),
    TextDyField.data_source('Availability Zone', 'availability_zone'),
    EnumDyField.data_source('Auto-assign Public IP', 'map_public_ip_on_launch', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

vpc_igw = ItemDynamicLayout.set_fields('Internet Gateway', fields=[
    TextDyField.data_source('Internet Gateway ID', 'data.internet_gateway.internet_gateway_id'),
    EnumDyField.data_source('State', 'data.internet_gateway.state', default_state={
        'safe': ['attached', 'available'],
        'warning': ['attaching', 'detaching'],
        'disable': ['detached']
    })
])

vpc_natgw = TableDynamicLayout.set_fields('NAT Gateway', 'data.nat_gateways', fields=[
    TextDyField.data_source('NAT Gateway ID', 'nat_gateway_id'),
    EnumDyField.data_source('Status', 'state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'alert': ['failed'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Subnet', 'subnet_id'),
])

vpc_endpoints = TableDynamicLayout.set_fields('Endpoint', 'data.endpoints', fields=[
    TextDyField.data_source('Endpoint ID', 'vpc_endpoint_id'),
    EnumDyField.data_source('Status', 'state', default_state={
        'safe': ['available'],
        'warning': ['pendingAcceptance', 'pending', 'deleting'],
        'disable': ['deleted'],
        'alert': ['rejected', 'failed', 'expired']
    }),
    TextDyField.data_source('Service Name', 'service_name'),
    EnumDyField.data_source('Endpoint Type', 'vpc_endpoint_type', default_outline_badge=['Interface', 'Gateway']),
])

vpc_peercon = TableDynamicLayout.set_fields('Peering Connection', 'data.peering_connections', fields=[
    TextDyField.data_source('Peering Connection ID', 'data.vpc_peering_connection_id'),
    EnumDyField.data_source('Status', 'data.status.code', default_state={
        'safe': ['active'],
        'warning': ['initiating-request', 'pending-acceptance', 'provisioning', 'deleting'],
        'disable': ['deleted'],
        'alert': ['rejected', 'failed', 'expired']
    }),
])

vpc_egress_gw = ItemDynamicLayout.set_fields('Egress Only Internet Gateway', 'data.egress_only_internet_gateway',
                                             fields=[
                                                 TextDyField.data_source('Egress Only Internet Gateway ID',
                                                                         'data.egress_only_internet_gateway_id'),
                                                 ListDyField.data_source('State', 'data.attachments', default_badge={
                                                     'type': 'inline',
                                                     'sub_key': 'state'
                                                 }),
                                             ])

vpn_gw = ItemDynamicLayout.set_fields('VPN Gateway', fields=[
    TextDyField.data_source('Name', 'data.vpn_gateway.name'),
    TextDyField.data_source('ID', 'data.vpn_gateway.vpn_gateway_id'),
    TextDyField.data_source('State', 'data.vpn_gateway.state'),
    TextDyField.data_source('Type', 'data.vpn_gateway.type'),
    ListDyField.data_source('VPC', 'data.vpn_gateway.vpc_attachments', default_badge={
        'type': 'outline',
        'sub_key': 'vpc_id',
    }),
    TextDyField.data_source('ASN (Amazon side)', 'data.vpn_gateway.amazon_side_asn'),
])

vpc_transit_gw = ItemDynamicLayout.set_fields('Transit Gateway', fields=[
    TextDyField.data_source('Name', 'data.transit_gateway.name'),
    TextDyField.data_source('Transit Gateway ID', 'data.transit_gateway.transit_gateway_id'),
    TextDyField.data_source('Owner Account ID', 'data.transit_gateway.owner_id'),
    EnumDyField.data_source('State', 'data.transit_gateway.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'modifying', 'deleting'],
        'disable': ['deleted']
    }),
    EnumDyField.data_source('DNS Support', 'data.transit_gateway.options.dns_support', default_badge={
        'indigo.500': ['enable'], 'coral.600': ['disable']
    }),
    EnumDyField.data_source('VPN ECMP support', 'data.transit_gateway.options.vpn_ecmp_support', default_badge={
        'indigo.500': ['enable'], 'coral.600': ['disable']
    }),
    EnumDyField.data_source('Auto accept shared', 'data.transit_gateway.options.auto_accept_shared_attachments', default_badge={
        'indigo.500': ['enable'], 'coral.600': ['disable']
    }),
    EnumDyField.data_source('Default association route table',
                            'data.transit_gateway.options.default_route_table_association',
                            default_badge={'indigo.500': ['enable'], 'coral.600': ['disable']}),
    TextDyField.data_source('Association route table ID',
                            'data.transit_gateway.options.association_default_route_table_id'),
    EnumDyField.data_source('Default propagation route table',
                            'data.transit_gateway.options.default_route_table_propagation',
                            default_badge={'indigo.500': ['enable'], 'coral.600': ['disable']}),
    TextDyField.data_source('Propagation route table ID',
                            'data.transit_gateway.options.propagation_default_route_table_id'),
])

vpc_tags = SimpleTableDynamicLayout.set_tags()
vpc_metadata = CloudServiceMeta.set_layouts(layouts=[vpc, vpc_subnet, vpc_igw, vpc_natgw, vpc_endpoints,
                                                     vpc_peercon, vpc_egress_gw, vpn_gw, vpc_transit_gw, vpc_tags])


# SUBNET
subnet = ItemDynamicLayout.set_fields('Subnet', fields=[
    TextDyField.data_source('Subnet ID', 'data.subnet_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending']
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('IPv4 CIDR', 'data.cidr_block'),
    TextDyField.data_source('Available IPv4 Address', 'data.available_ip_address_count'),
    ListDyField.data_source('IPv6 CIDR', 'data.ipv6_cidr_block_association_set', default_badge={
        'sub_key': 'ipv6_cidr_block'
    }),
    TextDyField.data_source('Availability Zone', 'data.availability_zone'),
    TextDyField.data_source('Route Table', 'data.route_table.route_table_id'),
    EnumDyField.data_source('Subnet Type', 'data.subnet_type', default_badge={
        'indigo.500': ['public'], 'coral.600': ['private']
    }),
    TextDyField.data_source('Network ACL', 'data.network_acl.network_acl_id'),
    EnumDyField.data_source('Default', 'data.default_for_az', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Auto-assign Public IP', 'data.map_public_ip_on_launch', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Auto-assign IPv6', 'data.assign_ipv6_address_on_creation', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

subnet_rt = TableDynamicLayout.set_fields('Route Table', 'data.route_table.routes', fields=[
    TextDyField.data_source('Destination', 'destination_cidr_block'),
    TextDyField.data_source('Target', 'target'),
    EnumDyField.data_source('Status', 'state', default_state={
        'safe': ['active'],
    }),
])

subnet_nacl = TableDynamicLayout.set_fields('Network ACL', 'data.network_acl.entries', fields=[
    EnumDyField.data_source('Direction', 'direction', default_badge={
        'indigo.500': ['inbound'], 'coral.600': ['outbound']
    }),
    TextDyField.data_source('#', 'rule_number'),
    TextDyField.data_source('Protocol', 'protocol_display'),
    TextDyField.data_source('Port Range / ICMP Type', 'port_range_display'),
    TextDyField.data_source('Source', 'cidr_block'),
    EnumDyField.data_source('Allow / Deny', 'rule_action', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
])

subnet_tags = SimpleTableDynamicLayout.set_tags()
subnet_metadata = CloudServiceMeta.set_layouts(layouts=[subnet, subnet_rt, subnet_nacl, subnet_tags])


# ROUTE
rt = ItemDynamicLayout.set_fields('Route Tables', fields=[
    TextDyField.data_source('Route Table ID', 'data.route_table_id'),
    ListDyField.data_source('Explicitly Associate with', 'data.subnet_associations', default_badge={
        'sub_key': 'subnet_id',
        'type': 'outline',
    }),
    EnumDyField.data_source('Main', 'data.main', default_badge={
        'indigo.500': ['Yes'], 'coral.600': ['No']
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
])

rt_routes = TableDynamicLayout.set_fields('Routes', 'data.routes', fields=[
    TextDyField.data_source('Destination', 'destination_cidr_block'),
    TextDyField.data_source('Target', 'target'),
    EnumDyField.data_source('Status', 'state', default_state={
        'safe': ['active'],
        'alert': ['backhole']
    }),
])

rt_subnet_assoc = TableDynamicLayout.set_fields('Subnet Associations', 'data.subnet_associations', fields=[
    TextDyField.data_source('Subnet ID', 'subnet_id'),
    EnumDyField.data_source('State', 'association_state.state', default_state={
        'safe': ['associated'],
        'warning': ['associating', 'disassociating', ''],
        'alert': ['failed'],
        'disable': ['disassociated']
    }),
    TextDyField.data_source('Route Table ID', 'route_table_id'),
    TextDyField.data_source('Route Table Association ID', 'route_table_association_id'),
])

rt_edge_assoc = TableDynamicLayout.set_fields('Edge Assocations', 'data.edge_associations', fields=[
    TextDyField.data_source('Gateway ID', 'gateway_id'),
    EnumDyField.data_source('State', 'association_state.state', default_state={
        'safe': ['associated'],
        'warning': ['associating', 'disassociating', ''],
        'alert': ['failed'],
        'disable': ['disassociated']
    }),
    TextDyField.data_source('Route Table ID', 'route_table_id'),
    TextDyField.data_source('Route Table Association ID', 'route_table_association_id'),
])

rt_tags = SimpleTableDynamicLayout.set_tags()
rt_metadata = CloudServiceMeta.set_layouts(layouts=[rt, rt_routes, rt_subnet_assoc, rt_edge_assoc, rt_tags])


# Internet Gateway
igw = ItemDynamicLayout.set_fields('Internet Gateway', fields=[
    TextDyField.data_source('Internet Gateway ID', 'data.internet_gateway_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available', 'attached'],
        'warning': ['attaching', 'detaching'],
        'disable': ['detached']
    }),
    ListDyField.data_source('VPC ID', 'data.attachments', options={
        'sub_key': 'vpc_id'
    }),
])

igw_tags = SimpleTableDynamicLayout.set_tags()
igw_metadata = CloudServiceMeta.set_layouts(layouts=[igw, igw_tags])


# Egress Only Internet Gateway
eoigw = ItemDynamicLayout.set_fields('Egress Only Internet Gateway', fields=[
    TextDyField.data_source('Egress Only Internet Gateway ID', 'data.egress_only_internet_gateway_id'),
    ListDyField.data_source('State', 'data.attachments', default_badge={
        'type': 'inline',
        'sub_key': 'state'
    }),
    ListDyField.data_source('VPC ID', 'data.attachments', options={
        'sub_key': 'vpc_id'
    })
])
eoigw_tags = SimpleTableDynamicLayout.set_tags()
eoigw_metadata = CloudServiceMeta.set_layouts(layouts=[eoigw, eoigw_tags])

# ENDPOINT
ep = ItemDynamicLayout.set_fields('Endpoints', fields=[
    TextDyField.data_source('Endpoint ID', 'data.vpc_endpoint_id'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pendingAcceptance', 'pending', 'deleting'],
        'disable': ['deleted'],
        'alert': ['rejected', 'failed', 'expired']
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('Service Name', 'data.service_name'),
    EnumDyField.data_source('Endpoint Type', 'data.vpc_endpoint_type', default_outline_badge=['Gateway', 'Interface']),
    ListDyField.data_source('DNS Names', 'data.dns_entries', default_badge={
        'type': 'outline',
        'sub_key': 'dns_name',
    }),
    EnumDyField.data_source('Private DNS Names enabled', 'data.private_dns_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

ep_tags = SimpleTableDynamicLayout.set_tags()
ep_metadata = CloudServiceMeta.set_layouts(layouts=[ep, ep_tags])

# NAT GATEWAY
natgw = ItemDynamicLayout.set_fields('NAT Gateway', fields=[
    TextDyField.data_source('NAT Gateway ID', 'data.nat_gateway_id'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'alert': ['failed'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Status Message', 'data.failure_message'),
    ListDyField.data_source('Elastic IP', 'data.nat_gateway_addresses', default_badge={
        'type': 'outline',
        'sub_key': 'public_ip',
    }),
    ListDyField.data_source('Private IP', 'data.nat_gateway_addresses', default_badge={
        'type': 'outline',
        'sub_key': 'private_ip',
    }),
    ListDyField.data_source('Network Interface', 'data.nat_gateway_addresses', default_badge={
        'type': 'outline',
        'sub_key': 'network_interface_id',
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('Subnet', 'data.subnet_id'),
    DateTimeDyField.data_source('Created', 'data.create_time'),
])

natgw_tags = SimpleTableDynamicLayout.set_tags()
natgw_metadata = CloudServiceMeta.set_layouts(layouts=[natgw, natgw_tags])

# PEERING CONNECTION
peercon = ItemDynamicLayout.set_fields('Peering Connection', fields=[
    TextDyField.data_source('Peering Connection ID', 'data.vpc_peering_connection_id'),
    EnumDyField.data_source('Status', 'data.status.code', default_state={
        'safe': ['active'],
        'warning': ['initiating-request', 'pending-acceptance', 'provisioning', 'deleting'],
        'disable': ['deleted'],
        'alert': ['rejected', 'failed', 'expired']
    }),
    DateTimeDyField.data_source('Expiration Time', 'data.expiration_time'),
])

peercon_requester = ItemDynamicLayout.set_fields('Requester', fields=[
    TextDyField.data_source('Requester VPC', 'data.requester_vpc_info.vpc_id'),
    TextDyField.data_source('Requester VPC CIDR', 'data.requester_vpc_info.cidr_block'),
    TextDyField.data_source('Requester Owner', 'data.requester_vpc_info.owner_id'),
    TextDyField.data_source('Requester VPC Region', 'data.requester_vpc_info.region'),
])

peercon_accepter = ItemDynamicLayout.set_fields('Accepter', fields=[
    TextDyField.data_source('Accepter VPC', 'data.accepter_vpc_info.vpc_id'),
    TextDyField.data_source('Accepter VPC CIDR', 'data.accepter_vpc_info.cidr_block'),
    TextDyField.data_source('Accepter Owner', 'data.accepter_vpc_info.owner_id'),
    TextDyField.data_source('Accepter VPC Region', 'data.accepter_vpc_info.region'),
])

peercon_tags = SimpleTableDynamicLayout.set_tags()
pc_metadata = CloudServiceMeta.set_layouts(layouts=[peercon, peercon_requester, peercon_accepter, peercon_tags])

# NETWORK ACL
nacl = ItemDynamicLayout.set_fields('Network ACL', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Network ACL ID', 'data.network_acl_id'),
    EnumDyField.data_source('Default', 'data.is_default', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
])

nacl_inbound = TableDynamicLayout.set_fields('Inbound Rules', 'data.inbound_entries', fields=[
    TextDyField.data_source('Rule #', 'rule_number'),
    EnumDyField.data_source('Protocol', 'protocol_display',
                            default_outline_badge=['ALL', 'TCP', 'UDP', 'ICMP', 'ICMPv6']),
    TextDyField.data_source('Port Range', 'port_range_display'),
    TextDyField.data_source('Source', 'cidr_block'),
    EnumDyField.data_source('Allow / Deny', 'rule_action', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
])

nacl_outbound = TableDynamicLayout.set_fields('Outbound Rules', 'data.outbound_entries', fields=[
    TextDyField.data_source('Rule #', 'rule_number'),
    EnumDyField.data_source('Protocol', 'protocol_display',
                            default_outline_badge=['ALL', 'TCP', 'UDP', 'ICMP', 'ICMPv6']),
    TextDyField.data_source('Port Range', 'port_range_display'),
    TextDyField.data_source('Source', 'cidr_block'),
    EnumDyField.data_source('Allow / Deny', 'rule_action', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
])

nacl_subnet_assoc = TableDynamicLayout.set_fields('Subnet Associations', 'data.associations', fields=[
    TextDyField.data_source('Subnet ID', 'subnet_id')
])

nacl_tag = SimpleTableDynamicLayout.set_tags()
nacl_metadata = CloudServiceMeta.set_layouts(layouts=[nacl, nacl_inbound, nacl_outbound, nacl_subnet_assoc, nacl_tag])


# TRANSIT GATEWAY
transitgw = ItemDynamicLayout.set_fields('Transit Gateway', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Transit Gateway ID', 'data.transit_gateway_id'),
    TextDyField.data_source('Owner Account ID', 'data.owner_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'modifying', 'deleting'],
        'disable': ['deleted']
    }),
    EnumDyField.data_source('DNS Support', 'data.options.dns_support', default_badge={
        'indigo.500': ['enable'], 'coral.600': ['disable']
    }),
    EnumDyField.data_source('VPN ECMP support', 'data.options.vpn_ecmp_support', default_badge={
        'indigo.500': ['enable'], 'coral.600': ['disable']
    }),
    EnumDyField.data_source('Auto accept shared', 'data.options.auto_accept_shared_attachments', default_badge={
        'indigo.500': ['enable'], 'coral.600': ['disable']
    }),
    EnumDyField.data_source('Default association route table', 'data.options.default_route_table_association',
                            default_badge={'indigo.500': ['enable'], 'coral.600': ['disable']}),
    TextDyField.data_source('Association route table ID', 'data.options.association_default_route_table_id'),
    EnumDyField.data_source('Default propagation route table', 'data.options.default_route_table_propagation',
                            default_badge={'indigo.500': ['enable'], 'coral.600': ['disable']}),
    TextDyField.data_source('Propagation route table ID', 'data.options.propagation_default_route_table_id'),
])

transitgw_vpn_conn = TableDynamicLayout.set_fields('VPN Connections', 'data.vpn_connections', fields=[
    TextDyField.data_source('name', 'name'),
    TextDyField.data_source('VPN ID', 'vpn_connection_id'),
    EnumDyField.data_source('State', 'state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Virtual Private Gateway', 'vpn_gateway_id'),
    TextDyField.data_source('Transit Gateway', 'transit_gateway_id'),
    TextDyField.data_source('Customer Gateway', 'customer_gateway_id'),
    TextDyField.data_source('Customer Gateway Address', 'customer_gateway_address'),
    TextDyField.data_source('Type', 'type'),
    EnumDyField.data_source('Category', 'category', default_badge={
        'indigo.500': ['VPN'], 'coral.500': ['VPN-Classic']
    }),
])

transitgw_tag = SimpleTableDynamicLayout.set_tags()
transitgw_metadata = CloudServiceMeta.set_layouts(layouts=[transitgw, transitgw_vpn_conn, transitgw_tag])


# CUSTOMER GATEWAY
customergw = ItemDynamicLayout.set_fields('Customer Gateway', fields=[
    TextDyField.data_source('ID', 'data.customer_gateway_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Type', 'data.type'),
    TextDyField.data_source('IP Address', 'data.ip_address'),
    TextDyField.data_source('BGP ASN', 'data.bgp_asn'),
    TextDyField.data_source('Device', 'data.device_name'),
    TextDyField.data_source('Certificate ARN', 'data.certificate_arn'),
])

customergw_vpn_conn = ItemDynamicLayout.set_fields('VPN Connection', fields=[
    TextDyField.data_source('name', 'data.vpn_connection.name'),
    TextDyField.data_source('VPN ID', 'data.vpn_connection.vpn_connection_id'),
    EnumDyField.data_source('State', 'data.vpn_connection.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Virtual Private Gateway', 'data.vpn_connection.vpn_gateway_id'),
    TextDyField.data_source('Transit Gateway', 'data.vpn_connection.transit_gateway_id'),
    TextDyField.data_source('Customer Gateway', 'data.vpn_connection.customer_gateway_id'),
    TextDyField.data_source('Customer Gateway Address', 'data.vpn_connection.customer_gateway_address'),
    TextDyField.data_source('Type', 'data.vpn_connection.type'),
    EnumDyField.data_source('Category', 'data.vpn_connection.category', default_badge={
        'indigo.500': ['VPN'], 'coral.500': ['VPN-Classic']
    }),
])

customergw_tag = SimpleTableDynamicLayout.set_tags()
customergw_metadata = CloudServiceMeta.set_layouts(layouts=[customergw, customergw_vpn_conn, customergw_tag])


# VPN GATEWAY
vpngw = ItemDynamicLayout.set_fields('Virtual Private Gateway', fields=[
    TextDyField.data_source('ID', 'data.vpn_gateway_id'),
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Type', 'data.type'),
    ListDyField.data_source('VPC', 'data.vpc_attachments', default_badge={
        'type': 'outline',
        'sub_key': 'vpc_id',
    }),
    TextDyField.data_source('ASN (Amazon side)', 'data.amazon_side_asn'),
])

vpngw_vpn_conn = ItemDynamicLayout.set_fields('VPN Connection', fields=[
    TextDyField.data_source('name', 'data.vpn_connection.name'),
    TextDyField.data_source('VPN ID', 'data.vpn_connection.vpn_connection_id'),
    EnumDyField.data_source('State', 'data.vpn_connection.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Virtual Private Gateway', 'data.vpn_connection.vpn_gateway_id'),
    TextDyField.data_source('Transit Gateway', 'data.vpn_connection.transit_gateway_id'),
    TextDyField.data_source('Customer Gateway', 'data.vpn_connection.customer_gateway_id'),
    TextDyField.data_source('Customer Gateway Address', 'data.vpn_connection.customer_gateway_address'),
    TextDyField.data_source('Type', 'data.vpn_connection.type'),
    EnumDyField.data_source('Category', 'data.vpn_connection.category', default_badge={
        'indigo.500': ['VPN'], 'coral.500': ['VPN-Classic']
    }),
])
vpngw_tag = SimpleTableDynamicLayout.set_tags()
vpngw_metadata = CloudServiceMeta.set_layouts(layouts=[vpngw, vpngw_vpn_conn, vpngw_tag])


# VPN CONNECTION
vpnconn = ItemDynamicLayout.set_fields('VPN Connection', fields=[
    TextDyField.data_source('VPN ID', 'data.vpn_connection_id'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['available'],
        'warning': ['pending', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Virtual Private Gateway', 'data.vpn_gateway_id'),
    TextDyField.data_source('Customer Gateway', 'data.customer_gateway_id'),
    TextDyField.data_source('Customer Gateway Address', 'data.customer_gateway_address'),
    TextDyField.data_source('Transit Gateway', 'data.transit_gateway_id'),
    TextDyField.data_source('Type', 'data.type'),
    TextDyField.data_source('Category', 'data.category'),
    EnumDyField.data_source('Static Routing Only', 'data.options.static_routes_only', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Enable Acceleration', 'data.options.enable_acceleration', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

vpnconn_tunnel = TableDynamicLayout.set_fields('VPN Tunnel', 'data.vgw_telemetry', fields=[
    TextDyField.data_source('Outside IP Address', 'outside_ip_address'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['UP'],
        'alert': ['DOWN']
    }),
    DateTimeDyField.data_source('Status Last Changed', 'last_status_change'),
    TextDyField.data_source('Certificate ARN', 'certificate_arn'),
])

vpnconn_tag = SimpleTableDynamicLayout.set_tags()
vpnconn_metadata = CloudServiceMeta.set_layouts(layouts=[vpnconn, vpnconn_tunnel, vpnconn_tag])


class VPCResource(CloudServiceResource):
    cloud_service_group = StringType(default='VPC')


# Resource
class VPCResource(VPCResource):
    cloud_service_type = StringType(default='VPC')
    data = ModelType(VPC)
    _metadata = ModelType(CloudServiceMeta, default=vpc_metadata, serialized_name='metadata')


class SubnetResource(VPCResource):
    cloud_service_type = StringType(default='Subnet')
    data = ModelType(Subnet)
    _metadata = ModelType(CloudServiceMeta, default=subnet_metadata, serialized_name='metadata')


class RouteTableResource(VPCResource):
    cloud_service_type = StringType(default='RouteTable')
    data = ModelType(RouteTable)
    _metadata = ModelType(CloudServiceMeta, default=rt_metadata, serialized_name='metadata')


class InternetGatewayResource(VPCResource):
    cloud_service_type = StringType(default='InternetGateway')
    data = ModelType(InternetGateway)
    _metadata = ModelType(CloudServiceMeta, default=igw_metadata, serialized_name='metadata')


class EgressOnlyInternetGatewayResource(VPCResource):
    cloud_service_type = StringType(default='EgressOnlyInternetGateway')
    data = ModelType(EgressOnlyInternetGateway)
    _metadata = ModelType(CloudServiceMeta, default=eoigw_metadata, serialized_name='metadata')


class EndpointResource(VPCResource):
    cloud_service_type = StringType(default='Endpoint')
    data = ModelType(Endpoint)
    _metadata = ModelType(CloudServiceMeta, default=ep_metadata, serialized_name='metadata')


class NATGatewayResource(VPCResource):
    cloud_service_type = StringType(default='NATGateway')
    data = ModelType(NATGateway)
    _metadata = ModelType(CloudServiceMeta, default=natgw_metadata, serialized_name='metadata')


class PeeringConnectionResource(VPCResource):
    cloud_service_type = StringType(default='PeeringConnection')
    data = ModelType(PeeringConnection)
    _metadata = ModelType(CloudServiceMeta, default=pc_metadata, serialized_name='metadata')


class NetworkACLResource(VPCResource):
    cloud_service_type = StringType(default='NetworkACL')
    data = ModelType(NetworkACL)
    _metadata = ModelType(CloudServiceMeta, default=nacl_metadata, serialized_name='metadata')


class TransitGatewayResource(VPCResource):
    cloud_service_type = StringType(default='TransitGateway')
    data = ModelType(TransitGateway)
    _metadata = ModelType(CloudServiceMeta, default=transitgw_metadata, serialized_name='metadata')


class CustomerGatewayResource(VPCResource):
    cloud_service_type = StringType(default='CustomerGateway')
    data = ModelType(CustomerGateway)
    _metadata = ModelType(CloudServiceMeta, default=customergw_metadata, serialized_name='metadata')


class VPNGatewayResource(VPCResource):
    cloud_service_type = StringType(default='VPNGateway')
    data = ModelType(VPNGateway)
    _metadata = ModelType(CloudServiceMeta, default=vpngw_metadata, serialized_name='metadata')


class VPNConnectionResource(VPCResource):
    cloud_service_type = StringType(default='VPNConnection')
    data = ModelType(VPNConnection)
    _metadata = ModelType(CloudServiceMeta, default=vpnconn_metadata, serialized_name='metadata')



# Response
class VPCResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.vpc_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(VPCResource)


class SubnetResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.subnet_arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(SubnetResource)


class RouteTableResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.route_table_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(RouteTableResource)


class InternetGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.internet_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(InternetGatewayResource)


class EgressOnlyInternetGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.egress_only_internet_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(EgressOnlyInternetGatewayResource)


class EndpointResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.vpc_endpoint_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(EndpointResource)


class NATGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.nat_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(NATGatewayResource)


class PeeringConnectionResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.vpc_peering_connection_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(PeeringConnectionResource)


class NetworkACLResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.network_acl_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(NetworkACLResource)


class TransitGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.transit_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(TransitGatewayResource)


class CustomerGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.customer_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(CustomerGatewayResource)


class VPNGatewayResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.vpn_gateway_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(VPNGatewayResource)


class VPNConnectionResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.vpn_connection_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(VPNConnectionResource)
