import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class ElasticIPAddressTags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class ElasticIPAddress(Model):
    name = StringType(default="")
    instance_id = StringType(deserialize_from="InstanceId")
    public_ip = StringType(deserialize_from="PublicIp")
    public_dns = StringType()
    nat_gateway_id = StringType()
    account_id = StringType()
    allocation_id = StringType(deserialize_from="AllocationId")
    association_id = StringType(deserialize_from="AssociationId")
    domain = StringType(deserialize_from="Domain", choices=("vpc", "standard"))
    network_interface_id = StringType(deserialize_from="NetworkInterfaceId")
    network_interface_owner_id = StringType(deserialize_from="NetworkInterfaceOwnerId")
    private_ip_address = StringType(deserialize_from="PrivateIpAddress")
    tags = ListType(ModelType(ElasticIPAddressTags), deserialize_from="Tags")
    public_ipv4_pool = StringType(deserialize_from="PublicIpv4Pool")
    network_border_group = StringType(deserialize_from="NetworkBorderGroup")
    customer_owned_ip = StringType(deserialize_from="CustomerOwnedIp")
    customer_owned_ipv4_pool = StringType(deserialize_from="CustomerOwnedIpv4Pool")
    region_name = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.public_ip,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={self.region_name}#ElasticIpDetails:PublicIp={self.public_ip}"
        }
