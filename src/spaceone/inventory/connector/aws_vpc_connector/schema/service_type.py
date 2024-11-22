import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import (
    TextDyField,
    ListDyField,
    DateTimeDyField,
    EnumDyField,
    SearchField,
)
from spaceone.inventory.libs.schema.resource import (
    CloudServiceTypeResource,
    CloudServiceTypeResponse,
    CloudServiceTypeMeta,
)
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
VPC
"""
vpc_total_count_conf = os.path.join(current_dir, "widget/vpc_total_count.yaml")
vpc_count_by_region_conf = os.path.join(current_dir, "widget/vpc_count_by_region.yaml")
vpc_count_by_account_conf = os.path.join(
    current_dir, "widget/vpc_count_by_account.yaml"
)

cst_vpc = CloudServiceTypeResource()
cst_vpc.name = "VPC"
cst_vpc.provider = "aws"
cst_vpc.group = "VPC"
cst_vpc.labels = ["Networking"]
cst_vpc.is_primary = True
cst_vpc.service_code = "AmazonVPC"
cst_vpc.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC.svg",
}

cst_vpc._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("VPC ID", "data.vpc_id"),
        EnumDyField.data_source(
            "State",
            "data.state",
            default_state={"safe": ["available"], "warning": ["pending"]},
        ),
        # TextDyField.data_source('CIDR', 'data.cidr_block'),
        ListDyField.data_source(
            "CIDR",
            "data.cidr_blocks",
            options={"sub_key": "cidr_block", "delimiter": "<br>"},
        ),
        TextDyField.data_source("Main Route Table", "data.main_route_table_id"),
        TextDyField.data_source("Main Network ACL", "data.main_network_acl_id"),
        TextDyField.data_source("Tenancy", "data.instance_tenancy"),
        EnumDyField.data_source(
            "Default VPC",
            "data.is_default",
            default_badge={"indigo.500": ["true"], "coral.600": ["false"]},
        ),
        TextDyField.data_source("Owner", "data.owner_id"),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        TextDyField.data_source(
            "DHCP Options ID", "data.dhcp_options_id", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Enable DNS Hostnames",
            "data.enable_dns_hostnames",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Enable DNS Support",
            "data.enable_dns_support",
            options={"is_optional": True},
        ),
        ListDyField.data_source(
            "Subnet ARNs",
            "data.subnets",
            options={"sub_key": "subnet_arn", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Subnet IDs",
            "data.subnets",
            options={"sub_key": "subnet_id", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Subnet Names",
            "data.subnets",
            options={"sub_key": "name", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Subnet CIDRs",
            "data.subnets",
            options={"sub_key": "cidr_block", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Subnet Availability Zones",
            "data.subnets",
            options={
                "sub_key": "availability_zone",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        ListDyField.data_source(
            "NAT Gatway Names",
            "data.nat_gateways",
            options={"sub_key": "name", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "NAT Gatway ARNs",
            "data.nat_gateways",
            options={"sub_key": "arn", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Endpoint ARNs",
            "data.endpoints",
            options={"sub_key": "arn", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Endpoint Names",
            "data.endpoints",
            options={"sub_key": "name", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Peering Connection Names",
            "data.peering_connections",
            options={"sub_key": "name", "delimiter": "<br>", "is_optional": True},
        ),
        TextDyField.data_source(
            "Egress Only Internet Gateway ARN",
            "data.egress_only_internet_gateway.arn",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Egress Only Internet Gateway Name",
            "data.egress_only_internet_gateway.name",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Internet Gateway ARN",
            "data.internet_gateway.arn",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Internet Gateway Name",
            "data.internet_gateway.name",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Transit Gateway ARN",
            "data.transit_gateway.transit_gateway_arn",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Transit Gateway Name",
            "data.transit_gateway.name",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Transit Gateway ID",
            "data.transit_gateway.transit_gateway_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Gateway ID",
            "data.vpn_gateway.vpn_gateway_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Gateway Name", "data.vpn_gateway.name", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "VPN Connection ID",
            "data.vpn_gateway.vpn_connection.vpn_connection_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Name",
            "data.vpn_gateway.vpn_connection.name",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
            },
        ),
        # SearchField.set(name='CIDR', key='data.cidr_block'),
        SearchField.set(name="CIDR", key="data.cidr_blocks.cidr_block"),
        SearchField.set(name="Default VPC", key="data.is_default", data_type="boolean"),
        SearchField.set(name="Subnet ID", key="data.subnets.subnet_id"),
        SearchField.set(name="Availability Zone", key="data.subnets.availability_zone"),
        SearchField.set(
            name="Internet Gateway ID", key="data.internet_gateway.internet_gateway_id"
        ),
        SearchField.set(name="Internet Gateway Name", key="data.internet_gateway.name"),
        SearchField.set(name="NAT Gateway ID", key="data.nat_gateways.nat_gateway_id"),
        SearchField.set(name="NAT Gateway Name", key="data.nat_gateways.name"),
        SearchField.set(name="Endpoint ID", key="data.endpoints.vpc_endpoint_id"),
        SearchField.set(
            name="Peering Connection ID",
            key="data.peering_connections.vpc_peering_connection_id",
        ),
        SearchField.set(
            name="Egress Only Internet Gateway ID",
            key="data.egress_only_internet_gateway.egress_only_internet_gateway_id",
        ),
        SearchField.set(name="VPN Gateway ID", key="data.vpn_gateway.vpn_gateway_id"),
        SearchField.set(name="VPN Gateway Name", key="data.vpn_gateway.name"),
        SearchField.set(
            name="Transit Gateway ID", key="data.transit_gateway.transit_gateway_id"
        ),
        SearchField.set(name="Transit Gateway Name", key="data.transit_gateway.name"),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(vpc_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(vpc_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(vpc_count_by_account_conf)),
    ],
)

"""
SUBNET
"""
subnet_total_count_conf = os.path.join(current_dir, "widget/subnet_total_count.yaml")
subnet_count_by_region_conf = os.path.join(
    current_dir, "widget/subnet_count_by_region.yaml"
)
subnet_count_by_account_conf = os.path.join(
    current_dir, "widget/subnet_count_by_account.yaml"
)

cst_subnet = CloudServiceTypeResource()
cst_subnet.name = "Subnet"
cst_subnet.provider = "aws"
cst_subnet.group = "VPC"
cst_subnet.labels = ["Networking"]
cst_subnet.service_code = "AmazonVPC"
cst_subnet.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC.svg",
}

cst_subnet._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Subnet ID", "data.subnet_id"),
        EnumDyField.data_source(
            "State",
            "data.state",
            default_state={"safe": ["available"], "warning": ["pending"]},
        ),
        TextDyField.data_source("CIDR", "data.cidr_block"),
        TextDyField.data_source("AZ", "data.availability_zone"),
        EnumDyField.data_source(
            "Type",
            "instance_type",
            default_badge={"indigo.500": ["public"], "coral.600": ["private"]},
        ),
        TextDyField.data_source("VPC", "data.vpc_id"),
        TextDyField.data_source(
            "ARN", "data.subnet_arn", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Route Table ID",
            "data.route_table.route_table_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Route Table ARN", "data.route_table.arn", options={"is_optional": True}
        ),
        ListDyField.data_source(
            "NAT Gateway ARNs",
            "data.nat_gateways",
            options={"sub_key": "arn", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "NAT Gateway IDs",
            "data.nat_gateways",
            options={
                "sub_key": "nat_gateway_id",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        ListDyField.data_source(
            "NAT Gateway Names",
            "data.nat_gateways",
            options={"sub_key": "name", "delimiter": "<br>", "is_optional": True},
        ),
        TextDyField.data_source(
            "Network ACL ARN", "data.network_acl.arn", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Network ACL ID",
            "data.network_acl.network_acl_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Network ACL Name", "data.network_acl.name", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Available IP Address Count",
            "data.available_ip_address_count",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Assign IPv6 on Creation",
            "data.assign_ipv6_address_on_creation",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Default for Availability Zone",
            "data.default_for_az",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Public IP on Launch",
            "data.map_public_ip_on_launch",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Subnet ID", key="data.subnet_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
            },
        ),
        SearchField.set(
            name="Subnet Type",
            key="instance_type",
            enums={
                "public": {"label": "Public"},
                "private": {"label": "Private"},
            },
        ),
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(name="CIDR", key="data.cidr_block"),
        SearchField.set(
            name="Available IP Address Count",
            key="data.available_ip_address_count",
            data_type="integer",
        ),
        SearchField.set(name="Availability Zone", key="data.availability_zone"),
        SearchField.set(name="Route Table ID", key="data.route_table.route_table_id"),
        SearchField.set(name="Network ACL ID", key="data.network_acl.network_acl_id"),
        SearchField.set(name="Default", key="data.default_for_az", data_type="boolean"),
        SearchField.set(
            name="Auto-assign Public IP",
            key="data.map_public_ip_on_launch",
            data_type="boolean",
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(subnet_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(subnet_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(subnet_count_by_account_conf)),
    ],
)

"""
ROUTE TABLE
"""
cst_rt = CloudServiceTypeResource()
cst_rt.name = "RouteTable"
cst_rt.provider = "aws"
cst_rt.group = "VPC"
cst_rt.labels = ["Networking"]
cst_rt.service_code = "AmazonVPC"
cst_rt.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC.svg",
}

cst_rt._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Route Table ID", "data.route_table_id"),
        ListDyField.data_source(
            "Subnet associations",
            "data.subnet_associations",
            options={"sub_key": "subnet_id", "delimiter": "<br>"},
        ),
        ListDyField.data_source(
            "Edge associations",
            "data.edge_associations",
            options={"sub_key": "gateway_id", "delimiter": "<br>"},
        ),
        EnumDyField.data_source(
            "Main",
            "data.main",
            default_badge={"indigo.500": ["Yes"], "coral.600": ["No"]},
        ),
        TextDyField.data_source("VPC ID", "data.vpc_id"),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        ListDyField.data_source(
            "Association Subnet ID",
            "data.subnet_associations",
            options={"sub_key": "subnet_id", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Route Target",
            "data.routes",
            options={"sub_key": "target", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Route Destination CIDR",
            "data.routes",
            options={
                "sub_key": "destination_cidr_block",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Route Table ID", key="data.route_table_id"),
        SearchField.set(
            name="Associated Subnet ID", key="data.subnet_associations.subnet_id"
        ),
        SearchField.set(
            name="Main",
            key="data.main",
            enums={
                "Yes": {"label": "Yes"},
                "No": {"label": "No"},
            },
        ),
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
)

"""
INTERNET GATEWAY
"""
igw_total_count_conf = os.path.join(current_dir, "widget/igw_total_count.yaml")
igw_count_by_region_conf = os.path.join(current_dir, "widget/igw_count_by_region.yaml")
igw_count_by_account_conf = os.path.join(
    current_dir, "widget/igw_count_by_account.yaml"
)

cst_igw = CloudServiceTypeResource()
cst_igw.name = "InternetGateway"
cst_igw.provider = "aws"
cst_igw.group = "VPC"
cst_igw.labels = ["Networking"]
cst_igw.service_code = "AmazonVPC"
cst_igw.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_Internet-Gateway_light-bg.svg",
}

cst_igw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Internet Gateway ID", "data.internet_gateway_id"),
        EnumDyField.data_source(
            "State",
            "data.state",
            default_state={
                "available": ["available"],
                "safe": ["attached"],
                "warning": ["attaching", "detaching"],
                "disable": ["detached"],
            },
        ),
        ListDyField.data_source(
            "VPC ID",
            "data.attachments",
            options={"sub_key": "vpc_id", "delimiter": "<br>"},
        ),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Internet Gateway ID", key="data.internet_gateway_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "blue.400"}},
                "attached": {"label": "Attached", "icon": {"color": "green.500"}},
                "attaching": {"label": "Attaching", "icon": {"color": "yellow.500"}},
                "detaching": {"label": "Detaching", "icon": {"color": "yellow.500"}},
                "detached": {"label": "Detached", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(igw_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(igw_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(igw_count_by_account_conf)),
    ],
)

"""
EGRESS ONLY INTERNET GATEWAY
"""
eoigw_total_count_conf = os.path.join(current_dir, "widget/eoigw_total_count.yaml")
eoigw_count_by_region_conf = os.path.join(
    current_dir, "widget/eoigw_count_by_region.yaml"
)
eoigw_count_by_account_conf = os.path.join(
    current_dir, "widget/eoigw_count_by_account.yaml"
)

cst_eoigw = CloudServiceTypeResource()
cst_eoigw.name = "EgressOnlyInternetGateway"
cst_eoigw.provider = "aws"
cst_eoigw.group = "VPC"
cst_eoigw.labels = ["Networking"]
cst_eoigw.service_code = "AmazonVPC"
cst_eoigw.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_Internet-Gateway_light-bg.svg",
}
cst_eoigw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source(
            "Egress Only Internet Gateway ID", "data.egress_only_internet_gateway_id"
        ),
        ListDyField.data_source(
            "State",
            "data.attachments",
            options={
                "delimiter": "<br>",
                "sub_key": "state",
            },
        ),
        ListDyField.data_source(
            "VPC ID",
            "data.attachments",
            options={
                "delimiter": "<br>",
                "sub_key": "vpc_id",
            },
        ),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(
            name="Egress Only Gateway ID", key="data.egress_only_internet_gateway_id"
        ),
        SearchField.set(
            name="State",
            key="data.attachments.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "blue.400"}},
                "attached": {"label": "Attached", "icon": {"color": "green.500"}},
                "attaching": {"label": "Attaching", "icon": {"color": "yellow.500"}},
                "detaching": {"label": "Detaching", "icon": {"color": "yellow.500"}},
                "detached": {"label": "Detached", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="VPC ID", key="data.attachments.vpc_id"),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(eoigw_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(eoigw_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(eoigw_count_by_account_conf)),
    ],
)

"""
NAT GATEWAY
"""
natgw_total_count_conf = os.path.join(current_dir, "widget/natgw_total_count.yaml")
natgw_count_by_region_conf = os.path.join(
    current_dir, "widget/natgw_count_by_region.yaml"
)
natgw_count_by_account_conf = os.path.join(
    current_dir, "widget/natgw_count_by_account.yaml"
)

cst_natgw = CloudServiceTypeResource()
cst_natgw.name = "NATGateway"
cst_natgw.provider = "aws"
cst_natgw.group = "VPC"
cst_natgw.labels = ["Networking"]
cst_natgw.service_code = "AmazonVPC"
cst_natgw.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_NAT-Gateway_light-bg.svg",
}
cst_natgw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("NAT Gateway ID", "data.nat_gateway_id"),
        EnumDyField.data_source(
            "Status",
            "data.state",
            default_state={
                "safe": ["available"],
                "warning": [
                    "pending",
                    "deleting",
                ],
                "alert": ["failed"],
                "disable": ["deleted"],
            },
        ),
        ListDyField.data_source(
            "Elastic IP",
            "data.nat_gateway_addresses",
            options={"sub_key": "public_ip", "delimiter": "<br>"},
        ),
        ListDyField.data_source(
            "Private IP",
            "data.nat_gateway_addresses",
            options={"sub_key": "private_ip", "delimiter": "<br>"},
        ),
        ListDyField.data_source(
            "Network Interface",
            "data.nat_gateway_addresses",
            options={"sub_key": "network_interface_id", "delimiter": "<br>"},
        ),
        TextDyField.data_source("VPC ID", "data.vpc_id"),
        TextDyField.data_source("Subnet", "data.subnet_id"),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        ListDyField.data_source(
            "Private IP",
            "data.nat_gateway_addresses",
            options={"sub_key": "private_ip", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Public IP",
            "data.nat_gateway_addresses",
            options={"sub_key": "public_ip", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "Network Interface ID",
            "data.nat_gateway_addresses",
            options={
                "sub_key": "network_interface_id",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="NAT Gateway ID", key="data.nat_gateway_id"),
        SearchField.set(
            name="Status",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "failed": {"label": "Failed", "icon": {"color": "red.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="Elastic IP", key="data.nat_gateway_addresses.public_ip"),
        SearchField.set(name="Private IP", key="data.nat_gateway_addresses.private_ip"),
        SearchField.set(
            name="Network Interface ID",
            key="data.nat_gateway_addresses.network_interface_id",
        ),
        SearchField.set(name="Subnet ID", key="data.subnet_id"),
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(natgw_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(natgw_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(natgw_count_by_account_conf)),
    ],
)

"""
PEERING CONNECTION
"""
peerconn_total_count_conf = os.path.join(
    current_dir, "widget/peerconn_total_count.yaml"
)
peerconn_count_by_region_conf = os.path.join(
    current_dir, "widget/peerconn_count_by_region.yaml"
)
peerconn_count_by_account_conf = os.path.join(
    current_dir, "widget/peerconn_count_by_account.yaml"
)

cst_peerconn = CloudServiceTypeResource()
cst_peerconn.name = "PeeringConnection"
cst_peerconn.provider = "aws"
cst_peerconn.group = "VPC"
cst_peerconn.labels = ["Networking"]
cst_peerconn.service_code = "AmazonVPC"
cst_peerconn.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_Peering_light-bg.svg",
}
cst_peerconn._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source(
            "Peering Connection ID", "data.vpc_peering_connection_id"
        ),
        EnumDyField.data_source(
            "Status",
            "data.status.code",
            default_state={
                "safe": ["active"],
                "warning": [
                    "initiating-request",
                    "pending-acceptance",
                    "provisioning",
                    "deleting",
                ],
                "disable": ["deleted"],
                "alert": ["rejected", "failed", "expired"],
            },
        ),
        TextDyField.data_source("Requester VPC", "data.requester_vpc_info.vpc_id"),
        TextDyField.data_source(
            "Requester VPC CIDR", "data.requester_vpc_info.cidr_block"
        ),
        TextDyField.data_source("Requester Owner", "data.requester_vpc_info.owner_id"),
        TextDyField.data_source("Accepter VPC", "data.accepter_vpc_info.vpc_id"),
        TextDyField.data_source(
            "Accepter VPC CIDR", "data.accepter_vpc_info.cidr_block"
        ),
        TextDyField.data_source("Accepter Owner", "data.accepter_vpc_info.owner_id"),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(
            name="Peering Connection ID", key="data.vpc_peering_connection_id"
        ),
        SearchField.set(name="ARN", key="data.arn"),
        SearchField.set(
            name="Status",
            key="data.status.code",
            enums={
                "active": {"label": "Active", "icon": {"color": "green.500"}},
                "initiating-request": {
                    "label": "Initiating Request",
                    "icon": {"color": "yellow.500"},
                },
                "pending-acceptance": {
                    "label": "Pending Acceptance",
                    "icon": {"color": "yellow.500"},
                },
                "provisioning": {
                    "label": "Provisioning",
                    "icon": {"color": "yellow.500"},
                },
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "failed": {"label": "Failed", "icon": {"color": "red.500"}},
                "rejected": {"label": "Rejected", "icon": {"color": "red.500"}},
                "expired": {"label": "Expired", "icon": {"color": "red.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="Requester VPC ID", key="data.requester_vpc_info.vpc_id"),
        SearchField.set(name="Accepter VPC Id", key="data.accepter_vpc_info.vpc_id"),
        SearchField.set(
            name="Expiration Time", key="data.expiration_time", data_type="datetime"
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(peerconn_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(peerconn_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(peerconn_count_by_account_conf)),
    ],
)

"""
NETWORK ACL
"""
cst_nacl = CloudServiceTypeResource()
cst_nacl.name = "NetworkACL"
cst_nacl.provider = "aws"
cst_nacl.group = "VPC"
cst_nacl.labels = ["Networking"]
cst_nacl.service_code = "AmazonVPC"
cst_nacl.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_NACL_light-bg.svg",
}
cst_nacl._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Network ACL ID", "data.network_acl_id"),
        EnumDyField.data_source(
            "Default",
            "data.is_default",
            default_badge={"indigo.500": ["true"], "coral.600": ["false"]},
        ),
        TextDyField.data_source("VPC ID", "data.vpc_id"),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        TextDyField.data_source(
            "Default", "data.is_default", options={"is_optional": True}
        ),
        ListDyField.data_source(
            "Association Subnet ID",
            "data.associations",
            options={"sub_key": "subnet_id", "delimiter": "<br>", "is_optional": True},
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Network ACL ID", key="data.network_acl_id"),
        SearchField.set(name="Default", key="data.is_default", data_type="boolean"),
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(name="Inbound Protocol", key="data.inbound_entries.protocol"),
        SearchField.set(
            name="Inbound Port From", key="data.inbound_entries.port_range.port_from"
        ),
        SearchField.set(
            name="Inbound Port To", key="data.inbound_entries.port_range.port_to"
        ),
        SearchField.set(name="Inbound Source", key="data.inbound_entries.cidr_block"),
        SearchField.set(
            name="Inbound Allow/Deny",
            key="data.inbound_entries.rule_action",
            enums={
                "allow": {"label": "Allow"},
                "deny": {"label": "Deny"},
            },
        ),
        SearchField.set(name="Outbound Protocol", key="data.outbound_entries.protocol"),
        SearchField.set(
            name="Outbound Port From", key="data.outbound_entries.port_range.port_from"
        ),
        SearchField.set(
            name="Outbound Port To", key="data.outbound_entries.port_range.port_to"
        ),
        SearchField.set(name="Outbound Source", key="data.outbound_entries.cidr_block"),
        SearchField.set(
            name="Outbound Allow/Deny",
            key="data.outbound_entries.rule_action",
            enums={
                "allow": {"label": "Allow"},
                "deny": {"label": "Deny"},
            },
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
)

"""
ENDPOINT
"""
ep_total_count_conf = os.path.join(current_dir, "widget/ep_total_count.yaml")
ep_count_by_region_conf = os.path.join(current_dir, "widget/ep_count_by_region.yaml")
ep_count_by_account_conf = os.path.join(current_dir, "widget/ep_count_by_account.yaml")

cst_endpoint = CloudServiceTypeResource()
cst_endpoint.name = "Endpoint"
cst_endpoint.provider = "aws"
cst_endpoint.group = "VPC"
cst_endpoint.labels = ["Networking"]
cst_endpoint.service_code = "AmazonVPC"
cst_endpoint.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_Endpoints_light-bg.svg",
}
cst_endpoint._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Endpoint ID", "data.vpc_endpoint_id"),
        EnumDyField.data_source(
            "Status",
            "data.state",
            default_state={
                "safe": ["available"],
                "warning": ["pendingAcceptance", "pending", "deleting"],
                "disable": ["deleted"],
                "alert": ["rejected", "failed", "expired"],
            },
        ),
        TextDyField.data_source("VPC ID", "data.vpc_id"),
        TextDyField.data_source("Service Name", "data.service_name"),
        TextDyField.data_source("Endpoint Type", "instance_type"),
        TextDyField.data_source("ARN", "data.arn", options={"is_optional": True}),
        ListDyField.data_source(
            "Route Table IDs", "data.route_table_ids", options={"is_optional": True}
        ),
        ListDyField.data_source(
            "Subnet IDs", "data.subnet_ids", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Requester Managed", "data.requester_managed", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Private DNS Enabled",
            "data.private_dns_enabled",
            options={"is_optional": True},
        ),
        ListDyField.data_source(
            "Network Interface IDs",
            "data.network_interface_ids",
            options={"is_optional": True},
        ),
        ListDyField.data_source(
            "DNS Entries Names",
            "data.dns_entries",
            options={"sub_key": "dns_name", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "DNS Entries Hosted Zone ID",
            "data.dns_entries",
            options={
                "sub_key": "hosted_zone_id",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Endpoint ID", key="data.vpc_endpoint_id"),
        SearchField.set(
            name="Status",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pendingAcceptance": {
                    "label": "Pending Acceptance",
                    "icon": {"color": "yellow.500"},
                },
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "rejected": {"label": "Rejected", "icon": {"color": "red.500"}},
                "failed": {"label": "Failed", "icon": {"color": "red.500"}},
                "expired": {"label": "Expired", "icon": {"color": "red.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="VPC ID", key="data.vpc_id"),
        SearchField.set(name="Service Name", key="data.service_name"),
        SearchField.set(
            name="Type",
            key="instance_type",
            enums={
                "Interface": {"label": "Interface"},
                "Gateway": {"label": "Gateway"},
            },
        ),
        SearchField.set(name="DNS Name", key="data.dns_entries.dns_name"),
        SearchField.set(
            name="Private DNS Names enabled",
            key="data.private_dns_enabled",
            data_type="boolean",
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(ep_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(ep_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(ep_count_by_account_conf)),
    ],
)

"""
TRANSIT GATEWAY
"""
transitgw_total_count_conf = os.path.join(
    current_dir, "widget/transitgw_total_count.yaml"
)
transitgw_count_by_region_conf = os.path.join(
    current_dir, "widget/transitgw_count_by_region.yaml"
)
transitgw_count_by_account_conf = os.path.join(
    current_dir, "widget/transitgw_count_by_account.yaml"
)

cst_transitgw = CloudServiceTypeResource()
cst_transitgw.name = "TransitGateway"
cst_transitgw.provider = "aws"
cst_transitgw.group = "VPC"
cst_transitgw.labels = ["Networking"]
cst_transitgw.service_code = "AmazonVPC"
cst_transitgw.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_Transit_Gateway.svg",
}
cst_transitgw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Transit Gateway ID", "data.transit_gateway_id"),
        TextDyField.data_source("Owner ID", "data.owner_id"),
        EnumDyField.data_source(
            "State",
            "data.state",
            default_state={
                "safe": ["available"],
                "warning": ["pending", "modifying", "deleting"],
                "disable": ["deleted"],
            },
        ),
        TextDyField.data_source(
            "Transit Gateway Attachment ID",
            "data.vpc_attachment.transit_gateway_attachment_id",
            options={"is_optional": True}, ),
        TextDyField.data_source(
            "Transit Gateway Attachment Name",
            "data.vpc_attachment.name",
            options={"is_optional": True}, ),
        TextDyField.data_source(
            "ARN", "data.transit_gateway_arn", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "VPN ECMP Support",
            "data.options.vpn_ecmp_support",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "DNS Support", "data.options.dns_support", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "Association Default Route Table ID",
            "data.options.association_default_route_table_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Multicast Support",
            "data.options.multicast_support",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Default Route Table Association",
            "data.options.default_route_table_association",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Default Route Table Propagation",
            "data.options.default_route_table_propagation",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Propagation Default Route Table ID",
            "data.options.propagation_default_route_table_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Auto Accept Shared Attachments",
            "data.options.auto_accept_shared_attachments",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "Amazon Side ASN",
            "data.options.amazon_side_asn",
            options={"is_optional": True},
        ),
        ListDyField.data_source(
            "VPN Connection IDs",
            "data.vpn_connections",
            options={
                "sub_key": "vpn_connection_id",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        ListDyField.data_source(
            "VPN Connection Names",
            "data.vpn_connections",
            options={"sub_key": "name", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "VPN Connection Types",
            "data.vpn_connections",
            options={"sub_key": "type", "delimiter": "<br>", "is_optional": True},
        ),
        ListDyField.data_source(
            "VPN Connection Customer Gateway ID",
            "data.vpn_connections",
            options={
                "sub_key": "customer_gateway_id",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Transit Gateway ID", key="data.transit_gateway_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "modifying": {"label": "Modifying", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(
            name="Associated Route Table ID",
            key="data.transit_gateway_route_table.transit_gateway_route_table_id",
        ),
        SearchField.set(
            name="VPN Connection ID", key="data.vpn_connections.vpn_connection_id"
        ),
        SearchField.set(name="VPN Connection Name", key="data.vpn_connections.name"),
        SearchField.set(
            name="Customer Gateway ID", key="data.vpn_connections.customer_gateway_id"
        ),
        SearchField.set(
            name="VPN Gateway ID", key="data.vpn_connections.vpn_gateway_id"
        ),
        SearchField.set(name="AWS Account ID", key="account"),
        SearchField.set(name="Transit Gateway Attachment ID", key="data.vpc_attachment.transit_gateway_attachment_id"),
        SearchField.set(name="Transit Gateway Attachment Name", key="data.vpc_attachment.name")
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(transitgw_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(transitgw_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(transitgw_count_by_account_conf)),
    ],
)

"""
CUSTOMER GATEWAY
"""
customergw_total_count_conf = os.path.join(
    current_dir, "widget/customergw_total_count.yaml"
)
customergw_count_by_region_conf = os.path.join(
    current_dir, "widget/customergw_count_by_region.yaml"
)
customergw_count_by_account_conf = os.path.join(
    current_dir, "widget/customergw_count_by_account.yaml"
)

cst_customgw = CloudServiceTypeResource()
cst_customgw.name = "CustomerGateway"
cst_customgw.provider = "aws"
cst_customgw.group = "VPC"
cst_customgw.labels = ["Networking"]
cst_customgw.service_code = "AmazonVPC"
cst_customgw.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_Customer-Gateway_dark-bg.svg",
}
cst_customgw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("ID", "data.customer_gateway_id"),
        EnumDyField.data_source(
            "State",
            "data.state",
            default_state={
                "safe": ["available"],
                "warning": ["pending", "deleting"],
                "disable": ["deleted"],
            },
        ),
        TextDyField.data_source("Type", "instance_type"),
        TextDyField.data_source("IP Address", "data.ip_address"),
        TextDyField.data_source("BGP ASN", "data.bgp_asn"),
        TextDyField.data_source(
            "Certificate ARN", "data.certificate_arn", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "VPN Connection ID",
            "data.vpn_connection.vpn_connection_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Name",
            "data.vpn_connection.name",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Type",
            "data.vpn_connection.type",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Category",
            "data.vpn_connection.category",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection VPN Gateway ID",
            "data.vpn_connection.vpn_gateway_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Customer Gateway ID",
            "data.vpn_connection.customer_gateway_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Transit Gateway ID",
            "data.vpn_connection.transit_gateway_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Customer Gateway ID", key="data.customer_gateway_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="Type", key="instance_type"),
        SearchField.set(name="IP Address", key="data.ip_address"),
        SearchField.set(name="BGP ASN", key="data.bgp_asn"),
        SearchField.set(name="Device", key="data.device_name"),
        SearchField.set(
            name="VPN Connection ID", key="data.vpn_connection.vpn_connection_id"
        ),
        SearchField.set(name="VPN Connection Name", key="data.vpn_connection.name"),
        SearchField.set(
            name="VPN Connection State",
            key="data.vpn_connection.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(customergw_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(customergw_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(customergw_count_by_account_conf)),
    ],
)

"""
VPN CONNECTION
"""
vpnconn_total_count_conf = os.path.join(current_dir, "widget/vpnconn_total_count.yaml")
vpnconn_count_by_region_conf = os.path.join(
    current_dir, "widget/vpnconn_count_by_region.yaml"
)
vpnconn_count_by_account_conf = os.path.join(
    current_dir, "widget/vpnconn_count_by_account.yaml"
)

cst_vpnconn = CloudServiceTypeResource()
cst_vpnconn.name = "VPNConnection"
cst_vpnconn.provider = "aws"
cst_vpnconn.group = "VPC"
cst_vpnconn.labels = ["Networking"]
cst_vpnconn.service_code = "AmazonVPC"
cst_vpnconn.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_VPN-Connection_dark-bg.svg",
}
cst_vpnconn._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("VPN ID", "data.vpn_connection_id"),
        EnumDyField.data_source(
            "State",
            "data.state",
            default_state={
                "safe": ["available"],
                "warning": ["pending", "deleting"],
                "disable": ["deleted"],
            },
        ),
        TextDyField.data_source("Virtual Private Gateway", "data.vpn_gateway_id"),
        TextDyField.data_source("Transit Gateway", "data.transit_gateway_id"),
        TextDyField.data_source("Customer Gateway", "data.customer_gateway_id"),
        TextDyField.data_source(
            "Customer Gateway Address", "data.customer_gateway_address"
        ),
        TextDyField.data_source("Type", "instance_type"),
        EnumDyField.data_source(
            "Category",
            "data.category",
            default_badge={"indigo.500": ["VPN"], "coral.500": ["VPN-Classic"]},
        ),
        ListDyField.data_source(
            "Virtual Gateway Telemetry: Outside IP",
            "data.vgw_telemetry",
            options={
                "sub_key": "outside_ip_address",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        TextDyField.data_source(
            "Enable Acceleration",
            "data.options.enable_acceleration",
            options={"is_optional": True},
        ),
        ListDyField.data_source(
            "VPN Tunnel: Outside IP",
            "data.options.tunnel_options",
            options={
                "sub_key": "outside_ip_address",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        ListDyField.data_source(
            "Routes: Destination CIDR",
            "data.routes",
            options={
                "sub_key": "destination_cidr_block",
                "delimiter": "<br>",
                "is_optional": True,
            },
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="VPN Connection ID", key="data.vpn_connection_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="Virtual Private Gateway ID", key="data.vpn_gateway_id"),
        SearchField.set(name="Customer Gateway ID", key="data.customer_gateway_id"),
        SearchField.set(name="Transit Gateway ID", key="data.transit_gateway_id"),
        SearchField.set(name="Type", key="instance_type"),
        SearchField.set(
            name="Category",
            key="data.category",
            enums={
                "VPN": {"label": "VPN"},
                "VPN-Classic": {"label": "VPN Classic"},
            },
        ),
        SearchField.set(
            name="VPN Tunnel IP", key="data.vgw_telemetry.outside_ip_address"
        ),
        SearchField.set(
            name="VPN Tunnel Status",
            key="data.vgw_telemetry.status",
            enums={
                "UP": {"label": "UP"},
                "DOWN": {"label": "DOWN"},
            },
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(vpnconn_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(vpnconn_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(vpnconn_count_by_account_conf)),
    ],
)

"""
VPN GATEWAY
"""
vpngw_total_count_conf = os.path.join(current_dir, "widget/vpngw_total_count.yaml")
vpngw_count_by_region_conf = os.path.join(
    current_dir, "widget/vpngw_count_by_region.yaml"
)
vpngw_count_by_account_conf = os.path.join(
    current_dir, "widget/vpngw_count_by_account.yaml"
)

cst_vpngw = CloudServiceTypeResource()
cst_vpngw.name = "VPNGateway"
cst_vpngw.provider = "aws"
cst_vpngw.group = "VPC"
cst_vpngw.labels = ["Networking"]
cst_vpngw.service_code = "AmazonVPC"
cst_vpngw.tags = {
    "spaceone:icon": f"{ASSET_URL}/Amazon-VPC_VPN-Gateway_dark-bg.svg",
}
cst_vpngw._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("ID", "data.vpn_gateway_id"),
        TextDyField.data_source("State", "data.state"),
        TextDyField.data_source("Type", "instance_type"),
        ListDyField.data_source(
            "VPC",
            "data.vpc_attachments",
            options={"sub_key": "vpc_id", "delimiter": "<br>"},
        ),
        TextDyField.data_source("ASN (Amazon side)", "data.amazon_side_asn"),
        TextDyField.data_source(
            "Availability Zone", "data.availability_zone", options={"is_optional": True}
        ),
        TextDyField.data_source(
            "VPN Connection ID",
            "data.vpn_connection.vpn_connection_id",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "VPN Connection Name",
            "data.vpn_connection.name",
            options={"is_optional": True},
        ),
        TextDyField.data_source(
            "AWS Account ID", "account", options={"is_optional": True}
        ),
    ],
    search=[
        SearchField.set(name="Virtual Private Gateway ID", key="data.vpn_gateway_id"),
        SearchField.set(
            name="State",
            key="data.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="Type", key="instance_type"),
        SearchField.set(name="VPC ID", key="data.vpc_attachments.vpc_id"),
        SearchField.set(name="ASN", key="data.amazon_side_asn"),
        SearchField.set(
            name="VPN Connection ID", key="data.vpn_connection.vpn_connection_id"
        ),
        SearchField.set(name="VPN Connection Name", key="data.vpn_connection.name"),
        SearchField.set(
            name="VPN Connection Status",
            key="data.vpn_connection.state",
            enums={
                "available": {"label": "Available", "icon": {"color": "green.500"}},
                "pending": {"label": "Pending", "icon": {"color": "yellow.500"}},
                "deleting": {"label": "Deleting", "icon": {"color": "yellow.500"}},
                "deleted": {"label": "Deleted", "icon": {"color": "grey.500"}},
            },
        ),
        SearchField.set(name="AWS Account ID", key="account"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(vpngw_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(vpngw_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(vpngw_count_by_account_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_vpc}),
    CloudServiceTypeResponse({"resource": cst_subnet}),
    CloudServiceTypeResponse({"resource": cst_rt}),
    CloudServiceTypeResponse({"resource": cst_igw}),
    CloudServiceTypeResponse({"resource": cst_eoigw}),
    CloudServiceTypeResponse({"resource": cst_natgw}),
    CloudServiceTypeResponse({"resource": cst_peerconn}),
    CloudServiceTypeResponse({"resource": cst_nacl}),
    CloudServiceTypeResponse({"resource": cst_endpoint}),
    CloudServiceTypeResponse({"resource": cst_transitgw}),
    CloudServiceTypeResponse({"resource": cst_customgw}),
    CloudServiceTypeResponse({"resource": cst_vpnconn}),
    CloudServiceTypeResponse({"resource": cst_vpngw}),
]
