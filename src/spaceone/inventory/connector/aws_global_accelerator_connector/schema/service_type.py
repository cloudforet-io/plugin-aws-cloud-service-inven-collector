import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField, \
    SearchField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResponse, CloudServiceTypeResource, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
GLOBAL ACCELERATOR
"""
total_count_conf = os.path.join(current_dir, "widget/total_count.yaml")
count_by_region_conf = os.path.join(current_dir, "widget/count_by_region.yaml")
count_by_account_conf = os.path.join(current_dir, "widget/count_by_account.yaml")

cst_ga = CloudServiceTypeResource()
cst_ga.name = "Accelerator"
cst_ga.provider = "aws"
cst_ga.group = "GlobalAccelerator"
cst_ga.labels = ["Networking"]
cst_ga.is_primary = True
cst_ga.is_major = True
cst_ga.service_code = "AWSGlobalAccelerator"

cst_ga._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source("Type", "data.type",
                                default_badge={"indigo.500": ["Standard"], "coral.600": ["Customised routing"]}),
        TextDyField.data_source("IP Address Type", "data.ip_address_type",options={
            "is_optional": True
        }),
        ListDyField.data_source("IPv4",
                                "data.ipv4_addresses",
                                options={"delimiter": "<br>"}),
        ListDyField.data_source("IPv6",
                                "data.ipv6_addresses",
                                options={"delimiter": "<br>"}),
        EnumDyField.data_source("Enabled", "data.enabled", default_state={
            "safe": ["True"],
            "alert": ["False"]
        }),
        TextDyField.data_source("DNS Name", "data.dns_name"),
        TextDyField.data_source("Dual Stack DNS Name", "data.dual_stack_dns_name"),
        EnumDyField.data_source("Status", "data.status", default_state={
            "safe": ["DEPLOYED"],
            "warning": ["IN_PROGRESS"]
        }),
        DateTimeDyField.data_source("Created", "data.created_at"),
        DateTimeDyField.data_source("Edited", "data.edited_at"),
    ],
    search=[
        SearchField.set(name="ARN", key="data.arn"),
        SearchField.set(name="Name", key="data.name"),
        SearchField.set(name="Type", key="data.type"),
        SearchField.set(name="Enabled", key="data.enabled",
                        enums={
                            "TRUE":{"label":"TRUE","icon":{"color":"green.500"}},
                            "FALSE":{"label":"FALSE","icon":{"color":"red.500"}}
                        }),
        SearchField.set(name="Status", key="data.status",
                        enums={
                        "DEPLOYED":{"label":"DEPLOYED","icon":{"color":"green.500"}},
                        "IN_PROGRESS":{"label":"IN_PROGRESS","icon":{"color":"yellow.500"}},
                        })
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
    ]
)

"""
CROSS - ACCOUNT ATTACHMENTS 
"""
cst_ca = CloudServiceTypeResource()
cst_ca.name = "Cross-account attachments"
cst_ca.provider = "aws"
cst_ca.group = "GlobalAccelerator"
cst_ca.labels = ["Networking"]
cst_ca.service_code = "AWSGlobalAccelerator"

cst_ca._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        ListDyField.data_source("Principals", "data.principals"),
        ListDyField.data_source(
            "Resources",
            "data.resources",
            options={"delimiter": "<br>", "sub_key": "endpoint_id"}
        ),
        DateTimeDyField.data_source("Created", "data.created_at"),
        DateTimeDyField.data_source("Last modified", "data.modified_time"),
    ],
    search=[
        SearchField.set(name="ID", key="data.arn"),
        SearchField.set(name="Name", key="data.name"),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_ga}),
    CloudServiceTypeResponse({"resource": cst_ca}),
]