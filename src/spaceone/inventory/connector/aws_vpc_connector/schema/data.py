import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")

'''
NETWORK ACL
'''
class IcmpTypeCode(Model):
    code = IntType(deserialize_from="Code")
    type = IntType(deserialize_from="Type")


class PortRange(Model):
    port_rom = IntType(deserialize_from="From")
    port_to = IntType(deserialize_from="To")


class NetworkACLAssociations(Model):
    network_acl_association_id = StringType(deserialize_from="NetworkAclAssociationId")
    network_acl_id = StringType(deserialize_from="NetworkAclId")
    subnet_id = StringType(deserialize_from="SubnetId")


class NetworkACLEntries(Model):
    cidr_block = StringType(deserialize_from="CidrBlock")
    egress = BooleanType(deserialize_from="Egress")
    icmp_type_code = ModelType(IcmpTypeCode, deserialize_from="IcmpTypeCode")
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")
    port_range = ModelType(PortRange, deserialize_from="PortRange")
    protocol = StringType(deserialize_from="Protocol")
    rule_action = StringType(deserialize_from="RuleAction", choices=("allow", "deny"))
    rule_number = IntType(deserialize_from="RuleNumber")
    protocol_display = StringType(default="")
    port_range_display = StringType(default="")


class NetworkACLTotalEntries(NetworkACLEntries):
    direction = StringType()


class NetworkACL(Model):
    arn = StringType(default="")
    name = StringType(default="")
    associations = ListType(ModelType(NetworkACLAssociations), deserialize_from="Associations")
    inbound_entries = ListType(ModelType(NetworkACLEntries))
    outbound_entries = ListType(ModelType(NetworkACLEntries))
    entries = ListType(ModelType(NetworkACLTotalEntries))
    is_default = BooleanType(deserialize_from="IsDefault")
    network_acl_id = StringType(deserialize_from="NetworkAclId")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#acls:networkAclId={self.network_acl_id}"
        }


'''
VPC PEERING CONNECTION
'''
class PeeringOptions(Model):
    allow_dns_resolution_from_remote_vpc = BooleanType(deserialize_from="AllowDnsResolutionFromRemoteVpc")
    allow_egress_from_local_classic_link_to_remote_vpc = BooleanType(deserialize_from="AllowEgressFromLocalClassicLinkToRemoteVpc")
    allow_egress_from_local_vpc_to_remote_classic_link = BooleanType(deserialize_from="AllowEgressFromLocalVpcToRemoteClassicLink")


class RequesterVpcInfoIpv6CidrBlockSet(Model):
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")


class RequesterVpcInfoCidrBlockSet(Model):
    cidr_block = StringType(deserialize_from="CidrBlock")


class RequesterVpcInfo(Model):
    cidr_block = StringType(deserialize_from="CidrBlock")
    ipv6_cidr_block_set = ListType(ModelType(RequesterVpcInfoIpv6CidrBlockSet), deserialize_from="Ipv6CidrBlockSet")
    cidr_block_set = ListType(ModelType(RequesterVpcInfoCidrBlockSet), deserialize_from="CidrBlockSet")
    owner_id = StringType(deserialize_from="OwnerId")
    peering_options = ModelType(PeeringOptions, deserialize_from="PeeringOptions")
    vpc_id = StringType(deserialize_from="VpcId")
    region = StringType(deserialize_from="Region")


class Status(Model):
    code = StringType(deserialize_from="Code", choices=("initiating-request", "pending-acceptance", "active",
                                                        "deleted", "rejected", "failed", "expired", "provisioning",
                                                        "deleting"))
    message = StringType(deserialize_from="Message")


class PeeringConnection(Model):
    arn = StringType(default="")
    name = StringType(default="")
    accepter_vpc_info = ModelType(RequesterVpcInfo, deserialize_from="AccepterVpcInfo")
    expiration_time = DateTimeType(deserialize_from="ExpirationTime")
    requester_vpc_info = ModelType(RequesterVpcInfo, deserialize_from="RequesterVpcInfo")
    status = ModelType(Status, deserialize_from="Status")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    vpc_peering_connection_id = StringType(deserialize_from="VpcPeeringConnectionId")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#PeeringConnections:vpcPeeringConnectionId={self.vpc_peering_connection_id}"
        }

