import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


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


class Topic(AWSCloudService):
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
    region_name = StringType(default="")

    def reference(self, region_code):
        return {
            "resource_id": self.topic_arn,
            "external_link": f"https://console.aws.amazon.com/sns/v3/home?region={region_code}#/topic/{self.topic_arn}"
        }
