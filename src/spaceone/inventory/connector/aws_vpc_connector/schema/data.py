import logging
from schematics import Model
from schematics.types import (
    ModelType,
    StringType,
    IntType,
    DateTimeType,
    ListType,
    BooleanType,
)
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


"""
VPN Connection
"""


class VPNConnectionVgwTelemetry(Model):
    accepted_route_count = IntType(deserialize_from="AcceptedRouteCount")
    last_status_change = DateTimeType(deserialize_from="LastStatusChange")
    outside_ip_address = StringType(deserialize_from="OutsideIpAddress")
    status = StringType(deserialize_from="Status", choices=("UP", "DOWN"))
    status_message = StringType(deserialize_from="StatusMessage")
    certificate_arn = StringType(deserialize_from="CertificateArn")


class VPNConnectionTunnelOptionPhase1EncryptionAlgorithms(Model):
    value = StringType(deserialize_from="Value")


class VPNConnectionTunnelOptionPhase2EncryptionAlgorithms(Model):
    value = StringType(deserialize_from="Value")


class VPNConnectionTunnelOptionPhase1IntegrityAlgorithms(Model):
    value = StringType(deserialize_from="Value")


class VPNConnectionTunnelOptionPhase2IntegrityAlgorithms(Model):
    value = StringType(deserialize_from="Value")


class VPNConnectionTunnelOptionPhase1DHGroupNumbers(Model):
    value = IntType(deserialize_from="Value")


class VPNConnectionTunnelOptionPhase2DHGroupNumbers(Model):
    value = IntType(deserialize_from="Value")


class VPNConnectionTunnelOptionIkeVersions(Model):
    value = StringType(deserialize_from="Value")


class VPNConnectionTunnelOption(Model):
    outside_ip_address = StringType(deserialize_from="OutsideIpAddress")
    tunnel_inside_cidr = StringType(deserialize_from="TunnelInsideCidr")
    pre_shared_key = StringType(deserialize_from="PreSharedKey")
    phase1_lifetime_seconds = IntType(deserialize_from="Phase1LifetimeSeconds")
    phase2_lifetime_seconds = IntType(deserialize_from="Phase2LifetimeSeconds")
    rekey_margin_time_seconds = IntType(deserialize_from="RekeyMarginTimeSeconds")
    rekey_fuzz_percentage = IntType(deserialize_from="RekeyFuzzPercentage")
    replay_window_size = IntType(deserialize_from="ReplayWindowSize")
    dpd_timeout_seconds = IntType(deserialize_from="DpdTimeoutSeconds")
    phase1_encryption_algorithms = ListType(
        ModelType(VPNConnectionTunnelOptionPhase1EncryptionAlgorithms),
        deserialize_from="Phase1EncryptionAlgorithms",
    )
    phase2_encryption_algorithms = ListType(
        ModelType(VPNConnectionTunnelOptionPhase2EncryptionAlgorithms),
        deserialize_from="Phase2EncryptionAlgorithms",
    )
    phase1_integrity_algorithms = ListType(
        ModelType(VPNConnectionTunnelOptionPhase1IntegrityAlgorithms),
        deserialize_from="Phase1IntegrityAlgorithms",
    )
    phase2_integrity_algorithms = ListType(
        ModelType(VPNConnectionTunnelOptionPhase2IntegrityAlgorithms),
        deserialize_from="Phase2IntegrityAlgorithms",
    )
    phase1_dh_group_numbers = ListType(
        ModelType(VPNConnectionTunnelOptionPhase1DHGroupNumbers),
        deserialize_from="Phase1DHGroupNumbers",
    )
    phase2_dh_group_numbers = ListType(
        ModelType(VPNConnectionTunnelOptionPhase2DHGroupNumbers),
        deserialize_from="Phase2DHGroupNumbers",
    )
    ike_versions = ListType(
        ModelType(VPNConnectionTunnelOptionIkeVersions), deserialize_from="IkeVersions"
    )


class VPNConnectionOptions(Model):
    enable_acceleration = BooleanType(deserialize_from="EnableAcceleration")
    static_routes_only = BooleanType(deserialize_from="StaticRoutesOnly")
    tunnel_options = ListType(
        ModelType(VPNConnectionTunnelOption), deserialize_from="TunnelOptions"
    )


class VPNConnectionRoutes(Model):
    destination_cidr_block = StringType(deserialize_from="DestinationCidrBlock")
    source = StringType(deserialize_from="Source")
    state = StringType(
        deserialize_from="State",
        choices=("pending", "available", "deleting", "deleted"),
    )