'''
NAT GATEWAY
'''
class ProvisionedBandwidth(Model):
    provision_time = DateTimeType(deserialize_from="ProvisionTime")
    provisioned = StringType(deserialize_from="Provisioned")
    request_time = DateTimeType(deserialize_from="RequestTime")
    requested = StringType(deserialize_from="Requested")
    status = StringType(deserialize_from="Status")


class NATGatewayNatGatewayAddresses(Model):
    allocation_id = StringType(deserialize_from="AllocationId")
    network_interface_id = StringType(deserialize_from="NetworkInterfaceId")
    private_ip = StringType(deserialize_from="PrivateIp")
    public_ip = StringType(deserialize_from="PublicIp")


class NATGateway(Model):
    arn = StringType(default="")
    name = StringType(default="")
    create_time = DateTimeType(deserialize_from="CreateTime")
    delete_time = DateTimeType(deserialize_from="DeleteTime")
    failure_code = StringType(deserialize_from="FailureCode")
    failure_message = StringType(deserialize_from="FailureMessage")
    nat_gateway_addresses = ListType(ModelType(NATGatewayNatGatewayAddresses), deserialize_from="NatGatewayAddresses")
    nat_gateway_id = StringType(deserialize_from="NatGatewayId")
    provisioned_bandwidth = ModelType(ProvisionedBandwidth, deserialize_from="ProvisionedBandwidth")
    state = StringType(deserialize_from="State", choices=("pending", "failed", "available", "deleting", "deleted"))
    subnet_id = StringType(deserialize_from="SubnetId")
    vpc_id = StringType(deserialize_from="VpcId")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#NatGateways:natGatewayId={self.nat_gateway_id}"
        }

    @serializable
    def cloudwatch(self):
        return {
            "namespace": "AWS/NATGateway",
            "dimensions": [
                {
                    "Name": "NatGatewayId",
                    "Value": self.nat_gateway_id
                }
            ],
            "region_name": self.region_name
        }


'''
ENDPOINT
'''
class LastError(Model):
    message = StringType(deserialize_from="Message")
    code = StringType(deserialize_from="Code")


class EndpointsGroups(Model):
    group_id = StringType(deserialize_from="GroupId")
    group_name = StringType(deserialize_from="GroupName")


class EndpointsDnsEntries(Model):
    dns_name = StringType(deserialize_from="DnsName")
    hosted_zone_id = StringType(deserialize_from="HostedZoneId")


class Endpoint(Model):
    arn = StringType(default="")
    name = StringType(default="")
    vpc_endpoint_id = StringType(deserialize_from="VpcEndpointId")
    vpc_endpoint_type = StringType(deserialize_from="VpcEndpointType", choices=("Interface", "Gateway"))
    vpc_id = StringType(deserialize_from="VpcId")
    service_name = StringType(deserialize_from="ServiceName")
    state = StringType(deserialize_from="State", choices=("PendingAcceptance", "Pending", "Available", "Deleting",
                                                          "Deleted", "Rejected", "Failed", "Expired"))
    policy_document = StringType(deserialize_from="PolicyDocument")
    route_table_ids = ListType(StringType, deserialize_from="RouteTableIds")
    subnet_ids = ListType(StringType, deserialize_from="SubnetIds")
    groups = ListType(ModelType(EndpointsGroups), deserialize_from="Groups")
    private_dns_enabled = BooleanType(deserialize_from="PrivateDnsEnabled")
    requester_managed = BooleanType(deserialize_from="RequesterManaged")
    network_interface_ids = ListType(StringType, deserialize_from="NetworkInterfaceIds")
    dns_entries = ListType(ModelType(EndpointsDnsEntries), deserialize_from="DnsEntries")
    creation_timestamp = DateTimeType(deserialize_from="CreationTimestamp")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    owner_id = StringType(deserialize_from="OwnerId")
    last_error = ModelType(LastError, deserialize_from="LastError")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#Endpoints:vpcEndpointId={self.vpc_endpoint_id}"
        }


'''
EGRESS ONLY INTERNET GATEWAY
'''
class EgressOnlyInternetGatewayAttachments(Model):
    state = StringType(deserialize_from="State", choices=("attaching", "attached", "detaching", "detached"))
    vpc_id = StringType(deserialize_from="VpcId")


class EgressOnlyInternetGateway(Model):
    arn = StringType(default="")
    name = StringType(default="")
    attachments = ListType(ModelType(EgressOnlyInternetGatewayAttachments), deserialize_from="Attachments")
    egress_only_internet_gateway_id = StringType(deserialize_from="EgressOnlyInternetGatewayId")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#EgressOnlyInternetGateways:egressOnlyInternetGatewayId={self.egress_only_internet_gateway_id}"
        }


