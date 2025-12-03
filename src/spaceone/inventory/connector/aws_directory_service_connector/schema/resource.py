from schematics.types import StringType, ModelType, PolyModelType

from spaceone.inventory.connector.aws_directory_service_connector.schema.data import Directory, SharedDirectory
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

"""
    Directories
"""
directory_base = ItemDynamicLayout.set_fields("Directory", fields=[
    TextDyField.data_source("Directory DNS name","data.name"),
    TextDyField.data_source("Directory ID","data.id"),
    TextDyField.data_source("Directory type", "data.type"),
    TextDyField.data_source("Size","data.size"),
    TextDyField.data_source("Edition","data.edition"),
    TextDyField.data_source("Directory DNS name","data.name"),
    TextDyField.data_source("Directory NetBIOS Name","data.short_name"),
    TextDyField.data_source("Description","data.description"),
    TextDyField.data_source("Operating system version","data.os_version"),
    TextDyField.data_source("Connected directory domain","data.name"),
    TextDyField.data_source("Connector account username","data.connect_settings.customer_user_name")
])

directory_networking = ItemDynamicLayout.set_fields("Networking", fields=[
    ListDyField.data_source("Availability zones","data.vpc_setting.availability_zones"),
    TextDyField.data_source("Network type","data.network_type"),
    ListDyField.data_source("DNS IPv4 addresses","data.dns_ip_addrs"),
    ListDyField.data_source("AD Connector IPv4 addresses","data.connect_settings.connect_ips"),
    ListDyField.data_source("DNS IPv6 addresses","data.dns_ipv6_addrs"),
    ListDyField.data_source("AD Connector IPv6 addresses","data.connect_settings.connect_ips_v6"),
    TextDyField.data_source("VPC", "data.vpc_setting.vpc_id"),
    ListDyField.data_source("Subnets","data.vpc_setting.subnet_ids"),
    EnumDyField.data_source("Status","data.stage",
                            default_state={
                                "safe": ["Created", "Active"],
                                "warning": ["Requested", "Creating", "Inoperable", "Restoring", "Deleting", "Updating"],
                                "alert": ["Impaired", "RestoreFailed", "Deleted", "Failed"]
                            }),
    DateTimeDyField.data_source("Launch time","data.launch_time"),
    DateTimeDyField.data_source("Last updated","data.last_updated")
])

directory_metadata = CloudServiceMeta.set_layouts(
    layouts=[directory_base, directory_networking]
)


"""
    Directories shared with me
"""
shared_directory_base = ItemDynamicLayout.set_fields("Shared Directory", fields=[
    TextDyField.data_source("Directory type","data.directory_type"),
    TextDyField.data_source("Directory ID","data.shared_directory_id"),
    DateTimeDyField.data_source("Launch time","data.data_shared"),
    EnumDyField.data_source("Shared state","data.shared_state",
                                    default_state={
                                        "safe": ["Shared", "Sharing"],
                                        "warning": ["PendingAcceptance", "Deleting", "Rejecting", "Rejected"],
                                        "alert": ["RejectFailed", "ShareFiled", "Deleted"]
                                    }),
])

shared_directory_owner = ItemDynamicLayout.set_fields("Owner Directory", fields=[
    TextDyField.data_source("Directory name","data.owner_directory_name"),
    TextDyField.data_source("Directory ID","data.owner_directory_id"),
    TextDyField.data_source("VPC","data.vpc_setting.vpc_id"),
    ListDyField.data_source("Subnets","data.vpc_setting.subnet_ids"),
    ListDyField.data_source("Availability Zones","data.vpc_setting.availability_zones"),
    TextDyField.data_source("DNS address","data.owner_directory_name"),
    EnumDyField.data_source("Status","data.owner_directory_status",
                            default_state={
                                "safe": ["Created", "Active"],
                                "warning": ["Requested", "Creating", "Inoperable", "Restoring", "Deleting", "Updating"],
                                "alert": ["Impaired", "RestoreFailed", "Deleted", "Failed"]
                            })
])

shared_directory_metadata = CloudServiceMeta.set_layouts(
    layouts=[shared_directory_base, shared_directory_owner]
)

class DirectoryServiceResource(CloudServiceResource):
    cloud_service_group = StringType(default="DirectoryService")

class DirectoryResource(DirectoryServiceResource):
    cloud_service_type = StringType(default="Directories")
    data = ModelType(Directory)
    _metadata = ModelType(CloudServiceMeta, default=directory_metadata, serialized_name="metadata")

class DirectoryResponse(CloudServiceResponse):
    resource = PolyModelType(DirectoryResource)

class SharedDirectoryResource(DirectoryServiceResource):
    cloud_service_type = StringType(default="Directories shared with me")
    data = ModelType(SharedDirectory)
    _metadata = ModelType(CloudServiceMeta, default=shared_directory_metadata, serialized_name="metadata")

class SharedDirectoryResponse(CloudServiceResponse):
    resource = PolyModelType(SharedDirectoryResource)