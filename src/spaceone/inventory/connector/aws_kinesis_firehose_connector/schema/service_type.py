from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_firehose = CloudServiceTypeResource()
cst_firehose.name = "DeliveryStreams"
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
            "data.delivery_stream_status_display",
            default_state={
                "safe": ["Active"],
                'warning': ["Deleting", "Updating"],
                "alert": ["Deleting_failed"],
                "disable": ["Creating_failed", "Suspended"]
            },
        ),
        TextDyField.data_source(
            "Creation time", "data.create_timestamp"
        ),
        TextDyField.data_source("Source", "data.source.source_name"),
        TextDyField.data_source("Data transformation", "data.lambda_info.data_transformation"),
        TextDyField.data_source(
            "Destination", "data.destination_display"
        ),
    ],
    search=[
        # SearchField.set(name="Stream Name", key="data.stream_name"),
        # SearchField.set(name="Stream ARN", key="data.stream_arn"),
        # SearchField.set(name="Stream Status", key="data.stream_status"),
        # SearchField.set(name="Consumer Name", key="data.consumers_vo.consumer_name"),
        # SearchField.set(name="Consumer ARN", key="data.consumers_vo.consumer_arn"),
        # SearchField.set(name="Shard ID", key="data.shards.shard_id"),
        # SearchField.set(name="Parent Shard Id", key="data.shards.parent_shard_id"),
        # SearchField.set(
        #     name="Retention Hours",
        #     key="data.retention_period_hours",
        #     data_type="Integer",
        # ),
        # SearchField.set(
        #     name="Retention Days", key="data.retention_period_days", data_type="Integer"
        # ),
        # SearchField.set(
        #     name="Number of Open Shards",
        #     key="data.open_shards_num",
        #     data_type="Integer",
        # ),
        # SearchField.set(
        #     name="Number of Closed Shards",
        #     key="data.closed_shards_num",
        #     data_type="Integer",
        # ),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_firehose}),
]
