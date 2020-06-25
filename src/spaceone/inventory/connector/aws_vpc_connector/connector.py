import time
import logging
from typing import List

from spaceone.inventory.connector.aws_vpc_connector.schema.data import VPC, Subnet, RouteTable, \
    RouteTableAssociations, RouteTableRoutes, InternetGateway, EgressOnlyInternetGateway, DHCPOptions, Endpoint, \
    NATGateway, PeeringConnection, NetworkACL, NetworkACLEntries, NetworkACLTotalEntries, TransitGateway, \
    CustomerGateway, VPNGateway, VPNConnection
from spaceone.inventory.connector.aws_vpc_connector.schema.resource import VPCResource, VPCResponse, SubnetResource, \
    SubnetResponse, InternetGatewayResource, InternetGatewayResponse, EgressOnlyInternetGatewayResource, \
    EgressOnlyInternetGatewayResponse, EndpointResource, EndpointResponse, NATGatewayResource, NATGatewayResponse, \
    PeeringConnectionResource, PeeringConnectionResponse, NetworkACLResource, NetworkACLResponse, \
    RouteTableResource, RouteTableResponse, TransitGatewayResource, TransitGatewayResponse, CustomerGatewayResource, \
    CustomerGatewayResponse, VPNGatewayResource, VPNGatewayResponse, VPNConnectionResource, VPNConnectionResponse
from spaceone.inventory.connector.aws_vpc_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)
PROTOCOL_NUMBER_INFO = {'0': 'HOPOPT', '1': 'ICMP', '2': 'IGMP', '3': 'GGP', '4': 'IPv4', '5': 'ST', '6': 'TCP',
                        '7': 'CBT', '8': 'EGP', '9': 'IGP', '10': 'BBN-RCC-MON', '11': 'NVP-II', '12': 'PUP',
                        '13': 'ARGUS', '14': 'EMCON', '15': 'XNET', '16': 'CHAOS', '17': 'UDP', '18': 'MUX',
                        '19': 'DCN-MEAS', '20': 'HMP', '21': 'PRM', '22': 'XNS-IDP', '23': 'TRUNK-1', '24': 'TRUNK-2',
                        '25': 'LEAF-1', '26': 'LEAF-2', '27': 'RDP', '28': 'IRTP', '29': 'ISO-TP4', '30': 'NETBLT',
                        '31': 'MFE-NSP', '32': 'MERIT-INP', '33': 'DCCP', '34': '3PC', '35': 'IDPR', '36': 'XTP',
                        '37': 'DDP', '38': 'IDPR-CMTP', '39': 'TP++', '40': 'IL', '41': 'IPv6', '42': 'SDRP',
                        '43': 'IPv6-Route', '44': 'IPv6-Frag', '45': 'IDRP', '46': 'RSVP', '47': 'GRE', '48': 'DSR',
                        '49': 'BNA', '50': 'ESP', '51': 'AH', '52': 'I-NLSP', '53': 'SWIPE', '54': 'NARP',
                        '55': 'MOBILE', '56': 'TLSP', '58': 'IPv6-ICMP', '59': 'IPv6-NoNxt', '60': 'IPv6-Opts',
                        '61': '61', '62': 'CFTP', '63': '63', '64': 'SAT-EXPAK', '65': 'KRYPTOLAN', '66': 'RVD',
                        '67': 'IPPC', '68': '68', '69': 'SAT-MON', '70': 'VISA', '71': 'IPCV', '72': 'CPNX',
                        '73': 'CPHB', '74': 'WSN', '75': 'PVP', '76': 'BR-SAT-MON', '77': 'SUN-ND', '78': 'WB-MON',
                        '79': 'WB-EXPAK', '80': 'ISO-IP', '81': 'VMTP', '82': 'SECURE-VMTP', '83': 'VINES', '84': 'IPTM',
                        '85': 'NSFNET-IGP', '86': 'DGP', '87': 'TCF', '88': 'EIGRP', '89': 'OSPFIGP', '90': 'Sprite-RPC',
                        '91': 'LARP', '92': 'MTP', '93': 'AX.25', '94': 'IPIP','95': 'MICP', '96': 'SCC-SP',
                        '97': 'ETHERIP', '98': 'ENCAP', '99': '99', '100': 'GMTP', '101': 'IFMP', '102': 'PNNI',
                        '103': 'PIM', '104': 'ARIS', '105': 'SCPS', '106': 'QNX', '107': 'A/N', '108': 'IPComp',
                        '109': 'SNP', '110': 'Compaq-Peer', '111': 'IPX-in-IP', '112': 'VRRP', '113': 'PGM',
                        '114': '114', '115': 'L2TP', '116': 'DDX', '117': 'IATP', '118': 'STP', '119': 'SRP',
                        '120': 'UTI', '121': 'SMP', '122': 'SM', '123': 'PTP', '124': 'ISIS over IPv4', '125': 'FIRE',
                        '126': 'CRTP', '127': 'CRUDP', '128': 'SSCOPMCE', '129': 'IPLT', '130': 'SPS', '131': 'PIPE',
                        '132': 'SCTP', '133': 'FC', '134': 'RSVP-E2E-IGNORE', '135': 'Mobility Header',
                        '136': 'UDPLite', '137': 'MPLS-in-IP', '138': 'manet', '139': 'HIP', '140': 'Shim6',
                        '141': 'WESP', '142': 'ROHC', '253': '253', '254': '254', '-1': 'ALL'}


