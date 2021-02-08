from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_kinesis_data_stream_connector.schema.data import (
    StreamDescription,
)
from spaceone.inventory.libs.schema.dynamic_field import (
    TextDyField,
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
firehose_meta_detail = ItemDynamicLayout.set_fields(
    "Stream Details",
    fields=[
        TextDyField.data_source("ARN", "data.delivery_stream_arn"),
        TextDyField.data_source("Status", "data.delivery_stream_status_display"),
        DateTimeDyField.data_source(
            "Data retention period", "data.create_timestamp"
        ),
        TextDyField.data_source("Permissions (IAM role)", "data.iam_role")
    ],
)

# TAB - Source
firehose_meta_source_details = ItemDynamicLayout.set_fields(
    "Details",
    fields=[
        TextDyField.data_source("Source", "data.source.source_details"),
        TextDyField.data_source("Server-side encryption for source records",
                                "data.delivery_stream_encryption_configuration.status"),
        TextDyField.data_source("Encryption type", "data.delivery_stream_encryption_configuration.key_type"),

    ]
)

firehose_meta_source_lambda = ItemDynamicLayout.set_fields(
    "Transform source records with AWS Lambda",
    "data.lambda",
    fields=[
        TextDyField.data_source("Source record transformation", "source_record_transformation"),
        TextDyField.data_source("Lambda function", "lambda_func"),
        TextDyField.data_source("Lambda function version", "lambda_func_ver"),
        TextDyField.data_source(
            "Timeout", "timeout"
        ),
        TextDyField.data_source("Buffer conditions", "buffer_conditions")
    ]
)

# firehose_meta_source_glue = ItemDynamicLayout.set_fields(
#     "Convert record format",
#     fields=[
#         TextDyField.data_source("Record format conversion", "data.has_glue"),
#         TextDyField.data_source("Output format", "data.output_format"),
#         TextDyField.data_source("Input format", "data.input_format"),
#         TextDyField.data_source("AWS Glue region",
#                                 "data.destinations.extended_s3_destination_description"
#                                 ".data_format_conversion_configuration.schema_configuration.region"),
#         TextDyField.data_source("AWS Glue database",
#                                 "data.destinations.extended_s3_destination_description"
#                                 ".data_format_conversion_configuration.schema_configuration.database_name"),
#         TextDyField.data_source("AWS Glue table",
#                                 "data.destinations.extended_s3_destination_description"
#                                 ".data_format_conversion_configuration.schema_configuration.table_name"),
#         TextDyField.data_source("AWS Glue table version",
#                                 "data.destinations.extended_s3_destination_description"
#                                 ".data_format_conversion_configuration.schema_configuration.version_id")
#     ]
# )


firehose_meta_source = ListDynamicLayout.set_layouts(
    "Source",
    layouts=[
        firehose_meta_source_details,
        # firehose_meta_source_glue,
        # firehose_meta_source_lambda
    ],
)

# TAB - Destination
# firehose_meta_destination_details = ItemDynamicLayout.set_fields(
#     "Details",
#     fields=[
#         TextDyField.data_source("CloudWatch error logging", "data.cloud_watch_logging_options_display"),
#         TextDyField.data_destination("Type", "data.destination_type"),
#         TextDyField.data_destination("Name", "data.destination_name"),
#         TextDyField.data_destination("Server-side encryption for destination records",
#                                 "data.delivery_stream_encryption_configuration.status"),
#         TextDyField.data_destination("Encryption type", "data.delivery_stream_encryption_configuration.key_type"),
#
#     ]
# )
#
# firehose_meta_destination = ListDynamicLayout.set_layouts(
#     "Destination",
#     layouts=[
#         firehose_meta_destination_details,
#     ],
# )
#

# TAB - Tags
firehose_meta_tags = TableDynamicLayout.set_fields(
    "Tags",
    "data.tags",
    fields=[
        TextDyField.data_source("Key", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)

# Overall
firehose_meta = CloudServiceMeta.set_layouts(
    [firehose_meta_detail,
     firehose_meta_source,
     # firehose_meta_destination,
     firehose_meta_tags]
)


class FirehoseResource(CloudServiceResource):  # service type - group
    cloud_service_group = StringType(default="KinesisDataFirehose")


class DeliveryStreamResource(FirehoseResource):  # service type - name
    cloud_service_type = StringType(default="DeliveryStream")
    data = ModelType(StreamDescription)
    _metadata = ModelType(
        CloudServiceMeta, default=firehose_meta, serialized_name="metadata"
    )


class FirehoseResponse(CloudServiceResponse):
    resource = PolyModelType(DeliveryStreamResource)
