import logging

from schematics import Model
from schematics.types import StringType, DateType, ModelType, BooleanType, IntType, FloatType

from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)

"""
Alarms
"""

class Alarms(AWSCloudService):
    alarm_arn = StringType(deserialize_from="AlarmArn")
    name = StringType(deserialize_from="AlarmName")
    state_value = StringType(choices=("OK","ALARM","INSUFFICIENT_DATA"), deserialize_from="StateValue")
    state_updated_timestamp = DateType(deserialize_from="StateUpdatedTimestamp")
    actions_enabled = BooleanType(deserialize_from="ActionsEnabled")
    conditions = StringType(deserialize_from="conditions")

    def reference(self, region_code):
        return {
            "resource_id": self.alarm_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#Alarm:search={self.alarm_arn};sort=alarmName",
        }