class VPCConnector(SchematicAWSConnector):
    vpc_res_schema = VPCResponse
    subnet_res_schema = SubnetResponse
    rtable_res_schema = RouteTableResponse
    igw_res_schema = InternetGatewayResponse
    eoigw_res_schema = EgressOnlyInternetGatewayResponse
    endpoint_res_schema = EndpointResponse
    natgw_res_schema = NATGatewayResponse
    peercon_res_schema = PeeringConnectionResponse
    netacl_res_schema = NetworkACLResponse
    transitgw_res_schema = TransitGatewayResponse
    customergw_res_schema = CustomerGatewayResponse
    vpngw_res_schema = VPNGatewayResponse
    vpnconn_res_schema = VPNConnectionResponse

    service_name = 'ec2'

    customer_gateways = None
    vpn_gateways = None
    vpn_connections = None
    transit_gateways = None
    peering_connections = None
    nat_gateways = None
    network_acls = None
    endpoints = None
    egress_only_internet_gateways = None
    internet_gateways = None
    route_tables = None
    subnets = None
    dhcp_options = None
    vpcs = []
    vpc_ids = []

    include_default = False

    def get_resources(self):
        resources = []
        start_time = time.time()

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # Region
        for region_name in self.region_names:
            self.reset_region(region_name)

            self.customer_gateways = []
            self.transit_gateways = []
            self.vpn_gateways = []
            self.vpn_connections = []
            self.peering_connections = []
            self.nat_gateways = []
            self.network_acls = []
            self.endpoints = []
            self.egress_only_internet_gateways = []
            self.internet_gateways = []
            self.route_tables = []
            self.subnets = []
            self.dhcp_options = []

            # VPC
            self.vpcs = self.list_vpcs()
            self.vpc_ids = [vpc.get('VpcId') for vpc in self.vpcs]

            # VPN Connection
            for data in self.request_vpn_connection_data(region_name):
                resources.append(self.vpnconn_res_schema(
                    {'resource': VPNConnectionResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # VPN Gateway
            for data in self.request_vpn_gateway_data(region_name):
                resources.append(self.vpngw_res_schema(
                    {'resource': VPNGatewayResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Customer Gateway
            for data in self.request_customer_gateway_data(region_name):
                resources.append(self.customergw_res_schema(
                    {'resource': CustomerGatewayResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Transit Gateway
            for data in self.request_transit_gateway_data(region_name):
                resources.append(self.transitgw_res_schema(
                    {'resource': TransitGatewayResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Peering Connection
            for data in self.request_peering_connection_data(region_name):
                resources.append(self.peercon_res_schema(
                    {'resource': PeeringConnectionResource({'data': data,
                                                            'reference': ReferenceModel(data.reference)})}))

            # NAT Gateway
            for data in self.request_nat_gateway_data(region_name):
                resources.append(self.natgw_res_schema(
                    {'resource': NATGatewayResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Network ACL
            for data in self.request_network_acl_data(region_name):
                resources.append(self.netacl_res_schema(
                    {'resource': NetworkACLResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Endpoint
            for data in self.request_endpoint_data(region_name):
                resources.append(self.endpoint_res_schema(
                    {'resource': EndpointResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Egress Only Internet Gateway
            for data in self.request_egress_only_internet_gateway_data(region_name):
                resources.append(self.eoigw_res_schema(
                    {'resource': EgressOnlyInternetGatewayResource({'data': data,
                                                                    'reference': ReferenceModel(data.reference)})}))

            # Internet Gateways
            for data in self.request_internet_gateway_data(region_name):
                resources.append(self.igw_res_schema(
                    {'resource': InternetGatewayResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Route table
            for data in self.request_route_table_data(region_name):
                resources.append(self.rtable_res_schema(
                    {'resource': RouteTableResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # Subnet
            for data in self.request_subnet_data(region_name):
                resources.append(self.subnet_res_schema(
                    {'resource': SubnetResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            # VPC
            for data in self.request_vpc_data(region_name):
                resources.append(self.vpc_res_schema(
                    {'resource': VPCResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

        print(f' VPC Finished {time.time() - start_time} Seconds')
        return resources

    def request_vpc_data(self, region_name) -> List[VPC]:
        if len(self.dhcp_options) > 0:
            self.dhcp_options = self.describe_dhcp_options()

        for vpc in self.vpcs:
            route_tables = self._match_vpc_object(self.route_tables, vpc.get('VpcId'))

            vpc.update({
                'arn': self.generate_arn(service=self.service_name,
                                         region=region_name, account_id=self.account_id,
                                         resource_type="vpc", resource_id=vpc.get('VpcId')),
                'subnets': self._match_vpc_object(self.subnets, vpc.get('VpcId')),
                'route_tables': route_tables,
                'main_route_table_id': self._get_main_route_table(route_tables),
                'main_network_acl_id': self._get_main_network_acl(self._match_vpc_object(self.network_acls,
                                                                                         vpc.get('VpcId'))),
                'endpoints': self._match_vpc_object(self.endpoints, vpc.get('VpcId')),
                'peering_connections': self._match_vpc_peering_connection(vpc.get('VpcId')),
                'nat_gateways': self._match_vpc_object(self.nat_gateways, vpc.get('VpcId')),
                'transit_gateway': self._match_transit_gateway(vpc.get('VpcId')),
                'vpn_gateway': self._match_vpn_gateway(vpc.get('VpcId')),
                'region_name': region_name,
                'account_id': self.account_id,
                'internet_gateway': self._match_internet_gateway(vpc.get('VpcId')),
                'enable_dns_support': self.describe_vpc_attribute(vpc.get('VpcId'), 'enableDnsSupport'),
                'enable_dns_hostnames': self.describe_vpc_attribute(vpc.get('VpcId'), 'enableDnsHostnames'),
                'name': self._get_name_from_tags(vpc.get('Tags', []))
            })

            match_eoigw = self._match_egress_only_internet_gateway(vpc.get('VpcId'))
            if match_eoigw is not None:
                vpc.update({
                    'egress_only_internet_gateway': match_eoigw
                })

            match_dhcp_option = self._match_dhcp_options(vpc.get('DhcpOptionsId'))
            if match_dhcp_option is not None:
                vpc.update({
                    'dhcp_option': match_dhcp_option
                })

            yield VPC(vpc, strict=False)

    def describe_vpc_attribute(self, vpc_id, attribute):
        response = self.client.describe_vpc_attribute(VpcId=vpc_id, Attribute=attribute)
        _first_letter_upper_attr = attribute[:1].upper() + attribute[1:]
        if response[_first_letter_upper_attr]['Value'] is True:
            return "Enabled"
        else:
            return "Disabled"

    def request_peering_connection_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_vpc_peering_connections()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'accepter-vpc-info.vpc-id', 'Values': self.vpc_ids},
                        {'Name': 'requester-vpc-info.vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_vpc_peering_connections(Filters=_filters)

        for peerx in response.get('VpcPeeringConnections', []):
            peerx.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="vpc-peering-connection",
                                         resource_id=peerx.get('VpcPeeringConnectionId')),
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(peerx.get('Tags', []))
            })

            peer_connect = PeeringConnection(peerx, strict=False)
            self.peering_connections.append(peer_connect)
            yield peer_connect

    def request_nat_gateway_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_nat_gateways()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_nat_gateways(Filters=_filters)

        for ngw in response.get('NatGateways', []):
            ngw.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="nat-gateway", resource_id=ngw.get('NatGatewayId')),
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(ngw.get('Tags', []))
            })

            nat_gateway = NATGateway(ngw, strict=False)
            self.nat_gateways.append(nat_gateway)
            yield nat_gateway

    def request_network_acl_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_network_acls()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_network_acls(Filters=_filters)

        for nacl in response.get('NetworkAcls', []):
            inbound_rules, outbound_rules, total_rules = self._get_rules_from_rules(nacl.get('Entries', []))

            nacl.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="network-acl", resource_id=nacl.get('NetworkAclId')),
                'inbound_entries': inbound_rules,
                'outbound_entries': outbound_rules,
                'entries': total_rules,
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(nacl.get('Tags', []))
            })

            network_acl = NetworkACL(nacl, strict=False)
            self.network_acls.append(network_acl)
            yield network_acl

    def request_endpoint_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_vpc_endpoints()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_vpc_endpoints(Filters=_filters)

        for endp in response.get('VpcEndpoints', []):
            endp.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="vpc-endpoint", resource_id=endp.get('VpcEndpointId')),
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(endp.get('Tags', []))
            })

            endpoint = Endpoint(endp, strict=False)
            self.endpoints.append(endpoint)
            yield endpoint

    def request_egress_only_internet_gateway_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_egress_only_internet_gateways()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_egress_only_internet_gateways(Filters=_filters)

        for eoigw in response.get('EgressOnlyInternetGateways', []):
            eoigw.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="egress-only-internet-gateway",
                                         resource_id=eoigw.get('EgressOnlyInternetGatewayId')),
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(eoigw.get('Tags', []))
            })

            egress_only_internet_gateway = EgressOnlyInternetGateway(eoigw, strict=False)
            self.egress_only_internet_gateways.append(egress_only_internet_gateway)
            yield egress_only_internet_gateway

    def request_internet_gateway_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_internet_gateways()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'attachment.vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_internet_gateways(Filters=_filters)

        for igw in response.get('InternetGateways', []):
            state = None
            _attachments = igw.get('Attachments', [])
            if len(_attachments) > 0:
                state = _attachments[0]['State']

            igw.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="internet-gateway",
                                         resource_id=igw.get('InternetGatewayId')),
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(igw.get('Tags', []))
            })

            if state is not None:
                igw.update({
                    'state': state
                })

            internet_gateway = InternetGateway(igw, strict=False)
            self.internet_gateways.append(internet_gateway)
            yield internet_gateway

    def request_route_table_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_route_tables()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_route_tables(Filters=_filters)

        for rt in response.get('RouteTables', []):
            subnet_associations, edge_associations, main = self._get_association(rt.get('Associations', []))

            rt.update({
                'arn': self.generate_arn(service=self.service_name, region=region_name, account_id=self.account_id,
                                         resource_type="route-table",
                                         resource_id=rt.get('RouteTableId')),
                'routes': self._get_route(rt.get('Routes', [])),
                'subnet_associations':  subnet_associations,
                'edge_associations': edge_associations,
                'main': main,
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(rt.get('Tags', []))
            })

            route_table = RouteTable(rt, strict=False)
            self.route_tables.append(route_table)
            yield route_table

    def request_subnet_data(self, region_name):
        response = {}
        if self.include_default:
            response = self.client.describe_subnets()
        elif len(self.vpc_ids) > 0:
            _filters = [{'Name': 'vpc-id', 'Values': self.vpc_ids}]
            response = self.client.describe_subnets()

        for subnet in response.get('Subnets', []):
            subnet.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(subnet.get('Tags', []))
            })

            if match_route_table := self._match_route_table(subnet.get('SubnetId')):
                # Match subnet type: public or private
                for route in match_route_table.routes:
                    if route.gateway_id is not None and 'igw' in route.gateway_id:
                        subnet.update({'subnet_type': 'public'})

                subnet.update({'route_table': match_route_table})

            if match_network_acl := self._match_network_acl(subnet.get('SubnetId')):
                subnet.update({'network_acl': match_network_acl})

            if match_nat_gateways := self._match_nat_gateways(subnet.get('SubnetId')):
                subnet.update({'nat_gateways': match_nat_gateways})

            subnet = Subnet(subnet, strict=False)
            self.subnets.append(subnet)
            yield subnet

    def request_transit_gateway_data(self, region_name):
        response = self.client.describe_transit_gateways()

        for transit_gateway in response.get('TransitGateways', []):
            transit_gateway.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(transit_gateway.get('Tags', [])),
                'vpn_connections': self._match_vpn_connection('transit_gateway', transit_gateway.get('TransitGatewayId'))
            })

            tgw = TransitGateway(transit_gateway, strict=False)
            self.transit_gateways.append(tgw)
            yield tgw

    def request_customer_gateway_data(self, region_name):
        response = self.client.describe_customer_gateways()

        for customer_gateway in response.get('CustomerGateways', []):
            customer_gateway.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(customer_gateway.get('Tags', [])),
            })

            _match_vpn_conn = self._match_vpn_connection('customer_gateway', customer_gateway.get('CustomerGatewayId'))

            if len(_match_vpn_conn) > 0:
                customer_gateway.update({
                    'vpn_connection': _match_vpn_conn[0]
                })

            customer_gw = CustomerGateway(customer_gateway, strict=False)
            self.customer_gateways.append(customer_gw)
            yield customer_gw

    def request_vpn_gateway_data(self, region_name):
        response = self.client.describe_vpn_gateways()

        for vpn_gateway in response.get('VpnGateways', []):
            vpn_gateway.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(vpn_gateway.get('Tags', []))
            })

            _match_vpn_conn = self._match_vpn_connection('vpn_gateway', vpn_gateway.get('VpnGatewayId'))

            if len(_match_vpn_conn) > 0:
                vpn_gateway.update({
                    'vpn_connection': _match_vpn_conn[0]
                })

            vpn_gw = VPNGateway(vpn_gateway, strict=False)
            self.vpn_gateways.append(vpn_gw)
            yield vpn_gw

    def request_vpn_connection_data(self, region_name):
        response = self.client.describe_vpn_connections()

        for vpn_connection in response.get('VpnConnections', []):
            vpn_connection.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(vpn_connection.get('Tags', []))
            })

            vpn_conn = VPNConnection(vpn_connection, strict=False)
            self.vpn_connections.append(vpn_conn)
            yield vpn_conn

    @staticmethod
    def _get_name_from_tags(tags):
        for tag in tags:
            if 'Name' in tag.get('Key'):
                return tag.get('Value')

        return ""

    def _get_rules_from_rules(self, entries):
        inbounds = []
        outbounds = []
        total_rules = []

        for entry in entries:
            entry.update({
                'protocol_display': PROTOCOL_NUMBER_INFO.get(entry.get('Protocol', 'None'), ''),
                'port_range_display': self._get_port_range_display(entry)
            })

            if entry.get('Egress') is True:
                # INBOUND
                inbounds.append(NetworkACLEntries(entry, strict=False))
                entry.update({'direction': 'inbound'})
            else:
                # OUTBOUND
                outbounds.append(NetworkACLEntries(entry, strict=False))
                entry.update({'direction': 'outbound'})

            total_rules.append(NetworkACLTotalEntries(entry, strict=False))

        return inbounds, outbounds, total_rules

    def _match_route_table(self, subnet_id):
        for route_table in self.route_tables:
            for subnet_asso in route_table.subnet_associations:
                if subnet_asso.subnet_id == subnet_id:
                    return route_table

        return None

    def _match_network_acl(self, subnet_id):
        for nacl in self.network_acls:
            for asso in nacl.associations:
                if asso.subnet_id == subnet_id:
                    return nacl

    def _match_internet_gateway(self, vpc_id):
        for igw in self.internet_gateways:
            for attach in igw.attachments:
                if attach.vpc_id == vpc_id:
                    return igw

    def _match_transit_gateway(self, vpc_id):
        for transit_gw in self.transit_gateways:
            for _attach in transit_gw.vpc_attachments:
                if vpc_id == _attach.vpc_id:
                    return transit_gw

    def _match_vpn_gateway(self, vpc_id):
        for vpn_gw in self.vpn_gateways:
            if vpn_gw.vpc_attachments is not None:
                for _attach in vpn_gw.vpc_attachments:
                    if vpc_id == _attach.vpc_id:
                        return vpn_gw

        return None

    def _match_nat_gateways(self, subnet_id):
        return [ngw for ngw in self.nat_gateways if ngw.subnet_id == subnet_id]

    def _match_egress_only_internet_gateway(self, vpc_id):
        for eoigw in self.egress_only_internet_gateways:
            for attach in eoigw.attachments:
                if attach.vpc_id == vpc_id:
                    return eoigw

        return None

    def _match_dhcp_options(self, dhcp_option_id):
        for dhcp_option in self.dhcp_options:
            if dhcp_option.get('DhcpOptionsId') == dhcp_option_id:
                return DHCPOptions(dhcp_option, strict=False)

        return None

    @staticmethod
    def _match_vpc_object(objects, vpc_id):
        return [obj for obj in objects if obj.vpc_id == vpc_id]

    @staticmethod
    def _get_main_route_table(route_tables):
        for route_table in route_tables:
            if route_table.main == 'Yes':
                return route_table.route_table_id

        return ''

    @staticmethod
    def _get_port_range_display(entry):
        if 'PortRange' in entry:
            return f'{entry["PortRange"]["From"]} - {entry["PortRange"]["To"]}'
        else:
            return 'ALL'

    @staticmethod
    def _get_association(associations):
        main = 'No'
        subnet_asssocs = []
        gw_assocs = []

        for _assoc in associations:
            if _assoc.get('Main', False) is True:
                main = 'Yes'

            if 'SubnetId' in _assoc:
                subnet_asssocs.append(RouteTableAssociations(_assoc, strict=False))

            if 'GatewayId' in _assoc:
                gw_assocs.append(RouteTableAssociations(_assoc, strict=False))

        return subnet_asssocs, gw_assocs, main

    @staticmethod
    def _get_route(routes):
        return_routes = []

        for route in routes:
            route.update({
                'target': route.get('NatGatewayId', route.get('GatewayId', '')),
                'destination': route.get('DestinationPrefixListId', route.get('DestinationCidrBlock', ''))
            })

            return_routes.append(RouteTableRoutes(route, strict=False))

        return return_routes

    def _match_vpc_peering_connection(self, vpc_id):
        match_peering_connections = []
        for peercon in self.peering_connections:
            if getattr(peercon, 'accepter_vpc_info', None) is not None and peercon.accepter_vpc_info.vpc_id == vpc_id:
                match_peering_connections.append(peercon)
            elif getattr(peercon, 'requester_vpc_info', None) is not None and peercon.requester_vpc_info.vpc_id == vpc_id:
                match_peering_connections.append(peercon)

        return match_peering_connections

    def _match_vpn_connection(self, resource_type, resource_id):
        match_vpn_connections = []

        resource_type_map = {
            'transit_gateway': 'transit_gateway_id',
            'customer_gateway': 'customer_gateway_id',
            'vpn_gateway': 'vpn_gateway_id',
        }

        for vpnconn in self.vpn_connections:
            if target_resource_id := getattr(vpnconn, resource_type_map.get(resource_type, ''), None):
                if target_resource_id == resource_id:
                    match_vpn_connections.append(vpnconn)

        return match_vpn_connections

    @staticmethod
    def _get_main_network_acl(nacls):
        acl_id = [nacl.network_acl_id for nacl in nacls if nacl.is_default is True]
        if len(acl_id) > 0:
            return acl_id[0]
        else:
            return ''

    def describe_dhcp_options(self):
        response = self.client.describe_dhcp_options()
        return response.get('DhcpOptions', [])

    def list_vpcs(self):
        vpcs = []
        _filter_value = ['false']

        if self.include_default:
            _filter_value.append('true')

        paginator = self.client.get_paginator('describe_vpcs')
        response_iterator = paginator.paginate(
            Filters=[{
                'Name': 'isDefault',
                'Values': _filter_value
            }],
            PaginationConfig={
                'MaxItems': 10000
            }
        )

        for data in response_iterator:
            vpcs = vpcs + data.get('Vpcs', [])

        return vpcs