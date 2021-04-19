from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_firehose = CloudServiceTypeResource()
cst_firehose.name = "DeliveryStream"
cst_firehose.provider = "aws"
cst_firehose.group = "KinesisFirehose"
cst_firehose.labels = ["Analytics"]
cst_firehose.is_primary = True
cst_firehose.is_major = False
cst_firehose.service_code = "AmazonKinesisFirehose"
cst_firehose.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Kinesis-Firehose.svg',
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
                "alert": ["DELETING_FAILED", "CREATING_FAILED", "SUSPENDED"]
            },
        ),
        TextDyField.data_source("Source", "data.source.source_name"),
        TextDyField.data_source("Data transformation", "data.additional_tabs.lambda_tab.data_transformation"),
        TextDyField.data_source("Destination", "data.additional_tabs.destination_name"),
        DateTimeDyField.data_source("Creation time", "data.create_timestamp"),
    ],
    search=[
        SearchField.set(name="Stream Name", key="data.delivery_stream_name"),
        SearchField.set(name="Stream ARN", key="data.delivery_stream_arn"),
        SearchField.set(name="Stream Status", key="data.delivery_stream_status"),
        SearchField.set(name="Source Name", key="data.source.source_name"),
        SearchField.set(name="Destination", key="data.additional_tabs.destination_name"),
        SearchField.set(name="IAM role", key="data.additional_tabs.iam_role"),
        SearchField.set(name="S3 backup mode", key="data.additional_tabs.s3_backup_info")
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_firehose}),
]
