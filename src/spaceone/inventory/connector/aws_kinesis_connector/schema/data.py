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

_LOGGER = logging.getLogger(__name__)


# list_tags_for_stream
class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")
    has_more_tags = BooleanType(deserialize_from="HasMoreTags", serialize_when_none=False)


# list_stream_consumers
class Consumers(Model):
    consumer_name = StringType(deserialize_from="ConsumerName")
    consumer_arn = StringType(deserialize_from="ConsumerARN")
    consumer_status = StringType(
        deserialize_from="ConsumerStatus", choices=("CREATING", "DELETING", "ACTIVE")
    )
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
    shard_level_metrics = ListType(StringType(choices=(
        "IncomingBytes",
        "IncomingRecords",
        "OutgoingBytes",
        "OutgoingRecords",
        "WriteProvisionedThroughputExceeded",
        "ReadProvisionedThroughputExceeded",
        "IteratorAgeMilliseconds",
        "ALL"
    )), deserialize_from="ShardLevelMetrics")


class StreamDescription(Model):
    stream_name = StringType(deserialize_from="StreamName")
    stream_arn = StringType(deserialize_from="StreamARN")
    stream_status = StringType(
        deserialize_from="StreamStatus",
        choices=("CREATING", "DELETING", "ACTIVE", "UPDATING"),
    )
    shards = ListType(ModelType(Shards), deserialize_from="Shards")
    has_more_shards = BooleanType(deserialize_from="HasMoreShards")
    retention_period_hours = IntType(deserialize_from="RetentionPeriodHours")
    stream_creation_timestamp = DateTimeType(deserialize_from="StreamCreationTimestamp")
    enhanced_monitoring = ListType(
        ModelType(EnhancedMonitoring), deserialize_from="EnhancedMonitoring"
    )
    encryption_type = StringType(
        deserialize_from="EncryptionType", choices=("NONE", "KMS")
    )
    key_id = StringType(deserialize_from="KeyId")
    consumers = ListType(ModelType(Consumers), default=[])
    tags = ListType(ModelType(Tags), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.stream_arn,
            "external_link": f"https://console.aws.amazon.com/kinesis/home?region={region_code}#/streams/details/{self.stream_name}",
        }
