import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class TopicKMS(Model):
    kms_id = StringType(default="")
    description = StringType(default="")
    arn = StringType(default="")
    account_id = StringType(default="")
    encryption = StringType(default="")
    alias = StringType(default="")


class Subscription(Model):
    subscription_arn = StringType(deserialize_from="SubscriptionArn")
    owner = StringType(deserialize_from="Owner")
    protocol = StringType(deserialize_from="Protocol")
    endpoint = StringType(deserialize_from="Endpoint")
    topic_arn = StringType(deserialize_from="TopicArn")


class Topic(Model):
    name = StringType(default="")
    display_name = StringType(deserialize_from="DisplayName")
    effective_delivery_policy = StringType(deserialize_from="EffectiveDeliveryPolicy")
    owner = StringType(deserialize_from="Owner")
    policy = StringType(deserialize_from="Policy")
    kms = ModelType(TopicKMS)
    subscription_confirmed = IntType(deserialize_from="SubscriptionsConfirmed")
    subscription_deleted = IntType(deserialize_from="SubscriptionsDeleted")
    subscriptions_pending = IntType(deserialize_from="SubscriptionsPending")
    topic_arn = StringType(deserialize_from="TopicArn")
    subscriptions = ListType(ModelType(Subscription))
    tags = ListType(ModelType(Tags), default=[])
    region_name = StringType(default="")
    account_id = StringType(default="")
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.topic_arn,
            "external_link": f"https://console.aws.amazon.com/sns/v3/home?region={region_code}#/topic/{self.topic_arn}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/SNS",
            "dimensions": [CloudWatchDimensionModel({'Name': 'TopicName', 'Value': self.name})],
            "region_name": region_code
        }
