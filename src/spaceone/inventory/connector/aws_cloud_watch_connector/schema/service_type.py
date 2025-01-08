from spaceone.inventory.conf.cloud_service_conf import ASSET_URL
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResponse, CloudServiceTypeResource, \
    CloudServiceTypeMeta

"""
ALARMS
"""
cst_alarms = CloudServiceTypeResource()
cst_alarms.name = "Alarms"
cst_alarms.provider = "aws"
cst_alarms.group = "CloudWatch"
cst_alarms.labels = ["Monitoring"]
cst_alarms.service_code = "AWSCloudWatch"
cst_alarms.tags = {
    "spaceone:icon": f"{ASSET_URL}/Cloud-Watch.svg",
}

cst_alarms._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("State", "data.state"),
        TextDyField.data_source("Last State Update", "data.last_state_update"),
        TextDyField.data_source("Conditions", "data.conditions"),
        ListDyField.data_source("Actions", "data.actions"),
    ],
    search=[
        SearchField.set(name="Alarm ARN", key="data.alarm_arn"),
        SearchField.set(name="Alarm Name", key="data.alarm_name"),
        SearchField.set(name="State", key="data.state"),
        SearchField.set(name="Actions", key="data.actions"),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_alarms}),
]
