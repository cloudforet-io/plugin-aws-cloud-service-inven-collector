from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.data import DeliveryStreamDescription
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, ListDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

"""
kinesis
"""
# TAB - Stream
firehose_meta_stream_details = ItemDynamicLayout.set_fields(
    "Stream Details",
    fields=[
        TextDyField.data_source("ARN", "data.delivery_stream_arn"),
        EnumDyField.data_source(
            "Status",
            "data.delivery_stream_status",
            default_state={
                "safe": ["ACTIVE"],
                'warning': ["CREATING", "DELETING"],
                "alert": ["DELETING_FAILED", "CREATING_FAILED", "SUSPENDED"]
            },
        ),
        DateTimeDyField.data_source("Creation Time", "data.create_timestamp"),
        TextDyField.data_source("Source", "data.source.source_name"),
        ListDyField.data_source('Destination', 'data.destinations', options={
            'sub_key': 'destination_id',
            'delimiter': '<br>'
        }),
        TextDyField.data_source('ARN', 'data.delivery_stream_arn'),
        TextDyField.data_source('Type', 'data.delivery_stream_type'),
        TextDyField.data_source('Version ID', 'data.version_id'),
        TextDyField.data_source('Encryption Configuration Status',
                                'data.delivery_stream_encryption_configuration.status'),
        TextDyField.data_source('Failure Description', 'data.failure_description')
    ],
)

# TAB - Source
firehose_meta_source_details = ItemDynamicLayout.set_fields(
    "Source",
    fields=[
        TextDyField.data_source("Source Name", "data.source.source_name"),
        TextDyField.data_source("Source Details", "data.source.source_details"),
        TextDyField.data_source("Server-side encryption for source records",
                                "data.delivery_stream_encryption_configuration.status"),
        TextDyField.data_source("Encryption type", "data.delivery_stream_encryption_configuration.key_type"),
    ]
)

# TAB - S3 Destination
firehose_meta_s3_destination_details = TableDynamicLayout.set_fields(
    "S3 Destination Details",
    root_path="data.destinations.s3_destination_description",
    fields=[
        TextDyField.data_source("S3 Bucket ARN", "bucket_arn"),
        TextDyField.data_source("Prefix", "prefix"),
        TextDyField.data_source("Error prefix", "error_output_prefix"),
        TextDyField.data_source("Buffer Size", "buffering_hints.size_in_mbs"),
        TextDyField.data_source("Buffer Interval", "buffering_hints.interval_in_seconds"),
        TextDyField.data_source("Compression", "compression_format"),
        TextDyField.data_source("Encryption", "encryption_configuration.kms_encryption_config.aws_kms_key_arn"),
        TextDyField.data_source("Cloud Watch Logging", "cloud_watch_logging_optinos.enabled"),
    ]
)

firehose_meta_s3_destination_extend = TableDynamicLayout.set_fields(
    "Extend Details",
    root_path="data.destinations.extended_s3_destination_description",
    fields=[
        TextDyField.data_source("S3 Backup Mode", "s3_backup_mode"),
        TextDyField.data_source("S3 Backup Bucket ARN", "s3_backup_description.bucket_arn"),
        TextDyField.data_source("Processing Configuration", "processing_configuration.enabled"),
        ListDyField.data_source("Processing Type", "processing_configuration.processors", options={
            'sub_key': 'type',
            'delimiter': '<br>'
        }),
        TextDyField.data_source("Dynamic Partition Enabled", "dynamic_partitioning_configuration.enabled"),
    ]
)

firehose_meta_s3_destination = ListDynamicLayout.set_layouts(
    "Amazon S3 Destination",
    layouts=[
        firehose_meta_s3_destination_details,
        firehose_meta_s3_destination_extend
    ],
)

# TAB - Http Endpoint Destination
firehose_meta_http_endpoint_destination_details = TableDynamicLayout.set_fields(
    "Http Endpoint Destination",
    root_path="data.destinations.http_endpoint_destination_description",
    fields=[
        TextDyField.data_source("HTTP endpoint name", "endpoint_configuration.name"),
        TextDyField.data_source("HTTP endpoint URL", "endpoint_configuration.url"),
        TextDyField.data_source("Content encoding", "request_configuration.content_encoding"),
        TextDyField.data_source("Retry duration", "retry_options.duration_in_seconds"),
        TextDyField.data_source("S3 Backup Mode", "s3_backup_mode"),
    ]
)

