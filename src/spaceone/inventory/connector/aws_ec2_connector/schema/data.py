import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


"""
AMI
"""
class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class ImageBlockDeviceMappingsEBS(Model):
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination")
    iops = IntType(deserialize_from="Iops")
    snapshot_id = StringType(deserialize_from="SnapshotId")
    volume_size = IntType(deserialize_from="VolumeSize")
    volume_type = StringType(deserialize_from="VolumeType",
                             choices=("standard", "io1", "io2", "gp2", "gp3", "sc1", "st1"))
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    encrypted = BooleanType(deserialize_from="Encrypted")


class ImageStateReason(Model):
    code = StringType(deserialize_from="Code")
    message = StringType(deserialize_from="Message")


class ImageProductCodes(Model):
    product_code_id = StringType(deserialize_from="ProductCodeId")
    product_code_type = StringType(deserialize_from="ProductCodeType", choices=("devpay", "marketplace"))


class ImageBlockDeviceMappings(Model):
    device_name = StringType(deserialize_from="DeviceName")
    virtual_name = StringType(deserialize_from="VirtualName")
    ebs = ModelType(ImageBlockDeviceMappingsEBS, deserialize_from="Ebs")
    no_device = StringType(deserialize_from="NoDevice")


class LaunchPermission(Model):
    user_id = StringType(deserialize_from='UserId')


class Image(Model):
    architecture = StringType(deserialize_from="Architecture", choices=("i386", "x86_64", "arm64"))
    creation_date = StringType(deserialize_from="CreationDate")
    image_id = StringType(deserialize_from="ImageId")
    image_location = StringType(deserialize_from="ImageLocation")
    image_type = StringType(deserialize_from="ImageType", choices=("machine", "kernel", "ramdisk"))
    public = BooleanType(deserialize_from="Public")
    kernel_id = StringType(deserialize_from="KernelId")
    owner_id = StringType(deserialize_from="OwnerId")
    platform = StringType(deserialize_from="Platform", default="Other Linux")
    platform_details = StringType(deserialize_from="PlatformDetails")
    usage_operation = StringType(deserialize_from="UsageOperation")
    product_codes = ListType(ModelType(ImageProductCodes), deserialize_from="ProductCodes")
    ramdisk_id = StringType(deserialize_from="RamdiskId")
    state = StringType(deserialize_from="State", choices=("pending", "available", "invalid", "deregistered",
                                                          "transient", "failed", "error"))
    block_device_mappings = ListType(ModelType(ImageBlockDeviceMappings, deserialize_from="BlockDeviceMappings"))
    description = StringType(deserialize_from="Description")
    ena_support = BooleanType(deserialize_from="EnaSupport")
    hypervisor = StringType(deserialize_from="Hypervisor", choices=("ovm", "xen"))
    image_owner_alias = StringType(deserialize_from="ImageOwnerAlias")
    name = StringType(deserialize_from="Name")
    root_device_name = StringType(deserialize_from="RootDeviceName")
    root_device_type = StringType(deserialize_from="RootDeviceType", choices=("ebs", "instance-store"))
    sriov_net_support = StringType(deserialize_from="SriovNetSupport")
    state_reason = ModelType(ImageStateReason, deserialize_from="StateReason")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    virtualization_type = StringType(deserialize_from="VirtualizationType", choices=("hvm", "paravirtual"))
    launch_permissions = ListType(ModelType(LaunchPermission))

    def reference(self, region_code):
        return {
            "resource_id": self.image_id,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Images:visibility=owned-by-me;imageId={self.image_id};sort=name"
        }



"""
SECURITY GROUP
"""
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
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    vpc_id = StringType(deserialize_from="VpcId")
    account_id = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.group_id,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#SecurityGroups:group-id={self.group_id}"
        }
