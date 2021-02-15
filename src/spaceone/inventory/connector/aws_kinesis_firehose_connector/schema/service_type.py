from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_firehose = CloudServiceTypeResource()
cst_firehose.name = "DeliveryStream"
cst_firehose.provider = "aws"
cst_firehose.group = "KinesisDataFirehose"
cst_firehose.labels = ["Analytics"]
cst_firehose.is_primary = True
cst_firehose.is_major = True
cst_firehose.service_code = "AmazonKinesisFirehose"
cst_firehose.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-kinesis-firehose.svg',
}

cst_firehose._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Name", "data.delivery_stream_name"),
        EnumDyField.data_source(
            "Status",
            "data.delivery_stream_status",
            default_state={
                "safe": ["ACTIVE"],
                'warning': ["CREATING", "DELETING"],
                "alert": ["DELETING_FAILED"],
                "disable": ["CREATING_FAILED", "SUSPENDED"]
            },
        ),
        TextDyField.data_source(
            "Creation time", "data.create_timestamp"
        ),
        TextDyField.data_source("Source", "data.source.source_name"),
        TextDyField.data_source("Data transformation", "data.additional_tabs.lambda_tab.data_transformation"),
        TextDyField.data_source(
            "Destination", "data.additional_tabs.destination_name"
        ),
    ],
    search=[
        SearchField.set(name="Stream Name", key="data.delivery_stream_name"),
        SearchField.set(name="Stream ARN", key="data.delivery_stream_arn"),
        SearchField.set(name="Stream Status", key="data.delivery_stream_status"),
        SearchField.set(name="Source Name", key="data.source.source_name"),
        SearchField.set(name="Destination", key="data.additional_tabs.destination_name"),
        SearchField.set(name="Data transformation", key="data.additional_tabs.lambda_tab.data_transformation"),
        SearchField.set(name="Destination", key="data.additional_tabs.destination_name"),
        SearchField.set(name="Permissions (IAM role)", key="data.additional_tabs.iam_role"),
        SearchField.set(name="Source record transformation (Lambda)",
                        key="data.additional_tabs.lambda_tab.source_record_transformation"),
        SearchField.set(name="Lambda function name", key="data.additional_tabs.lambda_tab.lambda_func"),
        SearchField.set(name="S3 Backup mode", key="data.additional_tabs.s3_backup_info"),
        SearchField.set(
            name="Retention Days", key="data.retention_period_days", data_type="Integer"
        ),
        SearchField.set(
            name="Number of Open Shards",
            key="data.open_shards_num",
            data_type="Integer",
        ),
        SearchField.set(
            name="Number of Closed Shards",
            key="data.closed_shards_num",
            data_type="Integer",
        ),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_firehose}),
]
