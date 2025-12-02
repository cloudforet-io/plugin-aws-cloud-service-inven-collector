from schematics.types import StringType, ModelType, PolyModelType

from spaceone.inventory.connector.aws_global_accelerator_connector.schema.data import Accelerator, \
    CrossAccountAttachments
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, ListDyField, DateTimeDyField, \
    BadgeDyField, BadgeItemDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

# Global Accelerator
accelerator_base = ItemDynamicLayout.set_fields("Accelerator", fields=[
    TextDyField.data_source("Accelerator ID", "data.arn"),
    TextDyField.data_source("Accelerator Name", "data.name"),
    EnumDyField.data_source("Type", "data.type",
                                default_badge={"indigo.500": ["Standard"], "coral.600": ["Customised routing"]}),
    EnumDyField.data_source("IP Address Type", "data.ip_address_type",
                            default_badge={"indigo.500": ["IPV4"], "coral.600": ["DUAL_STACK"]}),
    ListDyField.data_source("IPv4","data.ipv4_addresses",
                            options={"delimiter": "<br>"}),
    ListDyField.data_source("IPv6","data.ipv6_addresses",
                            options={"delimiter": "<br>"}),
    EnumDyField.data_source("Enabled","data.enabled",default_state={
        "safe":["True"],
        "alert" : ["False"]
    }),
    TextDyField.data_source("DNS Name","data.dns_name"),
    TextDyField.data_source("Dual Stack DNS Name","data.dual_stack_dns_name"),
    EnumDyField.data_source("Status","data.status", default_state={
        "safe":["DEPLOYED"],
        "warning" : ["IN_PROGRESS"]
    }),
    DateTimeDyField.data_source("Creation time", "data.created_at"),
    DateTimeDyField.data_source("Modification time", "data.edited_at"),
])

accelerator_listeners = SimpleTableDynamicLayout.set_fields(
    "Listeners",
    root_path="data.listeners",
    fields=[
        TextDyField.data_source("ID", "arn"),
        ListDyField.data_source("Interface","port_display",
                                options={"delimiter": "<br>",
                                         "item":BadgeItemDyField.set({
                                             "background_color": "indigo.500",
                                             "shape":"ROUND",
                                             "text_color": "#ffffff",
                                         })},),
        ListDyField.data_source("Endpoint groups","endpoint_region",
                                options={"delimiter": "<br>",}),
    ]
)

accelerator_endpoints = SimpleTableDynamicLayout.set_fields(
    "Endpoints",
    root_path="data.endpoints",
    fields=[
        TextDyField.data_source("ID","arn"),
        TextDyField.data_source("Endpoint groups", "region"),
        TextDyField.data_source("Traffic dial","traffic_dial"),
    ]
)


listeners_endpoints = ListDynamicLayout.set_layouts(
    "Listeners",
    layouts=[accelerator_listeners, accelerator_endpoints]
)
accelerator_meta = CloudServiceMeta.set_layouts(
    layouts=[accelerator_base, listeners_endpoints]
)

# Cross - Account Attachments
cross_account_attachments_base = ItemDynamicLayout.set_fields(
    "Cross-account attachments",
    fields=[
        TextDyField.data_source("ID", "data.arn"),
        TextDyField.data_source("Name", "data.name"),
        ListDyField.data_source("Principals","data.principals"),
        ListDyField.data_source(
            "Resources",
            "data.resources",
            options={"delimiter": "<br>", "sub_key": "endpoint_id"}
        ),
        DateTimeDyField.data_source("Creation time", "data.created_at"),
        DateTimeDyField.data_source("Modification time", "data.modified_time"),
    ]
)

cross_account_attachments_meta = CloudServiceMeta.set_layouts(
    layouts=[cross_account_attachments_base]
)
# Accelerator
class GlobalAcceleratorResource(CloudServiceResource):
    cloud_service_group = StringType(default = "GlobalAccelerator")


class AcceleratorResource(GlobalAcceleratorResource):
    cloud_service_type = StringType(default = "Accelerator")
    data = ModelType(Accelerator)
    _metadata = ModelType(CloudServiceMeta, default=accelerator_meta, serialized_name="metadata")

class AcceleratorResponse(CloudServiceResponse):
    resource = PolyModelType(AcceleratorResource)


# Cross-Account Attachments
class CrossAccountAttachmentsResource(GlobalAcceleratorResource):
    cloud_service_type = StringType(default= "Cross-account attachments")
    data = ModelType(CrossAccountAttachments)
    _metadata = ModelType(CloudServiceMeta, default=cross_account_attachments_meta, serialized_name="metadata")

class CrossAccountAttachmentsResponse(CloudServiceResponse):
    resource = PolyModelType(CrossAccountAttachmentsResource)