class VPNConnection(AWSCloudService):
    name = StringType(default="")
    customer_gateway_configuration = StringType(
        deserialize_from="CustomerGatewayConfiguration"
    )
    customer_gateway_id = StringType(deserialize_from="CustomerGatewayId")
    customer_gateway_address = StringType()
    category = StringType(deserialize_from="Category")
    state = StringType(
        deserialize_from="State",
        choices=("pending", "available", "deleting", "deleted"),
    )
    type = StringType(deserialize_from="Type")
    vpn_connection_id = StringType(deserialize_from="VpnConnectionId")
    vpn_gateway_id = StringType(deserialize_from="VpnGatewayId")
    transit_gateway_id = StringType(deserialize_from="TransitGatewayId")
    options = ModelType(VPNConnectionOptions, deserialize_from="Options")
    routes = ListType(ModelType(VPNConnectionRoutes), deserialize_from="Routes")
    vgw_telemetry = ListType(
        ModelType(VPNConnectionVgwTelemetry), deserialize_from="VgwTelemetry"
    )

    def reference(self, region_code):
        return {
            "resource_id": self.vpn_connection_id,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#VpnConnections:VpnConnectionId={self.vpn_connection_id};sort=VpnConnectionId",
        }


"""
VPN GATEWAY
"""


class VPNGatewayVpcAttachments(Model):
    state = StringType(
        deserialize_from="State",
        choices=("attaching", "attached", "detaching", "detached"),
    )
    vpc_id = StringType(deserialize_from="VpcId")


class VPNGateway(AWSCloudService):
    name = StringType(default="")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    state = StringType(
        deserialize_from="State",
        choices=("pending", "available", "deleting", "deleted"),
    )
    type = StringType(deserialize_from="Type")
    vpc_attachments = ListType(
        ModelType(VPNGatewayVpcAttachments), deserialize_from="VpcAttachments"
    )
    vpn_gateway_id = StringType(deserialize_from="VpnGatewayId")
    amazon_side_asn = IntType(deserialize_from="AmazonSideAsn")
    vpn_connection = ModelType(VPNConnection)

    def reference(self, region_code):
        return {
            "resource_id": self.vpn_gateway_id,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#VpnGateways:VpnGatewayId={self.vpn_gateway_id};sort=VpnGatewayId",
        }


"""
CUSTOMER GATEWAY
"""


class CustomerGateway(AWSCloudService):
    name = StringType(default="")
    bgp_asn = StringType(deserialize_from="BgpAsn")
    customer_gateway_id = StringType(deserialize_from="CustomerGatewayId")
    ip_address = StringType(deserialize_from="IpAddress")
    certificate_arn = StringType(deserialize_from="CertificateArn")
    state = StringType(
        deserialize_from="State",
        choices=("pending", "available", "deleting", "deleted"),
    )
    type = StringType(deserialize_from="Type")
    device_name = StringType(deserialize_from="DeviceName")
    vpn_connection = ModelType(VPNConnection)
    region_name = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.customer_gateway_id,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#CustomerGateways:CustomerGatewayId={self.customer_gateway_id};sort=CustomerGatewayId",
        }


"""
TRANSIT GATEWAY ATTACHMENT
"""


class Association(Model):
    transit_gateway_route_table_id = StringType(
        deserialize_from="TransitGatewayRouteTableId"
    )
    state = StringType(
        deserialize_from="State",
        choices=("associating", "associated", "disassociating", "disassociated"),
    )


class TransitGatewayAttachment(Model):
    transit_gateway_attachment_id = StringType(
        deserialize_from="TransitGatewayAttachmentId"
    )
    transit_gateway_id = StringType(deserialize_from="TransitGatewayId")
    transit_gateway_owner_id = StringType(deserialize_from="TransitGatewayOwnerId")
    resource_owner_id = StringType(deserialize_from="ResourceOwnerId")
    resource_type = StringType(
        deserialize_from="ResourceType",
        choices=("vpc", "vpn", "direct-connect-gateway", "tgw-peering"),
    )
    resource_id = StringType(deserialize_from="ResourceId")
    state = StringType(
        deserialize_from="State",
        choices=(
            "initiating",
            "pendingAcceptance",
            "rollingBack",
            "pending",
            "available",
            "modifying",
            "deleting",
            "deleted",
            "failed",
            "rejected",
            "rejecting",
            "failing",
        ),
    )
    association = ModelType(Association, deserialize_from="Association")
    creation_time = DateTimeType(deserialize_from="CreationTime")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])