'''
INTERNET GATEWAY
'''
class InternetGatewayAttachments(Model):
    state = StringType(deserialize_from="State", choices=("attaching", "attached", "detaching", "detached"))
    vpc_id = StringType(deserialize_from="VpcId")


class InternetGateway(Model):
    arn = StringType(default="")
    name = StringType(default="")
    state = StringType()
    attachments = ListType(ModelType(InternetGatewayAttachments), deserialize_from="Attachments")
    internet_gateway_id = StringType(deserialize_from="InternetGatewayId")
    owner_id = StringType(deserialize_from="OwnerId")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#igws:internetGatewayId={self.internet_gateway_id}"
        }


'''
ROUTE TABLES
'''
class AssociationState(Model):
    state = StringType(deserialize_from="State",choices=("associating", "associated", "disassociating",
                                                         "disassociated", "failed"))
    status_message = StringType(deserialize_from="StatusMessage")


class RouteTableAssociations(Model):
    main = BooleanType(deserialize_from="Main")
    route_table_association_id = StringType(deserialize_from="RouteTableAssociationId")
    route_table_id = StringType(deserialize_from="RouteTableId")
    subnet_id = StringType(deserialize_from="SubnetId")
    gateway_id = StringType(deserialize_from="GatewayId")
    association_state = ModelType(AssociationState, deserialize_from="AssociationState")


class RouteTablePropagatingVgws(Model):
    gateway_id = StringType(deserialize_from="GatewayId")


class RouteTableRoutes(Model):
    destination_cidr_block = StringType(deserialize_from="DestinationCidrBlock")
    destination_ipv6_cidr_block = StringType(deserialize_from="DestinationIpv6CidrBlock")
    destination_prefix_list_id = StringType(deserialize_from="DestinationPrefixListId")
    egress_only_internet_gateway_id = StringType(deserialize_from="EgressOnlyInternetGatewayId")
    gateway_id = StringType(deserialize_from="GatewayId")
    instance_id = StringType(deserialize_from="InstanceId")
    instance_owner_id = StringType(deserialize_from="InstanceOwnerId")
    nat_gateway_id = StringType(deserialize_from="NatGatewayId")
    transit_gateway_id = StringType(deserialize_from="TransitGatewayId")
    local_gateway_id = StringType(deserialize_from="LocalGatewayId")
    network_interface_id = StringType(deserialize_from="NetworkInterfaceId")
    origin = StringType(deserialize_from="Origin", choices=("CreateRouteTable",
                                                            "CreateRoute",
                                                            "EnableVgwRoutePropagation"))
    state = StringType(deserialize_from="State", choices=("active", "blackhole"))
    target = StringType(default="")
    destination = StringType(default="")
    vpc_peering_connection_id = StringType(deserialize_from="VpcPeeringConnectionId")


class RouteTable(Model):
    arn = StringType(default="")
    name = StringType(default="")
    subnet_associations = ListType(ModelType(RouteTableAssociations), deserialize_from="SubnetAssociations")
    edge_associations = ListType(ModelType(RouteTableAssociations), deserialize_from="EdgeAssociations")
    propagating_vgws = ListType(ModelType(RouteTablePropagatingVgws), deserialize_from="PropagatingVgws")
    route_table_id = StringType(deserialize_from="RouteTableId")
    routes = ListType(ModelType(RouteTableRoutes), deserialize_from="Routes")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")
    main = StringType(default="")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#RouteTables:routeTableId={self.route_table_id}"
        }

'''
DHCP Options
'''
class DHCPConfigurationValues(Model):
    value = StringType(deserialize_from="Value")


class DHCPOptionsDhcpConfigurations(Model):
    key = StringType(deserialize_from="Key")
    values = ListType(ModelType(DHCPConfigurationValues), deserialize_from="Values")


class DHCPOptions(Model):
    dhcp_configurations = ListType(ModelType(DHCPOptionsDhcpConfigurations), deserialize_from="DhcpConfigurations")
    dhcp_options_id = StringType(deserialize_from="DhcpOptionsId")
    owner_id = StringType(deserialize_from="OwnerId")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#dhcpOptions:DhcpOptionsId={self.dhcp_options_id}"
        }

'''
SUBNET
'''
class Ipv6CidrBlockState(Model):
    state = StringType(deserialize_from="State", choices=("associating", "associated", "disassociating",
                                                          "disassociated", "failing", "failed"))
    status_message = StringType(deserialize_from="StatusMessage")


