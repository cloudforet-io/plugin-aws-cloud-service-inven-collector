import logging

from schematics import Model
from schematics.types import IntType, ModelType, StringType, BooleanType, serializable
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


class RedrivePolicy(Model):
    dead_letter_target_arn = StringType(deserialize_from="deadLetterTargetArn")
    max_receive_count = StringType(deserialize_from="maxReceiveCount")


class QueData(Model):
    class Option:
        serialize_when_none = False

    url = StringType()
    arn = StringType(deserialize_from="QueueArn")
    approximate_number_of_messages = IntType(deserialize_from="ApproximateNumberOfMessages")
    approximate_number_of_messages_delayed = IntType(deserialize_from="ApproximateNumberOfMessagesDelayed")
    approximate_number_of_messages_not_visible = IntType(deserialize_from="ApproximateNumberOfMessagesNotVisible")
    created_timestamp = StringType(deserialize_from='CreatedTimestamp')
    delay_seconds = IntType(deserialize_from="DelaySeconds")
    last_modified_timestamp = StringType(deserialize_from='LastModifiedTimestamp')
    maximum_message_size = IntType(deserialize_from="MaximumMessageSize")
    message_retention_period = IntType(deserialize_from="MessageRetentionPeriod")
    receive_message_wait_time_seconds = IntType(deserialize_from="ReceiveMessageWaitTimeSeconds")
    visibility_timeout = IntType(deserialize_from="VisibilityTimeout")
    redrive_policy = ModelType(RedrivePolicy, deserialize_from="RedrivePolicy")
    fifo_queue = StringType(deserialize_from="FifoQueue")
    content_based_duplication = StringType(deserialize_from="ContentBasedDeduplication")
    kms_master_key_id = StringType(deserialize_from="KmsMasterKeyId")
    kms_data_key_reuse_period_seconds = StringType(deserialize_from="KmsDataKeyReusePeriodSeconds")
    sqs_managed_sse_enabled = BooleanType(deserialize_from="SqsManagedSseEnabled")
    account_id = StringType()
    policy = StringType(deserialize_from="Policy")
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    @serializable
    def name(self):
        return self.arn.split(':')[-1]

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://{region_code}.console.aws.amazon.com/sqs/home?{region_code}#queue-browser:selected={self.url};prefix={self.name}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/SQS",
            "dimensions": [CloudWatchDimensionModel({"Name": "QueueName", "Value": self.name})],
            "region_name": region_code
        }