"""
TRANSIT GATEWAY ROUTE TABLE
"""


class TransitGatewayRouteTables(Model):
    transit_gateway_route_table_id = StringType(
        deserialize_from="TransitGatewayRouteTableId"
    )
    transit_gateway_id = StringType(deserialize_from="TransitGatewayId")
    state = StringType(
        deserialize_from="State",
        choices=("pending", "available", "deleting", "deleted"),
    )
    default_association_route_table = BooleanType(
        deserialize_from="DefaultAssociationRouteTable"
    )
    default_propagation_route_table = BooleanType(
        deserialize_from="DefaultPropagationRouteTable"
    )
    creation_time = DateTimeType(deserialize_from="CreationTime")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])


"""
TRANSIT GATEWAY
"""


class TransitGatewayOptions(Model):
    amazon_side_asn = IntType(deserialize_from="AmazonSideAsn")
    auto_accept_shared_attachments = StringType(
        deserialize_from="AutoAcceptSharedAttachments", choices=("enable", "disable")
    )
    default_route_table_association = StringType(
        deserialize_from="DefaultRouteTableAssociation", choices=("enable", "disable")
    )
    association_default_route_table_id = StringType(
        deserialize_from="AssociationDefaultRouteTableId"
    )
    default_route_table_propagation = StringType(
        deserialize_from="DefaultRouteTablePropagation", choices=("enable", "disable")
    )
    propagation_default_route_table_id = StringType(
        deserialize_from="PropagationDefaultRouteTableId"
    )
    vpn_ecmp_support = StringType(
        deserialize_from="VpnEcmpSupport", choices=("enable", "disable")
    )
    dns_support = StringType(
        deserialize_from="DnsSupport", choices=("enable", "disable")
    )
    multicast_support = StringType(
        deserialize_from="MulticastSupport", choices=("enable", "disable")
    )


class TransitGateway(AWSCloudService):
    name = StringType(default="")
    transit_gateway_id = StringType(deserialize_from="TransitGatewayId")
    transit_gateway_arn = StringType(deserialize_from="TransitGatewayArn")
    state = StringType(
        deserialize_from="State",
        choices=("pending", "available", "modifying", "deleting", "deleted"),
    )
    owner_id = StringType(deserialize_from="OwnerId")
    description = StringType(deserialize_from="Description")
    creation_time = DateTimeType(deserialize_from="CreationTime")
    options = ModelType(TransitGatewayOptions, deserialize_from="Options")
    transit_gateway_route_table = ModelType(TransitGatewayRouteTables)
    vpn_connections = ListType(ModelType(VPNConnection))

    def reference(self, region_code):
        return {
            "resource_id": self.transit_gateway_arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#TransitGateways:transitGatewayId={self.transit_gateway_id};sort=ownerId",
        }


"""
NETWORK ACL
"""


class IcmpTypeCode(Model):
    code = IntType(deserialize_from="Code")
    type = IntType(deserialize_from="Type")


class PortRange(Model):
    port_from = IntType(deserialize_from="From")
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


class NetworkACL(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    associations = ListType(
        ModelType(NetworkACLAssociations), deserialize_from="Associations"
    )
    inbound_entries = ListType(ModelType(NetworkACLEntries))
    outbound_entries = ListType(ModelType(NetworkACLEntries))
    entries = ListType(ModelType(NetworkACLTotalEntries))
    is_default = BooleanType(deserialize_from="IsDefault")
    network_acl_id = StringType(deserialize_from="NetworkAclId")
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#acls:networkAclId={self.network_acl_id}",
        }


"""
VPC PEERING CONNECTION
"""


class PeeringOptions(Model):
    allow_dns_resolution_from_remote_vpc = BooleanType(
        deserialize_from="AllowDnsResolutionFromRemoteVpc"
    )
    allow_egress_from_local_classic_link_to_remote_vpc = BooleanType(
        deserialize_from="AllowEgressFromLocalClassicLinkToRemoteVpc"
    )
    allow_egress_from_local_vpc_to_remote_classic_link = BooleanType(
        deserialize_from="AllowEgressFromLocalVpcToRemoteClassicLink"
    )


class RequesterVpcInfoIpv6CidrBlockSet(Model):
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")


class RequesterVpcInfoCidrBlockSet(Model):
    cidr_block = StringType(deserialize_from="CidrBlock")


