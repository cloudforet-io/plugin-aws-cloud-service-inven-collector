from spaceone.inventory.libs.schema.dynamic_field import (
    SearchField,
    TextDyField,
    EnumDyField,
)
from spaceone.inventory.libs.schema.resource import (
    CloudServiceTypeResource,
    CloudServiceTypeResponse,
    CloudServiceTypeMeta,
)

cst_kds = CloudServiceTypeResource()
cst_kds.name = "DataStreams"
cst_kds.provider = "aws"
cst_kds.group = "KinesisDataStreams"
cst_kds.labels = ["Analytics"]
cst_kds.is_primary = True
cst_kds.is_major = True
cst_kds.service_code = "AmazonKinesis"
cst_kds.tags = {
    "spaceone:icon": "https://assets-console-spaceone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon_Kinesis_Firehose.svg",
}

cst_kds._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Data Stream Name", "data.stream_name"),
        EnumDyField.data_source(
            "Status",
            "data.stream_status_display",
            default_state={
                "safe": ["Active"],
                "warning": ["Creating", "Deleting", "Updating"],
            },
        ),
        TextDyField.data_source("Open shards", "data.open_shards_num"),
        TextDyField.data_source(
            "Data retention period", "data.retention_period_display"
        ),
        TextDyField.data_source("Encryption", "data.encryption_display"),
        TextDyField.data_source(
            "Consumers with enhanced fan-out", "data.consumers_vo.num_of_consumers"
        ),
    ],
    search=[
        SearchField.set(name="Stream Name", key="data.stream_name"),
        SearchField.set(name="Stream ARN", key="data.stream_arn"),
        SearchField.set(name="Stream Status", key="data.stream_status"),
        SearchField.set(name="Consumer Name", key="data.consumers_vo.consumer_name"),
        SearchField.set(name="Consumer ARN", key="data.consumers_vo.consumer_arn"),
        SearchField.set(name="Shard ID", key="data.shards.shard_id"),
        SearchField.set(name="Parent Shard Id", key="data.shards.parent_shard_id"),
        SearchField.set(
            name="Retention Hours",
            key="data.retention_period_hours",
            data_type="Integer",
        ),
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
    CloudServiceTypeResponse({"resource": cst_kds}),
]
