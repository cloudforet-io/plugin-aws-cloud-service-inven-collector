import logging

from schematics import Model
from schematics.types import StringType, ModelType, ListType

from spaceone.inventory.libs.schema.dynamic_field import DateTimeDyField
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)

"""
Alarms
"""

class Action(Model):
    type = StringType( deserialize_from="type")
    description = StringType(deserialize_from="description")
    config = StringType(deserialize_from="config")


class History(Model):
    date = DateTimeDyField(deserialize_from="date")
    type = StringType(choices=("ConfigurationUpdate","StateUpdate","Action"), deserialize_from="type")
    description = StringType(deserialize_from="description")


class Alarms(AWSCloudService):
    alarm_arn = StringType(deserialize_from="AlarmArn")
    name = StringType(deserialize_from="AlarmName")
    state_value = StringType(choices=("OK","ALARM","INSUFFICIENT_DATA"), deserialize_from="StateValue")
    state_updated_timestamp = DateTimeDyField(deserialize_from="StateUpdatedTimestamp")
    actions_enabled = StringType(deserialize_from="actions_enabled")
    conditions = StringType(deserialize_from="conditions")
    actions = ListType(ModelType(Action, deserialize_from="action"), deserialize_from="actions")
    history = ListType(ModelType(History, deserialize_from="history"), deserialize_from="history")

    def reference(self, region_code):
        return {
            "resource_id": self.alarm_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Alarm:search={self.alarm_arn};sort=alarmName",
        }