class RequesterVpcInfo(Model):
    cidr_block = StringType(deserialize_from="CidrBlock")
    ipv6_cidr_block_set = ListType(
        ModelType(RequesterVpcInfoIpv6CidrBlockSet), deserialize_from="Ipv6CidrBlockSet"
    )
    cidr_block_set = ListType(
        ModelType(RequesterVpcInfoCidrBlockSet), deserialize_from="CidrBlockSet"
    )
    owner_id = StringType(deserialize_from="OwnerId")
    peering_options = ModelType(PeeringOptions, deserialize_from="PeeringOptions")
    vpc_id = StringType(deserialize_from="VpcId")
    region = StringType(deserialize_from="Region")


class Status(Model):
    code = StringType(
        deserialize_from="Code",
        choices=(
            "initiating-request",
            "pending-acceptance",
            "active",
            "deleted",
            "rejected",
            "failed",
            "expired",
            "provisioning",
            "deleting",
        ),
    )
    message = StringType(deserialize_from="Message")


class PeeringConnection(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    accepter_vpc_info = ModelType(RequesterVpcInfo, deserialize_from="AccepterVpcInfo")
    expiration_time = DateTimeType(deserialize_from="ExpirationTime")
    requester_vpc_info = ModelType(
        RequesterVpcInfo, deserialize_from="RequesterVpcInfo"
    )
    status = ModelType(Status, deserialize_from="Status")
    vpc_peering_connection_id = StringType(deserialize_from="VpcPeeringConnectionId")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#PeeringConnections:vpcPeeringConnectionId={self.vpc_peering_connection_id}",
        }


"""
NAT GATEWAY
"""


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


class NATGateway(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    create_time = DateTimeType(deserialize_from="CreateTime")
    delete_time = DateTimeType(deserialize_from="DeleteTime")
    failure_code = StringType(deserialize_from="FailureCode")
    failure_message = StringType(deserialize_from="FailureMessage")
    nat_gateway_addresses = ListType(
        ModelType(NATGatewayNatGatewayAddresses), deserialize_from="NatGatewayAddresses"
    )
    nat_gateway_id = StringType(deserialize_from="NatGatewayId")
    provisioned_bandwidth = ModelType(
        ProvisionedBandwidth, deserialize_from="ProvisionedBandwidth"
    )
    state = StringType(
        deserialize_from="State",
        choices=("pending", "failed", "available", "deleting", "deleted"),
    )
    subnet_id = StringType(deserialize_from="SubnetId")
    vpc_id = StringType(deserialize_from="VpcId")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#NatGateways:natGatewayId={self.nat_gateway_id}",
        }


"""
ENDPOINT
"""


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
    vpc_endpoint_type = StringType(
        deserialize_from="VpcEndpointType", choices=("Interface", "Gateway")
    )
    vpc_id = StringType(deserialize_from="VpcId")
    service_name = StringType(deserialize_from="ServiceName")
    state = StringType(
        deserialize_from="State",
        choices=(
            "PendingAcceptance",
            "Pending",
            "Available",
            "Deleting",
            "Deleted",
            "Rejected",
            "Failed",
            "Expired",
        ),
    )
    policy_document = StringType(deserialize_from="PolicyDocument")
    route_table_ids = ListType(StringType, deserialize_from="RouteTableIds")
    subnet_ids = ListType(StringType, deserialize_from="SubnetIds")
    groups = ListType(ModelType(EndpointsGroups), deserialize_from="Groups")
    private_dns_enabled = BooleanType(deserialize_from="PrivateDnsEnabled")
    requester_managed = BooleanType(deserialize_from="RequesterManaged")
    network_interface_ids = ListType(StringType, deserialize_from="NetworkInterfaceIds")
    dns_entries = ListType(
        ModelType(EndpointsDnsEntries), deserialize_from="DnsEntries"
    )
    creation_timestamp = DateTimeType(deserialize_from="CreationTimestamp")
    owner_id = StringType(deserialize_from="OwnerId")
    last_error = ModelType(LastError, deserialize_from="LastError")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#Endpoints:vpcEndpointId={self.vpc_endpoint_id}",
        }


"""
EGRESS ONLY INTERNET GATEWAY
"""


class EgressOnlyInternetGatewayAttachments(Model):
    state = StringType(
        deserialize_from="State",
        choices=("attaching", "attached", "detaching", "detached"),
    )
    vpc_id = StringType(deserialize_from="VpcId")