# TAB - Elastic Search Destination
firehose_meta_elasticsearch_destination_description = TableDynamicLayout.set_fields(
    "Amazon Elastic Search Destination",
    root_path="data.destinations.elasticsearch_destination_description",
    fields=[
        TextDyField.data_source("Cluster endpoint", "cluster_endpoint"),
        TextDyField.data_source("Domain ARN", "domain_arn"),
        TextDyField.data_source("Index Name", "index_name"),
        TextDyField.data_source("Type Name", "type_name"),
        TextDyField.data_source("Index rotation period", "index_rotation_period"),
        TextDyField.data_source("Retry duration", "retry_options.duration_in_seconds"),
        TextDyField.data_source("VPC ID", "vpc_configuration_description.vpc_id"),
        ListDyField.data_source("Subnet ID", "vpc_configuration_description.subnet_ids",
                                default_badge={"delimiter": "<br>"}),
        ListDyField.data_source("Security groups ID", "vpc_configuration_description.security_group_ids",
                                default_badge={"delimiter": "<br>"}),
    ]
)

# TAB - Amazon Openserach Destination
firehose_meta_elasticsearch_destination_description = TableDynamicLayout.set_fields(
    "Amazon Opensearch Destination",
    root_path="data.destinations.amazon_opensearch_service_destination_description",
    fields=[
        TextDyField.data_source("Cluster endpoint", "cluster_endpoint"),
        TextDyField.data_source("Domain ARN", "domain_arn"),
        TextDyField.data_source("Index Name", "index_name"),
        TextDyField.data_source("Type Name", "type_name"),
        TextDyField.data_source("Index rotation period", "index_rotation_period"),
        TextDyField.data_source("Retry duration", "retry_options.duration_in_seconds"),
        TextDyField.data_source("VPC ID", "vpc_configuration_description.vpc_id"),
        ListDyField.data_source("Subnet ID", "vpc_configuration_description.subnet_ids",
                                default_badge={"delimiter": "<br>"}),
        ListDyField.data_source("Security groups ID", "vpc_configuration_description.security_group_ids",
                                default_badge={"delimiter": "<br>"}),
    ]
)

# TAB - Splunk Destination
firehose_meta_splunk_destination_details = TableDynamicLayout.set_fields(
    "Amazon Splunk Destination",
    root_path="data.destinations.splunk_destination_description",
    fields=[
        TextDyField.data_source("HEC Endpoint", "hec_endpoint"),
        TextDyField.data_source("HEC ACK timeout", "hec_acknowledgment_timeout_in_seconds"),
        TextDyField.data_source("Retry duration", "retry_options.duration_in_seconds"),
    ]
)

# TAB - Redshift Destination
firehose_meta_redshift_destination_details = TableDynamicLayout.set_fields(
    "Amazon Redshift Destination",
    root_path="data.destinations.redshift_destination_description",
    fields=[
        TextDyField.data_source("COPY options", "copy_command.copy_options"),
        TextDyField.data_source("COPY command retry duration (seconds)", "retry_options.duration_in_seconds"),
        TextDyField.data_source("Cluster JDBC URL", "cluster_jdbc_url"),
        TextDyField.data_source("User name", "username"),
        TextDyField.data_source("Table", "copy_command.data_table_name"),
        TextDyField.data_source("Columns", "copy_command.data_table_columns")
    ]
)

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
firehose_meta = CloudServiceMeta.set_layouts([
    firehose_meta_stream_details,
    firehose_meta_source_details,
    firehose_meta_s3_destination,
    firehose_meta_splunk_destination_details,
    firehose_meta_redshift_destination_details,
    firehose_meta_http_endpoint_destination_details,
    firehose_meta_elasticsearch_destination_description,
    firehose_meta_elasticsearch_destination_description,
    firehose_meta_tags
])


class FirehoseResource(CloudServiceResource):  # service type - group
    cloud_service_group = StringType(default="KinesisFirehose")


class DeliveryStreamResource(FirehoseResource):  # service type - name
    cloud_service_type = StringType(default="DeliveryStream")
    data = ModelType(DeliveryStreamDescription)
    _metadata = ModelType(
        CloudServiceMeta, default=firehose_meta, serialized_name="metadata"
    )


class FirehoseResponse(CloudServiceResponse):
    resource = PolyModelType(DeliveryStreamResource)
