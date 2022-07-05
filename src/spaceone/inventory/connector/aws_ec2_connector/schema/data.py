import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


"""
AMI
"""
class ImageBlockDeviceMappingsEBS(Model):
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination", serialize_when_none=False)
    iops = IntType(deserialize_from="Iops", serialize_when_none=False)
    snapshot_id = StringType(deserialize_from="SnapshotId", serialize_when_none=False)
    volume_size = IntType(deserialize_from="VolumeSize", serialize_when_none=False)
    volume_type = StringType(deserialize_from="VolumeType",
                             choices=("standard", "io1", "io2", "gp2", "gp3", "sc1", "st1"),
                             serialize_when_none=False)
    kms_key_id = StringType(deserialize_from="KmsKeyId", serialize_when_none=False)
    encrypted = BooleanType(deserialize_from="Encrypted", serialize_when_none=False)


class ImageStateReason(Model):
    code = StringType(deserialize_from="Code", serialize_when_none=False)
    message = StringType(deserialize_from="Message", serialize_when_none=False)


class ImageProductCodes(Model):
    product_code_id = StringType(deserialize_from="ProductCodeId", serialize_when_none=False)
    product_code_type = StringType(deserialize_from="ProductCodeType", choices=("devpay", "marketplace"),
                                   serialize_when_none=False)


class ImageBlockDeviceMappings(Model):
    device_name = StringType(deserialize_from="DeviceName", serialize_when_none=False)
    virtual_name = StringType(deserialize_from="VirtualName", serialize_when_none=False)
    ebs = ModelType(ImageBlockDeviceMappingsEBS, deserialize_from="Ebs", serialize_when_none=False)
    no_device = StringType(deserialize_from="NoDevice", serialize_when_none=False)


class LaunchPermission(Model):
    user_id = StringType(deserialize_from='UserId', serialize_when_none=False)


class Image(AWSCloudService):
    image_id = StringType(deserialize_from="ImageId", serialize_when_none=False)
    name = StringType(deserialize_from="Name", serialize_when_none=False)
    architecture = StringType(deserialize_from="Architecture", choices=("i386", "x86_64", "arm64"),
                              serialize_when_none=False)
    creation_date = StringType(deserialize_from="CreationDate", serialize_when_none=False)
    image_location = StringType(deserialize_from="ImageLocation", serialize_when_none=False)
    image_type = StringType(deserialize_from="ImageType", choices=("machine", "kernel", "ramdisk"),
                            serialize_when_none=False)
    public = BooleanType(deserialize_from="Public", serialize_when_none=False)
    kernel_id = StringType(deserialize_from="KernelId", serialize_when_none=False)
    owner_id = StringType(deserialize_from="OwnerId", serialize_when_none=False)
    platform = StringType(deserialize_from="Platform", default="Other Linux", serialize_when_none=False)
    platform_details = StringType(deserialize_from="PlatformDetails", serialize_when_none=False)
    usage_operation = StringType(deserialize_from="UsageOperation", serialize_when_none=False)
    product_codes = ListType(ModelType(ImageProductCodes), deserialize_from="ProductCodes", serialize_when_none=False)
    ramdisk_id = StringType(deserialize_from="RamdiskId", serialize_when_none=False)
    state = StringType(deserialize_from="State", choices=("pending", "available", "invalid", "deregistered",
                                                          "transient", "failed", "error"),
                       serialize_when_none=False)
    block_device_mappings = ListType(ModelType(ImageBlockDeviceMappings),
                                     deserialize_from="BlockDeviceMappings",
                                     serialize_when_none=False)
    description = StringType(deserialize_from="Description", serialize_when_none=False)
    ena_support = BooleanType(deserialize_from="EnaSupport", serialize_when_none=False)
    hypervisor = StringType(deserialize_from="Hypervisor", choices=("ovm", "xen"), serialize_when_none=False)
    image_owner_alias = StringType(deserialize_from="ImageOwnerAlias", serialize_when_none=False)
    root_device_name = StringType(deserialize_from="RootDeviceName", serialize_when_none=False)
    root_device_type = StringType(deserialize_from="RootDeviceType", choices=("ebs", "instance-store"),
                                  serialize_when_none=False)
    sriov_net_support = StringType(deserialize_from="SriovNetSupport", serialize_when_none=False)
    state_reason = ModelType(ImageStateReason, deserialize_from="StateReason", serialize_when_none=False)
    virtualization_type = StringType(deserialize_from="VirtualizationType", choices=("hvm", "paravirtual"),
                                     serialize_when_none=False)
    launch_permissions = ListType(ModelType(LaunchPermission), serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.image_id,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Images:visibility=owned-by-me;imageId={self.image_id};sort=name"
        }



"""
SECURITY GROUP
"""
class InstanceState(Model):
    code = IntType(deserialize_from="Code")
    name = StringType(deserialize_from="Name", choices=("pending", "running", "shutting-down",
                                                        "terminated", "stopping", "stopped"))


class InstanceSecurityGroup(Model):
    group_name = StringType(deserialize_from="GroupName")
    group_id = StringType(deserialize_from="GroupId")


class InstanceTags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class Instance(Model):
    instance_id = StringType(deserialize_from="InstanceId")
    instance_name = StringType()
    state = ModelType(InstanceState, deserialize_from="State")
    subnet_id = StringType(deserialize_from="SubnetId")
    vpc_id = StringType(deserialize_from="VpcId")
    private_ip_address = StringType(deserialize_from="PrivateIpAddress")
    private_dns_name = StringType(deserialize_from="PrivateDnsName")
    public_ip_address = StringType(deserialize_from="PublicIpAddress")
    public_dns_name = StringType(deserialize_from="PublicDnsName")
    architecture = StringType(deserialize_from="Architecture")
    security_groups = ListType(ModelType(InstanceSecurityGroup), deserialize_from="SecurityGroups")
    tags = ListType(ModelType(InstanceTags), deserialize_from="Tags", default=[])


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


class SecurityGroup(AWSCloudService):
    description = StringType(deserialize_from="Description")
    group_name = StringType(deserialize_from="GroupName")
    ip_permissions = ListType(ModelType(SecurityGroupIpPermission))
    owner_id = StringType(deserialize_from="OwnerId")
    group_id = StringType(deserialize_from="GroupId")
    ip_permissions_egress = ListType(ModelType(SecurityGroupIpPermission))
    vpc_id = StringType(deserialize_from="VpcId")
    instances = ListType(ModelType(Instance), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.group_id,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#SecurityGroups:group-id={self.group_id}"
        }
