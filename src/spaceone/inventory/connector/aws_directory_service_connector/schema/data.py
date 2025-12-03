from schematics import Model
from schematics.types import StringType, ListType, ModelType, DateTimeType

from spaceone.inventory.libs.schema.resource import AWSCloudService

"""
Directories
"""

class RegionInfo(Model):
    primary_region = StringType(deserialize_from="PrimaryRegion")
    additional_region = ListType(StringType(),deserialize_from="AdditionalRegions")

class VpcSettings(Model):
    vpc_id = StringType(deserialize_from="VpcId")
    subnet_ids = ListType(StringType(), deserialize_from="SubnetIds")
    security_group_id = StringType(deserialize_from="SecurityGroupId")
    availability_zones = ListType(StringType(), deserialize_from="AvailabilityZones")

class ConnectSettings(Model):
    vpc_id = StringType(deserialize_from="VpcId")
    subnet_ids = ListType(StringType(), deserialize_from="SubnetIds")
    customer_user_name = StringType(deserialize_from="CustomerUserName")
    security_group_id = StringType(deserialize_from="SecurityGroupId")
    availability_zones = ListType(StringType(), deserialize_from="AvailabilityZones")
    connect_ips = ListType(StringType(), deserialize_from="ConnectIps")
    connect_ips_v6 = ListType(StringType(), deserialize_from="ConnectIpsV6")

class OwnerDirectoryDescription(Model):
    directory_id = StringType(deserialize_from="DirectoryId")
    account_id = StringType(deserialize_from="AccountId")

class Directory(AWSCloudService):
    name = StringType(deserialize_from="Name")
    short_name = StringType(deserialize_from="ShortName")
    id = StringType(deserialize_from="DirectoryId")
    type = StringType(deserialize_from="Type")
    size = StringType(deserialize_from="Size")
    alias = StringType(deserialize_from="Alias")
    access_url = StringType(deserialize_from="AccessUrl")
    description = StringType(deserialize_from="Description")
    dns_ip_addrs = ListType(StringType(), deserialize_from="DnsIpAddrs")
    dns_ipv6_addrs = ListType(StringType(), deserialize_from="DnsIpv6Addrs")
    edition = StringType(deserialize_from="Edition")
    regions_info = ModelType(RegionInfo,deserialize_from="RegionsInfo")
    multi_region = StringType(deserialize_from="MultiRegion")
    share_status = StringType(deserialize_from="ShareStatus")
    stage = StringType(deserialize_from="Stage")
    launch_time = DateTimeType(deserialize_from="LaunchTime")
    last_updated = DateTimeType(deserialize_from="StageLastUpdatedDateTime")
    vpc_setting = ModelType(VpcSettings, deserialize_from="VpcSettings")
    connect_settings = ModelType(ConnectSettings, deserialize_from="ConnectSettings")
    os_version = StringType(deserialize_from="OsVersion")
    network_type = StringType(deserialize_from="NetworkType")
    owner_directory_description = ModelType(OwnerDirectoryDescription, deserialize_from="OwnerDirectoryDescription")
    def reference(self, region_code):
        return {
            "resource_id": self.id,
            "external_link": f"https://{region_code}.console.aws.amazon.com/directoryservicev2/home?region={region_code}#!/directories/{self.id}"
        }


"""
Directories Shared With me
"""
class SharedDirectory(AWSCloudService):
    owner_directory_id = StringType(deserialize_from="OwnerDirectoryId")
    owner_account_id = StringType(deserialize_from="OwnerAccountId")
    shared_method = StringType(deserialize_from="ShareMethod")
    shared_account_id = StringType(deserialize_from="SharedAccountId")
    shared_directory_id = StringType(deserialize_from="SharedDirectoryId")
    shared_state = StringType(deserialize_from="ShareStatus")
    data_shared = DateTimeType(deserialize_from="CreatedDateTime")
    owner_directory_status = StringType(deserialize_from="OwnerDirectoryStatus")
    vpc_setting = ModelType(VpcSettings, deserialize_from="VpcSettings")
    owner_directory_name = StringType(deserialize_from="OwnerDirectoryName")
    directory_type = StringType(deserialize_from="DirectoryType")

    def reference(self, region_code):
        return {
            "resource_id": self.shared_directory_id,
            "external_link": f"https://{region_code}.console.aws.amazon.com/directoryservicev2/home?region={region_code}#!/directories-shared-with-me/{self.shared_directory_id}"
        }