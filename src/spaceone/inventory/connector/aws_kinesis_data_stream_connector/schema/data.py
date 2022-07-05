import logging

from schematics import Model
from schematics.types import (
    ModelType,
    StringType,
    IntType,
    DateTimeType,
    ListType,
    BooleanType,
)
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


# list_tags_for_stream
class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")
    has_more_tags = BooleanType(
        deserialize_from="HasMoreTags", serialize_when_none=False
    )


# list_stream_consumers
class Consumers(Model):
    consumers_num = IntType()
    consumer_name = StringType(deserialize_from="ConsumerName")
    consumer_arn = StringType(deserialize_from="ConsumerARN")
    consumer_status = StringType(
        deserialize_from="ConsumerStatus", choices=("CREATING", "DELETING", "ACTIVE")
    )
    consumer_status_display = StringType(choices=("Creating", "Deleting", "Active"))
    consumer_creation_timestamp = DateTimeType(
        deserialize_from="ConsumerCreationTimestamp"
    )


# describe_stream
class HashKeyRange(Model):
    starting_hash_key = StringType(deserialize_from="StartingHashKey")
    ending_hash_key = StringType(deserialize_from="EndingHashKey")


class SequenceNumberRange(Model):
    starting_sequence_number = StringType(deserialize_from="StartingSequenceNumber")
    ending_sequence_number = StringType(deserialize_from="EndingSequenceNumber")


class Shards(Model):
    shard_id = StringType(deserialize_from="ShardId")
    parent_shard_id = StringType(deserialize_from="ParentShardId")
    adjacent_parent_shard_id = StringType(deserialize_from="AdjacentParentShardId")
    hash_key_range = ModelType(HashKeyRange, deserialize_from="HashKeyRange")
    sequence_number_range = ModelType(
        SequenceNumberRange, deserialize_from="SequenceNumberRange"
    )


class EnhancedMonitoring(Model):
    shard_level_metrics = ListType(
        StringType(
            choices=(
                "IncomingBytes",
                "IncomingRecords",
                "OutgoingBytes",
                "OutgoingRecords",
                "WriteProvisionedThroughputExceeded",
                "ReadProvisionedThroughputExceeded",
                "IteratorAgeMilliseconds",
                "ALL",
            )
        ),
        deserialize_from="ShardLevelMetrics",
    )


class ConsumersVO(Model):
    num_of_consumers = IntType()
    consumers = ListType(ModelType(Consumers), default=[])


class StreamDescription(AWSCloudService):
    stream_name = StringType(deserialize_from="StreamName")
    stream_arn = StringType(deserialize_from="StreamARN")
    stream_status = StringType(
        deserialize_from="StreamStatus",
        choices=("CREATING", "DELETING", "ACTIVE", "UPDATING"),
    )
    stream_status_display = StringType(
        choices=("Creating", "Deleting", "Active", "Updating")
    )
    shards = ListType(ModelType(Shards), deserialize_from="Shards")
    open_shards_num = IntType()
    closed_shards_num = IntType()
    has_more_shards = BooleanType(deserialize_from="HasMoreShards")
    retention_period_hours = IntType(deserialize_from="RetentionPeriodHours")
    retention_period_days = IntType()
    retention_period_display = StringType()
    retention_period_display_hours = StringType()
    stream_creation_timestamp = DateTimeType(deserialize_from="StreamCreationTimestamp")
    enhanced_monitoring = ListType(
        ModelType(EnhancedMonitoring), deserialize_from="EnhancedMonitoring"
    )
    shard_level_metrics_display = ListType(StringType())
    encryption_type = StringType(
        deserialize_from="EncryptionType", choices=("NONE", "KMS")
    )
    encryption_display = StringType(choices=("Disabled", "Enabled"))
    key_id = StringType(deserialize_from="KeyId")
    consumers_vo = ModelType(ConsumersVO)
    tags = ListType(ModelType(Tags), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.stream_arn,
            "external_link": f"https://console.aws.amazon.com/kinesis/home?region={region_code}#/streams/details/{self.stream_name}",
        }
