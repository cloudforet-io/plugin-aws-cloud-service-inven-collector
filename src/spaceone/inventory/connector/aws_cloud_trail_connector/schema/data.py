import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


'''
INSIGHT SELECTOR
'''
class InsightSelector(Model):
    insight_type = StringType(deserialize_from="InsightType")


'''
EVENT SELECTOR
'''
class EventSelectorDataResources(Model):
    type = StringType(deserialize_from="Type")
    values = ListType(StringType, deserialize_from="Values")


class EventSelector(Model):
    read_write_type = StringType(deserialize_from="ReadWriteType", choices=("ReadOnly", "WriteOnly", "All"))
    include_management_events = BooleanType(deserialize_from="IncludeManagementEvents")
    data_resources = ListType(ModelType(EventSelectorDataResources), deserialize_from="DataResources")
    exclude_management_event_sources = ListType(StringType, deserialize_from="ExcludeManagementEventSources")


'''
TRAIL
'''
class CloudTrailTags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class Trail(Model):
    name = StringType(deserialize_from="Name")
    s3_bucket_name = StringType(deserialize_from="S3BucketName")
    s3_key_prefix = StringType(deserialize_from="S3KeyPrefix")
    sns_topic_name = StringType(deserialize_from="SnsTopicName")
    sns_topic_arn = StringType(deserialize_from="SnsTopicARN")
    include_global_service_events = BooleanType(deserialize_from="IncludeGlobalServiceEvents")
    is_multi_region_trail = BooleanType(deserialize_from="IsMultiRegionTrail")
    home_region = StringType(deserialize_from="HomeRegion")
    trail_arn = StringType(deserialize_from="TrailARN")
    log_file_validation_enabled = BooleanType(deserialize_from="LogFileValidationEnabled")
    cloud_watch_logs_log_group_arn = StringType(deserialize_from="CloudWatchLogsLogGroupArn")
    cloud_watch_logs_role_arn = StringType(deserialize_from="CloudWatchLogsRoleArn")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    has_custom_event_selectors = BooleanType(deserialize_from="HasCustomEventSelectors")
    has_insight_selectors = BooleanType(deserialize_from="HasInsightSelectors")
    is_organization_trail = BooleanType(deserialize_from="IsOrganizationTrail")
    event_selectors = ListType(ModelType(EventSelector))
    insight_selectors = ModelType(InsightSelector)
    tags = ListType(ModelType(CloudTrailTags))
    account_id = StringType(default="")

    def reference(self, region_name=None):
        return {
            "resource_id": self.trail_arn,
            "external_link": f"https://console.aws.amazon.com/cloudtrail/home?region={self.home_region}#/configuration/{self.trail_arn.replace('/', '@')}"
        }