class EgressOnlyInternetGateway(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    attachments = ListType(
        ModelType(EgressOnlyInternetGatewayAttachments), deserialize_from="Attachments"
    )
    egress_only_internet_gateway_id = StringType(
        deserialize_from="EgressOnlyInternetGatewayId"
    )

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#EgressOnlyInternetGateways:egressOnlyInternetGatewayId={self.egress_only_internet_gateway_id}",
        }


"""
INTERNET GATEWAY
"""


class InternetGatewayAttachments(Model):
    state = StringType(
        deserialize_from="State",
        choices=("attaching", "attached", "detaching", "detached"),
    )
    vpc_id = StringType(deserialize_from="VpcId")


class InternetGateway(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    state = StringType()
    attachments = ListType(
        ModelType(InternetGatewayAttachments), deserialize_from="Attachments"
    )
    internet_gateway_id = StringType(deserialize_from="InternetGatewayId")
    owner_id = StringType(deserialize_from="OwnerId")
    region_name = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#igws:internetGatewayId={self.internet_gateway_id}",
        }


"""
ROUTE TABLES
"""


class AssociationState(Model):
    state = StringType(
        deserialize_from="State",
        choices=(
            "associating",
            "associated",
            "disassociating",
            "disassociated",
            "failed",
        ),
    )
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
    destination_cidr_block = StringType(
        deserialize_from="DestinationCidrBlock", serialize_when_none=False
    )
    destination_ipv6_cidr_block = StringType(
        deserialize_from="DestinationIpv6CidrBlock", serialize_when_none=False
    )
    destination_prefix_list_id = StringType(
        deserialize_from="DestinationPrefixListId", serialize_when_none=False
    )
    egress_only_internet_gateway_id = StringType(
        deserialize_from="EgressOnlyInternetGatewayId", serialize_when_none=False
    )
    gateway_id = StringType(deserialize_from="GatewayId", serialize_when_none=False)
    instance_id = StringType(deserialize_from="InstanceId", serialize_when_none=False)
    instance_owner_id = StringType(
        deserialize_from="InstanceOwnerId", serialize_when_none=False
    )
    nat_gateway_id = StringType(
        deserialize_from="NatGatewayId", serialize_when_none=False
    )
    transit_gateway_id = StringType(
        deserialize_from="TransitGatewayId", serialize_when_none=False
    )
    local_gateway_id = StringType(
        deserialize_from="LocalGatewayId", serialize_when_none=False
    )
    network_interface_id = StringType(
        deserialize_from="NetworkInterfaceId", serialize_when_none=False
    )
    origin = StringType(
        deserialize_from="Origin",
        choices=("CreateRouteTable", "CreateRoute", "EnableVgwRoutePropagation"),
    )
    state = StringType(deserialize_from="State", choices=("active", "blackhole"))
    target = StringType(default="")
    destination = StringType(default="")
    vpc_peering_connection_id = StringType(
        deserialize_from="VpcPeeringConnectionId", serialize_when_none=False
    )


class RouteTable(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    subnet_associations = ListType(
        ModelType(RouteTableAssociations),
        deserialize_from="SubnetAssociations",
        default=[],
    )
    edge_associations = ListType(
        ModelType(RouteTableAssociations),
        deserialize_from="EdgeAssociations",
        default=[],
    )
    propagating_vgws = ListType(
        ModelType(RouteTablePropagatingVgws),
        deserialize_from="PropagatingVgws",
        default=[],
    )
    route_table_id = StringType(
        deserialize_from="RouteTableId", serialize_when_none=False
    )
    routes = ListType(
        ModelType(RouteTableRoutes), deserialize_from="Routes", default=[]
    )
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")
    main = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#RouteTables:routeTableId={self.route_table_id}",
        }


"""
DHCP Options
"""


class DHCPConfigurationValues(Model):
    value = StringType(deserialize_from="Value")


class DHCPOptionsDhcpConfigurations(Model):
    key = StringType(deserialize_from="Key")
    values = ListType(ModelType(DHCPConfigurationValues), deserialize_from="Values")


class DHCPOptions(Model):
    dhcp_configurations = ListType(
        ModelType(DHCPOptionsDhcpConfigurations), deserialize_from="DhcpConfigurations"
    )
    dhcp_options_id = StringType(deserialize_from="DhcpOptionsId")
    owner_id = StringType(deserialize_from="OwnerId")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    account_id = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#dhcpOptions:DhcpOptionsId={self.dhcp_options_id}",
        }


"""
SUBNET
"""


class Ipv6CidrBlockState(Model):
    state = StringType(
        deserialize_from="State",
        choices=(
            "associating",
            "associated",
            "disassociating",
            "disassociated",
            "failing",
            "failed",
        ),
    )
    status_message = StringType(deserialize_from="StatusMessage")


