import logging

from schematics import Model
from schematics.types import StringType, DateType, ModelType, ListType

from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)

"""
Alarms
"""

class Action(Model):
    type = StringType(deserialize_from="type")
    description = StringType(deserialize_from="description")
    config = StringType(deserialize_from="config")


class Alarms(AWSCloudService):
    alarm_arn = StringType(deserialize_from="AlarmArn")
    name = StringType(deserialize_from="AlarmName")
    state_value = StringType(choices=("OK","ALARM","INSUFFICIENT_DATA"), deserialize_from="StateValue")
    state_updated_timestamp = DateType(deserialize_from="StateUpdatedTimestamp")
    actions_enabled = StringType(deserialize_from="actions_enabled")
    actions = ListType(ModelType(Action, deserialize_from="action"), deserialize_from="actions")
    conditions = StringType(deserialize_from="conditions")

    def reference(self, region_code):
        return {
            "resource_id": self.alarm_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Alarm:search={self.alarm_arn};sort=alarmName",
        }
