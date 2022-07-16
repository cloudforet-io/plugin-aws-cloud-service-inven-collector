import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, \
    FloatType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


'''
MOUNT TARGET
'''
class MountTarget(Model):
    owner_id = StringType(deserialize_from="OwnerId")
    mount_target_id = StringType(deserialize_from="MountTargetId")
    file_system_id = StringType(deserialize_from="FileSystemId")
    subnet_id = StringType(deserialize_from="SubnetId")
    life_cycle_state = StringType(deserialize_from="LifeCycleState", choices=("creating", "available", "updating",
                                                                              "deleting", "deleted"))
    ip_address = StringType(deserialize_from="IpAddress")
    network_interface_id = StringType(deserialize_from="NetworkInterfaceId")
    availability_zone_id = StringType(deserialize_from="AvailabilityZoneId")
    availability_zone_name = StringType(deserialize_from="AvailabilityZoneName")
    security_groups = ListType(StringType())


'''
LIFECYCLE POLICY
'''
class LifecyclePolicy(Model):
    transition_to_ia = StringType(deserialize_from="TransitionToIA", choices=("AFTER_7_DAYS",
                                                                              "AFTER_14_DAYS",
                                                                              "AFTER_30_DAYS",
                                                                              "AFTER_60_DAYS",
                                                                              "AFTER_90_DAYS"))
    transition_to_ia_display = StringType(serialize_when_none=False)


'''
FILE SYSTEM
'''
class SizeInBytes(Model):
    value = IntType(deserialize_from="Value")
    timestamp = DateTimeType(deserialize_from="Timestamp")
    value_in_ia = IntType(deserialize_from="ValueInIA")
    value_in_standard = IntType(deserialize_from="ValueInStandard")


class FileSystem(AWSCloudService):
    arn = StringType()
    owner_id = StringType(deserialize_from="OwnerId")
    creation_token = StringType(deserialize_from="CreationToken")
    file_system_id = StringType(deserialize_from="FileSystemId")
    creation_time = DateTimeType(deserialize_from="CreationTime")
    life_cycle_state = StringType(deserialize_from="LifeCycleState", choices=("creating", "available", "updating",
                                                                         "deleting", "deleted"))
    name = StringType(deserialize_from="Name")
    number_of_mount_targets = IntType(deserialize_from="NumberOfMountTargets")
    size_in_bytes = ModelType(SizeInBytes, deserialize_from="SizeInBytes")
    performance_mode = StringType(deserialize_from="PerformanceMode", choices=("generalPurpose", "maxIO"))
    encrypted = BooleanType(deserialize_from="Encrypted")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    throughput_mode = StringType(deserialize_from="ThroughputMode", choices=("bursting", "provisioned"))
    provisioned_throughput_in_mibps = FloatType(deserialize_from="ProvisionedThroughputInMibps")
    life_cycle_policies = ListType(ModelType(LifecyclePolicy), default=[])
    mount_targets = ListType(ModelType(MountTarget))
    size = FloatType(default=0.0)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/efs/home?region={region_code}#/filesystems/{self.file_system_id}"
        }