class SubnetIpv6CidrBlockAssociationSet(Model):
    association_id = StringType(deserialize_from="AssociationId")
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")
    ipv6_cidr_block_state = ModelType(
        Ipv6CidrBlockState, deserialize_from="Ipv6CidrBlockState"
    )


class Subnet(AWSCloudService):
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
    assign_ipv6_address_on_creation = BooleanType(
        deserialize_from="AssignIpv6AddressOnCreation"
    )
    ipv6_cidr_block_association_set = ListType(
        ModelType(SubnetIpv6CidrBlockAssociationSet),
        deserialize_from="Ipv6CidrBlockAssociationSet",
    )
    subnet_arn = StringType(deserialize_from="SubnetArn")
    outpost_arn = StringType(deserialize_from="OutpostArn")
    nat_gateways = ListType(ModelType(NATGateway))
    route_table = ModelType(RouteTable)
    network_acl = ModelType(NetworkACL)
    region_name = StringType(default="")
    subnet_type = StringType(choices=["public", "private"], default="private")

    def reference(self, region_code):
        return {
            "resource_id": self.subnet_arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#subnets:SubnetId={self.subnet_id}",
        }


"""
VPC
"""


class CidrBlock(Model):
    cidr_block = StringType(deserialize_from="CidrBlock")


class CidrBlockState(Model):
    state = StringType(
        deserialize_from="State",
        choices=(
            "associating",
            "associated",
            "disassociating",
            "disassociated",
            "failing",
            "failed",
        ),
    )
    status_message = StringType(deserialize_from="StatusMessage")


class VPCIpv6CidrBlockAssociationSet(Model):
    association_id = StringType(deserialize_from="AssociationId")
    ipv6_cidr_block = StringType(deserialize_from="Ipv6CidrBlock")
    ipv6_cidr_block_state = ModelType(
        Ipv6CidrBlockState, deserialize_from="Ipv6CidrBlockState"
    )
    network_border_group = StringType(deserialize_from="NetworkBorderGroup")
    ipv6_pool = StringType(deserialize_from="Ipv6Pool")


class VPCCidrBlockAssociationSet(Model):
    association_id = StringType(deserialize_from="AssociationId")
    cidr_block = StringType(deserialize_from="CidrBlock")
    cidr_block_state = ModelType(CidrBlockState, deserialize_from="CidrBlockState")


class VPC(AWSCloudService):
    arn = StringType(default="")
    name = StringType(default="")
    cidr_blocks = ListType(ModelType(CidrBlock))
    dhcp_options_id = StringType(deserialize_from="DhcpOptionsId")
    dhcp_option = ModelType(DHCPOptions)
    state = StringType(deserialize_from="State", choices=("pending", "available"))
    vpc_id = StringType(deserialize_from="VpcId")
    owner_id = StringType(deserialize_from="OwnerId")
    instance_tenancy = StringType(
        deserialize_from="InstanceTenancy", choices=("default", "dedicated", "host")
    )
    ipv6_cidr_block_association_set = ListType(
        ModelType(VPCIpv6CidrBlockAssociationSet),
        deserialize_from="Ipv6CidrBlockAssociationSet",
    )
    cidr_block_association_set = ListType(
        ModelType(VPCCidrBlockAssociationSet),
        deserialize_from="CidrBlockAssociationSet",
    )
    is_default = BooleanType(deserialize_from="IsDefault")
    subnets = ListType(ModelType(Subnet))
    route_tables = ListType(ModelType(RouteTable))
    main_route_table_id = StringType()
    main_network_acl_id = StringType()
    egress_only_internet_gateway = ModelType(
        EgressOnlyInternetGateway, serialize_when_none=False
    )
    endpoints = ListType(ModelType(Endpoint))
    peering_connections = ListType(ModelType(PeeringConnection))
    account_id = StringType(default="")
    nat_gateways = ListType(ModelType(NATGateway))
    internet_gateway = ModelType(InternetGateway, serialize_when_none=False)
    transit_gateway = ModelType(TransitGateway, serialize_when_none=False)
    vpn_gateway = ModelType(VPNGateway, serialize_when_none=False)
    enable_dns_support = StringType(choices=("Enabled", "Disabled"))
    enable_dns_hostnames = StringType(choices=("Enabled", "Disabled"))

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/vpc/home?region={region_code}#vpcs:VpcId={self.vpc_id}",
        }
