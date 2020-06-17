import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

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
    subscription_confirmed = StringType(deserialize_from="SubscriptionsConfirmed")
    subscription_deleted = BooleanType(deserialize_from="SubscriptionsDeleted")
    subscriptions_pending = BooleanType(deserialize_from="SubscriptionsPending")
    topic_arn = StringType(deserialize_from="TopicArn")
    subscriptions = ListType(ModelType(Subscription))
    tags = ListType(ModelType(Tags))
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.topic_arn,
            "external_link": f"https://console.aws.amazon.com/sns/v3/home?region={self.region_name}#/topic/{self.topic_arn}"
        }

    @serializable
    def cloudwatch(self):
        return {
            "namespace": "AWS/SNS",
            "dimensions": [
                {
                    "Name": "TopicName",
                    "Value": self.name
                }
            ],
            "region_name": self.region_name
        }
