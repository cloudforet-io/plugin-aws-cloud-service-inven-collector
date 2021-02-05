from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_kinesis_data_streams_connector.schema.data import (
    StreamDescription,
)
from spaceone.inventory.libs.schema.dynamic_field import (
    TextDyField,
    ListDyField,
    EnumDyField,
    DateTimeDyField,
)
from spaceone.inventory.libs.schema.dynamic_layout import (
    ItemDynamicLayout,
    TableDynamicLayout,
    ListDynamicLayout,
)
from spaceone.inventory.libs.schema.resource import (
    CloudServiceResource,
    CloudServiceResponse,
    CloudServiceMeta,
)

"""
kinesis
"""
# TAB - Detail
kds_meta_detail = ItemDynamicLayout.set_fields(
    "Stream Details",
    fields=[
        TextDyField.data_source("Status", "data.stream_status_display"),
        TextDyField.data_source("ARN", "data.stream_arn"),
        TextDyField.data_source(
            "Data retention period", "data.retention_period_display"
        ),
    ],
)

# TAB - Configuration
kds_meta_configuration = ItemDynamicLayout.set_fields(
    "Configuration",
    fields=[
        TextDyField.data_source("Number of open shards", "data.open_shards_num"),
        TextDyField.data_source("Number of closed shards", "data.closed_shards_num"),
        TextDyField.data_source("Server-side encryption", "data.encryption_display"),
        TextDyField.data_source(
            "Data retention period", "data.retention_period_display_hours"
        ),
        ListDyField.data_source(
            "Enhanced (shard-level) metrics",
            "data.shard_level_metrics_display",
            default_badge={"delimiter": "<br>"},
        )
    ]
)

# TAB - Enhanced fan-out
kds_meta_consumers_using_enhanced_fan_out = TableDynamicLayout.set_fields(
    "Consumers using enhanced fan-out",
    "data.consumers_vo.consumers",
    fields=[
        TextDyField.data_source("Consumer name", "consumer_name"),
        EnumDyField.data_source(
            "Registration status",
            "consumer_status_display",
            default_state={"safe": ["Active"], "warning": ["Creating", "Deleting"]},
        ),
        DateTimeDyField.data_source("Registration date", "consumer_creation_timestamp"),
    ],
)

kds_meta_enhanced_fan_out = ListDynamicLayout.set_layouts(
    "Enhanced fan-out", layouts=[kds_meta_consumers_using_enhanced_fan_out]
)

# TAB - Tags
kds_meta_tags = TableDynamicLayout.set_fields(
    "Tags",
    "data.tags",
    fields=[
        TextDyField.data_source("Key", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)

# Overall
kds_meta = CloudServiceMeta.set_layouts(
    [kds_meta_detail, kds_meta_configuration, kds_meta_enhanced_fan_out, kds_meta_tags]
)


class KDSResource(CloudServiceResource):  # service type - group
    cloud_service_group = StringType(default="KinesisDataStream")


class StreamResource(KDSResource):  # service type - name
    cloud_service_type = StringType(default="DataStream")
    data = ModelType(StreamDescription)
    _metadata = ModelType(
        CloudServiceMeta, default=kds_meta, serialized_name="metadata"
    )


class KDSResponse(CloudServiceResponse):
    resource = PolyModelType(StreamResource)
