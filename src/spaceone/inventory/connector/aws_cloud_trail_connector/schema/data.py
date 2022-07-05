import logging
from schematics import Model
from schematics.types import ModelType, StringType, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


'''
INSIGHT SELECTOR
'''
class InsightSelector(Model):
    insight_type = StringType(deserialize_from="InsightType", serialize_when_none=False)


'''
EVENT SELECTOR
'''
class EventSelectorDataResources(Model):
    type = StringType(deserialize_from="Type", serialize_when_none=False)
    values = ListType(StringType, deserialize_from="Values", serialize_when_none=False)


class EventSelector(Model):
    read_write_type = StringType(deserialize_from="ReadWriteType", serialize_when_none=False,
                                 choices=("ReadOnly", "WriteOnly", "All"), )
    include_management_events = BooleanType(deserialize_from="IncludeManagementEvents",
                                            serialize_when_none=False)
    data_resources = ListType(ModelType(EventSelectorDataResources), deserialize_from="DataResources",
                              serialize_when_none=False)
    exclude_management_event_sources = ListType(StringType, deserialize_from="ExcludeManagementEventSources",
                                                serialize_when_none=False)


'''
TRAIL
'''
class Trail(AWSCloudService):
    name = StringType(deserialize_from="Name", serialize_when_none=False)
    s3_bucket_name = StringType(deserialize_from="S3BucketName", serialize_when_none=False)
    s3_key_prefix = StringType(deserialize_from="S3KeyPrefix", serialize_when_none=False)
    sns_topic_name = StringType(deserialize_from="SnsTopicName", serialize_when_none=False)
    sns_topic_arn = StringType(deserialize_from="SnsTopicARN", serialize_when_none=False)
    include_global_service_events = BooleanType(deserialize_from="IncludeGlobalServiceEvents", serialize_when_none=False)
    is_multi_region_trail = BooleanType(deserialize_from="IsMultiRegionTrail", serialize_when_none=False)
    home_region = StringType(deserialize_from="HomeRegion", serialize_when_none=False)
    trail_arn = StringType(deserialize_from="TrailARN", serialize_when_none=False)
    log_file_validation_enabled = BooleanType(deserialize_from="LogFileValidationEnabled", serialize_when_none=False)
    cloud_watch_logs_log_group_arn = StringType(deserialize_from="CloudWatchLogsLogGroupArn", serialize_when_none=False)
    cloud_watch_logs_role_arn = StringType(deserialize_from="CloudWatchLogsRoleArn", serialize_when_none=False)
    kms_key_id = StringType(deserialize_from="KmsKeyId", serialize_when_none=False)
    has_custom_event_selectors = BooleanType(deserialize_from="HasCustomEventSelectors", serialize_when_none=False)
    has_insight_selectors = BooleanType(deserialize_from="HasInsightSelectors", serialize_when_none=False)
    is_organization_trail = BooleanType(deserialize_from="IsOrganizationTrail", serialize_when_none=False)
    event_selectors = ListType(ModelType(EventSelector), serialize_when_none=False)
    insight_selectors = ModelType(InsightSelector, serialize_when_none=False)

    def reference(self, region_name=None):
        return {
            "resource_id": self.trail_arn,
            "external_link": f"https://console.aws.amazon.com/cloudtrail/home?region={self.home_region}#/configuration/{self.trail_arn.replace('/', '@')}"
        }
