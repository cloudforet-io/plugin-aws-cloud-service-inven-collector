import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)

'''
LAGS
'''
class Tags(Model):
    key = StringType(deserialize_from="key")
    value = StringType(deserialize_from="value")


class LAGConnections(Model):
    owner_account = StringType(deserialize_from="ownerAccount")
    connection_id = StringType(deserialize_from="connectionId")
    connection_name = StringType(deserialize_from="connectionName")
    connection_state = StringType(deserialize_from="connectionState", choices=("ordering", "requested", "pending",
                                                                               "available", "down", "deleting",
                                                                               "deleted", "rejected", "unknown"))
    region = StringType(deserialize_from="region")
    location = StringType(deserialize_from="location")
    bandwidth = StringType(deserialize_from="bandwidth")
    vlan = IntType(deserialize_from="vlan")
    partner_name = StringType(deserialize_from="partnerName")
    loa_issue_time = DateTimeType(deserialize_from="loaIssueTime")
    lag_id = StringType(deserialize_from="lagId")
    aws_device = StringType(deserialize_from="awsDevice")
    jumbo_frame_capable = BooleanType(deserialize_from="jumboFrameCapable")
    aws_device_v2 = StringType(deserialize_from="awsDeviceV2")
    has_logical_redundancy = StringType(deserialize_from="hasLogicalRedundancy", choices=("unknown","yes","no"))
    tags = ListType(ModelType(Tags))
    provider_name = StringType(deserialize_from="providerName")


class LAG(Model):
    connections_bandwidth = StringType(deserialize_from="connectionsBandwidth")
    number_of_connections = IntType(deserialize_from="numberOfConnections")
    lag_id = StringType(deserialize_from="lagId")
    owner_account = StringType(deserialize_from="ownerAccount")
    lag_name = StringType(deserialize_from="lagName")
    lag_state = StringType(deserialize_from="lagState", choices=("requested", "pending", "available", "down",
                                                                 "deleting", "deleted", "unknown"))
    location = StringType(deserialize_from="location")
    region = StringType(deserialize_from="region")
    minimum_links = IntType(deserialize_from="minimumLinks")
    aws_device = StringType(deserialize_from="awsDevice")
    aws_device_v2 = StringType(deserialize_from="awsDeviceV2")
    connections = ListType(ModelType(LAGConnections, deserialize_from="connections"))
    allows_hosted_connections = BooleanType(deserialize_from="allowsHostedConnections")
    jumbo_frame_capable = BooleanType(deserialize_from="jumboFrameCapable")
    has_logical_redundancy = StringType(deserialize_from="hasLogicalRedundancy", choices=("unknown", "yes", "no"))
    tags = ListType(ModelType(Tags, deserialize_from="tags"))
    provider_name = StringType(deserialize_from="providerName")
    account_id = StringType()

    def reference(self, region_code):
        return {
            "resource_id": self.lag_id,
            "external_link": f"https://console.aws.amazon.com/directconnect/v2/home?region={region_code}#/lags/arn:aws:directconnect:{region_code}:{self.owner_account}:{self.lag_id}"
        }


'''
VIRTUAL GATEWAY
'''
class VirtualPrivateGateway(Model):
    virtual_gateway_id = StringType(deserialize_from="virtualGatewayId")
    virtual_gateway_state = StringType(deserialize_from="virtualGatewayState")
    region = StringType(deserialize_from="region")
    owner_account = StringType(deserialize_from="ownerAccount")
    account_id = StringType()

    def reference(self, region_code):
        return {
            "resource_id": self.virtual_gateway_id,
            "external_link": f"https://console.aws.amazon.com/directconnect/v2/home?region={region_code}#/virtual-gateways/arn:aws:ec2:{region_code}:{self.owner_account}:{self.virtual_gateway_id}"
        }


'''
DIRECT CONNECT GATEWAY
'''
class DirectConnecGateway(Model):
    direct_connect_gateway_id = StringType(deserialize_from="directConnectGatewayId")
    direct_connect_gateway_name = StringType(deserialize_from="directConnectGatewayName")
    amazon_side_asn = IntType(deserialize_from="amazonSideAsn")
    owner_account = StringType(deserialize_from="ownerAccount")
    direct_connect_gateway_state = StringType(deserialize_from="directConnectGatewayState",choices=("pending",
                                                                                                    "available",
                                                                                                    "deleting",
                                                                                                    "deleted"))
    state_change_error = StringType(deserialize_from="stateChangeError")
    account_id = StringType()

    def reference(self, region_code):
        return {
            "resource_id": self.direct_connect_gateway_id,
            "external_link": f"https://console.aws.amazon.com/directconnect/v2/home?region={region_code}#/dxgateways/{self.direct_connect_gateway_id}"
        }


'''
VIRTUAL INTERFACE
'''
class VirtualInterfacerouteFilterPrefixes(Model):
    cidr = StringType(deserialize_from="cidr")