class SubnetIpv6CidrBlockAssociationSet(Model):
    association_id = StringType(deserialize_from="AssociationId")
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")
    ipv6_cidr_block_state = ModelType(Ipv6CidrBlockState, deserialize_from="Ipv6CidrBlockState")


class Subnet(Model):
    name = StringType(default="")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    availability_zone_id = StringType(deserialize_from="AvailabilityZoneId")
    available_ip_address_count = IntType(deserialize_from="AvailableIpAddressCount")
    cidr_block = StringType(deserialize_from="CidrBlock")
    default_for_az = BooleanType(deserialize_from="DefaultForAz")
    map_public_ip_on_launch = BooleanType(deserialize_from="MapPublicIpOnLaunch")
    state = StringType(deserialize_from="State", choices=("pending", "available"))
    subnet_id = StringType(deserialize_from="SubnetId")
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")
    assign_ipv6_address_on_creation = BooleanType(deserialize_from="AssignIpv6AddressOnCreation")
    ipv6_cidr_block_association_set = ListType(ModelType(SubnetIpv6CidrBlockAssociationSet),
                                               deserialize_from="Ipv6CidrBlockAssociationSet")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    subnet_arn = StringType(deserialize_from="SubnetArn")
    outpost_arn = StringType(deserialize_from="OutpostArn")
    nat_gateways = ListType(ModelType(NATGateway))
    route_table = ModelType(RouteTable)
    network_acl = ModelType(NetworkACL)
    region_name = StringType(default="")
    account_id = StringType(default="")
    subnet_type = StringType(choices=["public", "private"], default="private")

    @serializable
    def reference(self):
        return {
            "resource_id": self.subnet_arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#subnets:SubnetId={self.subnet_id}"
        }

'''
VPC
'''
class CidrBlockState(Model):
    state = StringType(deserialize_from="State",
                       choices=("associating", "associated", "disassociating", "disassociated", "failing", "failed"))
    status_message = StringType(deserialize_from="StatusMessage")


class VPCIpv6CidrBlockAssociationSet(Model):
    association_id = StringType(deserialize_from="AssociationId")
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")
    ipv6_cidr_block_state = ModelType(Ipv6CidrBlockState, deserialize_from="Ipv6CidrBlockState")
    network_border_group = StringType(deserialize_from="NetworkBorderGroup")
    ipv6_pool = StringType(deserialize_from="Ipv6Pool")


class VPCCidrBlockAssociationSet(Model):
    association_id = StringType(deserialize_from="AssociationId")
    cidr_block = StringType(deserialize_from="CidrBlock")
    cidr_block_state = ModelType(CidrBlockState, deserialize_from="CidrBlockState")


class VPC(Model):
    arn = StringType(default="")
    name = StringType(default="")
    cidr_block = StringType(deserialize_from="CidrBlock")
    dhcp_options_id = StringType(deserialize_from="DhcpOptionsId")
    dhcp_option = ModelType(DHCPOptions)
    state = StringType(deserialize_from="State", choices=("pending", "available"))
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")
    instance_tenancy = StringType(deserialize_from="InstanceTenancy", choices=("default", "dedicated", "host"))
    ipv6_cidr_block_association_set = ListType(ModelType(VPCIpv6CidrBlockAssociationSet),
                                               deserialize_from="Ipv6CidrBlockAssociationSet")
    cidr_block_association_set = ListType(ModelType(VPCCidrBlockAssociationSet),
                                          deserialize_from="CidrBlockAssociationSet")
    is_default = BooleanType(deserialize_from="IsDefault")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    subnets = ListType(ModelType(Subnet))
    route_tables = ListType(ModelType(RouteTable))
    main_route_table_id = StringType()
    main_network_acl_id = StringType()
    egress_only_internet_gateway = ModelType(EgressOnlyInternetGateway)
    endpoints = ListType(ModelType(Endpoint))
    peering_connections = ListType(ModelType(PeeringConnection))
    region_name = StringType(default="")
    account_id = StringType(default="")
    nat_gateways = ListType(ModelType(NATGateway))
    internet_gateway = ModelType(InternetGateway)
    enable_dns_support = StringType(choices=("Enabled", "Disabled"))
    enable_dns_hostnames = StringType(choices=("Enabled", "Disabled"))

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={self.region_name}#vpcs:VpcId={self.vpc_id}"
        }
