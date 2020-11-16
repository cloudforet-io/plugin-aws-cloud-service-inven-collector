import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


class Tag(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")

'''
CONTRIBUTOR INSIGHT
'''
class FailureException(Model):
    exception_name = StringType(deserialize_from="ExceptionName")
    exception_description = StringType(deserialize_from="ExceptionDescription")


class ContributorInsight(Model):
    table_name = StringType(deserialize_from="TableName")
    index_name = StringType(deserialize_from="IndexName")
    contributor_insights_rule_list = ListType(StringType, deserialize_from="ContributorInsightsRuleList")
    contributor_insights_status = StringType(deserialize_from="ContributorInsightsStatus",
                                             choices=("ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"))
    last_update_date_time = DateTimeType(deserialize_from="LastUpdateDateTime")
    failure_exception = ModelType(FailureException,deserialize_from="FailureException")


'''
CONTINUOUS BACKUP (POINT TO RECOVERY)
'''
class PointInTimeRecoveryDescription(Model):
    point_in_time_recovery_status = StringType(deserialize_from="PointInTimeRecoveryStatus",
                                               choices=("ENABLED", "DISABLED"))
    earliest_restorable_date_time = DateTimeType(deserialize_from="EarliestRestorableDateTime")
    latest_restorable_date_time = DateTimeType(deserialize_from="LatestRestorableDateTime")


class ContinuousBackup(Model):
    continuous_backups_status = StringType(deserialize_from="ContinuousBackupsStatus",
                                           choices=("ENABLED", "DISABLED"))
    point_in_time_recovery_description = ModelType(PointInTimeRecoveryDescription,
                                                   deserialize_from="PointInTimeRecoveryDescription")

'''
TIME-TO-LIVE
'''
class TimeToLive(Model):
    time_to_live_status = StringType(deserialize_from="TimeToLiveStatus", choices=("ENABLING", "DISABLING",
                                                                                   "ENABLED", "DISABLED"))
    attribute_name = StringType(deserialize_from="AttributeName")


class BillingModeSummary(Model):
    billing_mode = StringType(deserialize_from="BillingMode", default="PROVISIONED",
                              choices=("PROVISIONED", "PAY_PER_REQUEST"))
    last_update_to_pay_per_request_date_time = DateTimeType(deserialize_from="LastUpdateToPayPerRequestDateTime")


class Projection(Model):
    projection_type = StringType(deserialize_from="ProjectionType", choices=("ALL", "KEYS_ONLY", "INCLUDE"))
    non_key_attributes = ListType(StringType, deserialize_from="NonKeyAttributes")


class ProvisionedThroughput(Model):
    last_increase_date_time = DateTimeType(deserialize_from="LastIncreaseDateTime")
    last_decrease_date_time = DateTimeType(deserialize_from="LastDecreaseDateTime")
    number_of_decreases_today = IntType(deserialize_from="NumberOfDecreasesToday")
    read_capacity_units = IntType(deserialize_from="ReadCapacityUnits")
    write_capacity_units = IntType(deserialize_from="WriteCapacityUnits")


class StreamSpecification(Model):
    stream_enabled = BooleanType(deserialize_from="StreamEnabled")
    stream_view_type = StringType(deserialize_from="StreamViewType", choices=("NEW_IMAGE",
                                                                              "OLD_IMAGE",
                                                                              "NEW_AND_OLD_IMAGES",
                                                                              "KEYS_ONLY"))


class ProvisionedThroughputOverride(Model):
    read_capacity_units = IntType(deserialize_from="ReadCapacityUnits")


class RestoreSummary(Model):
    source_backup_arn = StringType(deserialize_from="SourceBackupArn")
    source_table_arn = StringType(deserialize_from="SourceTableArn")
    restore_date_time = DateTimeType(deserialize_from="RestoreDateTime")
    restore_in_progress = BooleanType(deserialize_from="RestoreInProgress")


class SSEDescription(Model):
    status = StringType(deserialize_from="Status", choices=("ENABLING","ENABLED","DISABLING","DISABLED","UPDATING"))
    sse_type = StringType(deserialize_from="SSEType", choices=("AES256","KMS"))
    kms_master_key_arn = StringType(deserialize_from="KMSMasterKeyArn")
    inaccessible_encryption_date_time = DateTimeType(deserialize_from="InaccessibleEncryptionDateTime")


class ArchivalSummary(Model):
    archival_date_time = DateTimeType(deserialize_from="ArchivalDateTime")
    archival_reason = StringType(deserialize_from="ArchivalReason")
    archival_backup_arn = StringType(deserialize_from="ArchivalBackupArn")


class TableAttributeDefinitions(Model):
    attribute_name = StringType(deserialize_from="AttributeName")
    attribute_type = StringType(deserialize_from="AttributeType", choices=("S","N","B"))


class TableKeySchema(Model):
    attribute_name = StringType(deserialize_from="AttributeName")
    key_type = StringType(deserialize_from="KeyType", choices=("HASH","RANGE"))


class TableLocalSecondaryIndexes(Model):
    index_name = StringType(deserialize_from="IndexName")
    key_schema = ListType(ModelType(TableKeySchema), deserialize_from="KeySchema")
    projection = ModelType(Projection, deserialize_from="Projection")
    index_size_bytes = IntType(deserialize_from="IndexSizeBytes")
    item_count = IntType(deserialize_from="ItemCount")
    index_arn = StringType(deserialize_from="IndexArn")


class TableGlobalSecondaryIndexes(Model):
    index_name = StringType(deserialize_from="IndexName")
    key_schema = ListType(ModelType(TableKeySchema), deserialize_from="KeySchema")
    projection = ModelType(Projection, deserialize_from="Projection")
    index_status = StringType(deserialize_from="IndexStatus", choices=("CREATING", "UPDATING", "DELETING", "ACTIVE"))
    backfilling = BooleanType(deserialize_from="Backfilling")
    provisioned_throughput = ModelType(ProvisionedThroughput, deserialize_from="ProvisionedThroughput")
    index_size_bytes = IntType(deserialize_from="IndexSizeBytes")
    item_count = IntType(deserialize_from="ItemCount")
    index_arn = StringType(deserialize_from="IndexArn")


class GlobalSecondaryIndexes(Model):
    index_name = StringType(deserialize_from="IndexName")
    provisioned_throughput_override = ModelType(ProvisionedThroughputOverride,
                                                deserialize_from="ProvisionedThroughputOverride")


class TableReplicas(Model):
    region_name = StringType(deserialize_from="RegionName")
    replica_status = StringType(deserialize_from="ReplicaStatus", choices=("CREATING",
                                                                           "CREATION_FAILED",
                                                                           "UPDATING",
                                                                           "DELETING",
                                                                           "ACTIVE"))
    replica_status_description = StringType(deserialize_from="ReplicaStatusDescription")
    replica_status_percent_progress = StringType(deserialize_from="ReplicaStatusPercentProgress")
    kms_master_key_id = StringType(deserialize_from="KMSMasterKeyId")
    provisioned_throughput_override = ModelType(ProvisionedThroughputOverride,
                                                deserialize_from="ProvisionedThroughputOverride")
    global_secondary_indexes = ListType(ModelType(GlobalSecondaryIndexes), deserialize_from="GlobalSecondaryIndexes")


class Table(Model):
    attribute_definitions = ListType(ModelType(TableAttributeDefinitions), deserialize_from="AttributeDefinitions")
    table_name = StringType(deserialize_from="TableName")
    key_schema = ListType(ModelType(TableKeySchema), deserialize_from="KeySchema")
    table_status = StringType(deserialize_from="TableStatus", choices=("CREATING",
                                                                       "UPDATING",
                                                                       "DELETING",
                                                                       "ACTIVE",
                                                                       "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
                                                                       "ARCHIVING",
                                                                       "ARCHIVED"))
    creation_date_time = DateTimeType(deserialize_from="CreationDateTime")
    provisioned_throughput = ModelType(ProvisionedThroughput, deserialize_from="ProvisionedThroughput")
    table_size_bytes = IntType(deserialize_from="TableSizeBytes")
    item_count = IntType(deserialize_from="ItemCount")
    table_arn = StringType(deserialize_from="TableArn")
    table_id = StringType(deserialize_from="TableId")
    billing_mode_summary = ModelType(BillingModeSummary, deserialize_from="BillingModeSummary")
    local_secondary_indexes = ListType(ModelType(TableLocalSecondaryIndexes),
                                       deserialize_from="LocalSecondaryIndexes")
    global_secondary_indexes = ListType(ModelType(TableGlobalSecondaryIndexes),
                                        deserialize_from="GlobalSecondaryIndexes")
    stream_specification = ModelType(StreamSpecification, deserialize_from="StreamSpecification")
    latest_stream_label = StringType(deserialize_from="LatestStreamLabel")
    latest_stream_arn = StringType(deserialize_from="LatestStreamArn")
    global_table_version = StringType(deserialize_from="GlobalTableVersion")
    replicas = ListType(ModelType(TableReplicas), deserialize_from="Replicas")
    restore_summary = ModelType(RestoreSummary, deserialize_from="RestoreSummary")
    sse_description = ModelType(SSEDescription, deserialize_from="SSEDescription")
    archival_summary = ModelType(ArchivalSummary, deserialize_from="ArchivalSummary")
    partition_key_display = StringType(default="")
    sort_key_display = StringType(default="")
    total_read_capacity = IntType(default=0)
    total_write_capacity = IntType(default=0)
    auto_scaling_policies = ListType(StringType, choices=("READ", "WRITE"))
    encryption_type = StringType(default="")
    index_count = IntType(default=0)
    account_id = StringType(default="")
    time_to_live = ModelType(TimeToLive)
    continuous_backup = ModelType(ContinuousBackup)
    contributor_insight = ModelType(ContributorInsight)
    tags = ListType(ModelType(Tag))
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.table_arn,
            "external_link": f"https://console.aws.amazon.com/dynamodb/home?region={region_code}#tables:selected={self.table_name};tab=overview"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/DynamoDB",
            "dimensions": [CloudWatchDimensionModel({'Name': 'TableName', 'Value': self.table_name})],
            "region_name": region_code
        }