class VirtualInterfacebgpPeers(Model):
    bgp_peer_id = StringType(deserialize_from="bgpPeerId")
    asn = IntType(deserialize_from="asn")
    auth_key = StringType(deserialize_from="authKey")
    address_family = StringType(deserialize_from="addressFamily", choices=("ipv4", "ipv6"))
    amazon_address = StringType(deserialize_from="amazonAddress")
    customer_address = StringType(deserialize_from="customerAddress")
    bgp_peer_state = StringType(deserialize_from="bgpPeerState", choices=("verifying", "pending", "available",
                                                                          "deleting", "deleted"))
    bgp_status = StringType(deserialize_from="bgpStatus", choices=("up", "down", "unknown"))
    aws_device_v2 = StringType(deserialize_from="awsDeviceV2")


class VirtualInterface(Model):
    owner_account = StringType(deserialize_from="ownerAccount")
    virtual_interface_id = StringType(deserialize_from="virtualInterfaceId")
    location = StringType(deserialize_from="location")
    connection_id = StringType(deserialize_from="connectionId")
    virtual_interface_type = StringType(deserialize_from="virtualInterfaceType")
    virtual_interface_name = StringType(deserialize_from="virtualInterfaceName")
    vlan = IntType(deserialize_from="vlan")
    asn = IntType(deserialize_from="asn")
    amazon_side_asn = IntType(deserialize_from="amazonSideAsn")
    auth_key = StringType(deserialize_from="authKey")
    amazon_address = StringType(deserialize_from="amazonAddress")
    customer_address = StringType(deserialize_from="customerAddress")
    address_family = StringType(deserialize_from="addressFamily", choices=("ipv4", "ipv6"))
    virtual_interface_state = StringType(deserialize_from="virtualInterfaceState", choices=("confirming",
                                                                                            "verifying",
                                                                                            "pending",
                                                                                            "available",
                                                                                            "down",
                                                                                            "deleting",
                                                                                            "deleted",
                                                                                            "rejected",
                                                                                            "unknown"))
    customer_router_config = StringType(deserialize_from="customerRouterConfig")
    mtu = IntType(deserialize_from="mtu")
    jumbo_frame_capable = BooleanType(deserialize_from="jumboFrameCapable")
    virtual_gateway_id = StringType(deserialize_from="virtualGatewayId")
    direct_connect_gateway_id = StringType(deserialize_from="directConnectGatewayId")
    route_filter_prefixes = ListType(ModelType(VirtualInterfacerouteFilterPrefixes,
                                               deserialize_from="routeFilterPrefixes"))
    bgp_peers = ListType(ModelType(VirtualInterfacebgpPeers,
                                   deserialize_from="bgpPeers"))
    region = StringType(deserialize_from="region")
    aws_device_v2 = StringType(deserialize_from="awsDeviceV2")
    tags = ListType(ModelType(Tags, deserialize_from="tags"))
    account_id = StringType()
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.virtual_interface_id,
            "external_link": f"https://console.aws.amazon.com/directconnect/v2/home?region={region_code}#/virtual-interfaces/arn:aws:directconnect:{region_code}:{self.owner_account}:{self.virtual_interface_id}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/DX",
            "dimensions": [CloudWatchDimensionModel({'Name': 'VirtualInterfaceId', 'Value': self.virtual_interface_id})],
            "region_name": region_code
        }


'''
CONNECTION
'''
class Connection(Model):
    arn = StringType()
    owner_account = StringType(deserialize_from="ownerAccount")
    connection_id = StringType(deserialize_from="connectionId")
    connection_name = StringType(deserialize_from="connectionName")
    connection_state = StringType(deserialize_from="connectionState", choices=("ordering", "requested", "pending",
                                                                               "available", "down", "deleting",
                                                                               "deleted", "rejected", "unknown"))
    region = StringType(deserialize_from="region")
    location = StringType(deserialize_from="location")
    bandwidth = StringType(deserialize_from="bandwidth")
    vlan = IntType(deserialize_from="vlan")
    partner_name = StringType(deserialize_from="partnerName")
    loa_issue_time = DateTimeType(deserialize_from="loaIssueTime")
    lag_id = StringType(deserialize_from="lagId")
    aws_device = StringType(deserialize_from="awsDevice")
    jumbo_frame_capable = BooleanType(deserialize_from="jumboFrameCapable")
    aws_device_v2 = StringType(deserialize_from="awsDeviceV2")
    has_logical_redundancy = StringType(deserialize_from="hasLogicalRedundancy", choices=("unknown", "yes", "no"))
    tags = ListType(ModelType(Tags, deserialize_from="tags"))
    provider_name = StringType(deserialize_from="providerName")
    virtual_interfaces = ListType(ModelType(VirtualInterface))
    account_id = StringType()
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/directconnect/v2/home?region={region_code}#/connections/arn:aws:directconnect:{region_code}:{self.owner_account}:{self.connection_id}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/DX",
            "dimensions": [CloudWatchDimensionModel({'Name': 'ConnectionId', 'Value': self.connection_id})],
            "region_name": region_code
        }
