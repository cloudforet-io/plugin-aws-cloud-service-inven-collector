import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class SecurityGroupIpPermissionIpRanges(Model):
    cidr_ip = StringType(deserialize_from="CidrIp")
    description = StringType(deserialize_from="Description")


class SecurityGroupIpPermissionIpv6Ranges(Model):
    cidr_ipv6 = StringType(deserialize_from="CidrIpv6")
    description = StringType(deserialize_from="Description")


class SecurityGroupIpPermissionPrefixListIds(Model):
    description = StringType(deserialize_from="Description")
    prefix_list_id = StringType(deserialize_from="PrefixListId")


class SecurityGroupIpPermissionUserIdGroupPairs(Model):
    description = StringType(deserialize_from="Description")
    group_id = StringType(deserialize_from="GroupId")
    group_name = StringType(deserialize_from="GroupName")
    peering_status = StringType(deserialize_from="PeeringStatus")
    user_id = StringType(deserialize_from="UserId")
    vpc_id = StringType(deserialize_from="VpcId")
    vpc_peering_connection_id = StringType(deserialize_from="VpcPeeringConnectionId")


class SecurityGroupIpPermission(Model):
    from_port = IntType(deserialize_from="FromPort")
    ip_protocol = StringType(deserialize_from="IpProtocol")
    ip_ranges = ModelType(SecurityGroupIpPermissionIpRanges)
    ipv6_ranges = ModelType(SecurityGroupIpPermissionIpv6Ranges)
    prefix_list_ids = ListType(ModelType(SecurityGroupIpPermissionPrefixListIds, deserialize_from="PrefixListIds"))
    to_port = IntType(deserialize_from="ToPort")
    user_id_group_pairs = ModelType(SecurityGroupIpPermissionUserIdGroupPairs)
    protocol_display = StringType(default="")
    port_display = StringType(default="")
    source_display = StringType(default="")
    description_display = StringType(default="")


class SecurityGroup(Model):
    description = StringType(deserialize_from="Description")
    group_name = StringType(deserialize_from="GroupName")
    ip_permissions = ListType(ModelType(SecurityGroupIpPermission))
    owner_id = StringType(deserialize_from="OwnerId")
    group_id = StringType(deserialize_from="GroupId")
    ip_permissions_egress = ListType(ModelType(SecurityGroupIpPermission))
    tags = ListType(ModelType(Tags, deserialize_from="Tags"))
    vpc_id = StringType(deserialize_from="VpcId")
    account_id = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.group_id,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#SecurityGroups:group-id={self.group_id}"
        }
