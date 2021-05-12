import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, FloatType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


'''
SNAPSHOT
'''
class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class Snapshot(Model):
    name = StringType(default="")
    arn = StringType(default="")
    data_encryption_key_id = StringType(deserialize_from="DataEncryptionKeyId")
    description = StringType(deserialize_from="Description")
    encrypted = BooleanType(deserialize_from="Encrypted")
    kms_key_id = StringType(default="")
    kms_key_arn = StringType(deserialize_from="KmsKeyId")
    owner_id = StringType(deserialize_from="OwnerId")
    account_id = StringType(default="")
    progress = StringType(deserialize_from="Progress")
    snapshot_id = StringType(deserialize_from="SnapshotId")
    start_time = DateTimeType(deserialize_from="StartTime")
    state = StringType(deserialize_from="State", choices=("pending", "completed", "error"))
    state_message = StringType(deserialize_from="StateMessage")
    volume_id = StringType(deserialize_from="VolumeId")
    volume_size = IntType(deserialize_from="VolumeSize")
    owner_alias = StringType(deserialize_from="OwnerAlias")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Snapshots:visibility=owned-by-me;snapshotId={self.snapshot_id};sort=snapshotId"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/EBS",
            "dimensions": [CloudWatchDimensionModel({'Name': 'SnapshotId', 'Value': self.snapshot_id})],
            "region_name": region_code
        }


'''
ATTRIBUTE
'''
class AutoEnableIO(Model):
    value = BooleanType(deserialize_from="Value")


class AttributeProductCodes(Model):
    product_code_id = StringType(deserialize_from="ProductCodeId")
    product_code_type = StringType(deserialize_from="ProductCodeType", choices=("devpay", "marketplace"))


class Attribute(Model):
    auto_enable_io = ModelType(AutoEnableIO,deserialize_from="AutoEnableIO")
    product_codes = ListType(ModelType(AttributeProductCodes), deserialize_from="ProductCodes")
    volume_id = StringType(deserialize_from="VolumeId")


'''
VOLUME
'''
class VolumeAttachments(Model):
    attach_time = DateTimeType(deserialize_from="AttachTime")
    device = StringType(deserialize_from="Device")
    instance_id = StringType(deserialize_from="InstanceId")
    state = StringType(deserialize_from="State", choices=("attaching", "attached", "detaching", "detached", "busy"))
    volume_id = StringType(deserialize_from="VolumeId")
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination")


class Volume(Model):
    arn = StringType(default="")
    name = StringType(default="")
    account_id = StringType(default="")
    attachments = ListType(ModelType(VolumeAttachments), deserialize_from="Attachments")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    create_time = DateTimeType(deserialize_from="CreateTime")
    encrypted = BooleanType(deserialize_from="Encrypted")
    kms_key_id = StringType(default="")
    kms_key_arn = StringType(deserialize_from="KmsKeyId")
    outpost_arn = StringType(deserialize_from="OutpostArn")
    size = FloatType(default=0)
    size_gb = IntType(deserialize_from="Size")
    snapshot_id = StringType(deserialize_from="SnapshotId")
    state = StringType(deserialize_from="State", choices=("creating", "available", "in-use",
                                                          "deleting", "deleted", "error"))
    volume_id = StringType(deserialize_from="VolumeId")
    iops = IntType(deserialize_from="Iops")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    volume_type = StringType(deserialize_from="VolumeType", choices=("standard", "io1", "gp2", "gp3", "sc1", "st1"))
    fast_restored = BooleanType(deserialize_from="FastRestored")
    multi_attach_enabled = BooleanType(deserialize_from="MultiAttachEnabled")
    attribute = ModelType(Attribute)
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Volumes:search={self.volume_id};sort=state"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/EBS",
            "dimensions": [CloudWatchDimensionModel({'Name': 'VolumeId', 'Value': self.volume_id})],
            "region_name": region_code
        }
