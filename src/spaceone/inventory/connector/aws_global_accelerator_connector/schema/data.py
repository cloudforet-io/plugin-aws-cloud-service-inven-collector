from schematics.types import StringType, ListType, ModelType, DateTimeType, IntType, FloatType, BooleanType
from schematics import Model
from spaceone.inventory.libs.schema.resource import AWSCloudService


class IpSets(Model):
    ip_addresses = ListType(StringType(), deserialize_from= "IpAddresses")
    ip_address_family = StringType(deserialize_from="IpAddressFamily")

class Events(Model):
    message = StringType(deserialize_from="Message")
    time = DateTimeType(deserialize_from="Timestamp")

class PortRanges(Model):
    from_port = IntType(deserialize_from="FromPort")
    to_port = IntType(deserialize_from="ToPort")

class Listener(Model):
    arn = StringType(deserialize_from="ListenerArn")
    port_ranges = ListType(ModelType(PortRanges), deserialize_from="PortRanges")
    protocol = StringType(deserialize_from="Protocol")
    endpoint_region = ListType(StringType(), deserialize_from="EndpointGroupRegion")
    port_display = ListType(StringType(), default=[])

class EndpointGroup(Model):
    arn = StringType(deserialize_from="EndpointGroupArn")
    region = StringType(deserialize_from="EndpointGroupRegion")
    traffic_dial = FloatType(deserialize_from="TrafficDialPercentage")
    
class Resources(Model):
    endpoint_id = StringType(deserialize_from="EndpointId")
    cidr = StringType(deserialize_from="Cidr")
    region = StringType(deserialize_from="Region")

class CrossAccountAttachments(AWSCloudService):
    arn = StringType(deserialize_from="AttachmentArn")
    name = StringType(deserialize_from="Name")
    principals = ListType(StringType(), deserialize_from="Principals")
    resources = ListType(ModelType(Resources), deserialize_from="Resources")
    modified_time = DateTimeType(deserialize_from="LastModifiedTime")
    created_at = DateTimeType(deserialize_from="CreatedTime")

    def reference(self):
        return{
            "resource_id": self.arn,
            "external_link": f"https://us-west-2.console.aws.amazon.com/globalaccelerator/home?region=ap-northeast-2#CrossAccountAttachmentDetails:AttachmentArn={self.arn}"
        }

class Accelerator(AWSCloudService):
    arn = StringType(deserialize_from = "AcceleratorArn")
    name = StringType(deserialize_from="Name")
    type = StringType(deserialize_from="Type")
    ip_address_type = StringType(deserialize_from="IpAddressType")
    enabled = StringType(deserialize_from="Enabled")
    ip_sets = ListType(ModelType(IpSets), deserialize_from="IpSets",default=[])
    ipv4_addresses = ListType(StringType(), deserialize_from="IPv4Addresses")
    ipv6_addresses = ListType(StringType(), deserialize_from="IPv6Addresses")
    dns_name = StringType(deserialize_from="DnsName")
    status = StringType(deserialize_from="Status")
    created_at = DateTimeType(deserialize_from="CreatedTime")
    edited_at = DateTimeType(deserialize_from="LastModifiedTime")
    dual_stack_dns_name = StringType(deserialize_from="DualStackDnsName")
    events = ListType(ModelType(Events), deserialize_from="Events")
    listeners = ListType(ModelType(Listener), deserialize_from="listeners")
    endpoints = ListType(ModelType(EndpointGroup), deserialize_from="endpoints")


    def reference(self):

        if self.type == "Customised routing":
            hash_fragment = f"CustomRoutingAcceleratorDetails:AcceleratorArn={self.arn}"
        else:
            hash_fragment = f"AcceleratorDetails:AcceleratorArn={self.arn}"
        external_link = (
            "https://us-west-2.console.aws.amazon.com/globalaccelerator/home"
            f"#{hash_fragment}"
        )

        return {
            "resource_id": self.arn,
            "external_link": external_link
        }