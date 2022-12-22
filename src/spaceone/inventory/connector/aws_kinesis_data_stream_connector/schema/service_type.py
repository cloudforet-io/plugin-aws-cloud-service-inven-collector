import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import (
    SearchField,
    TextDyField,
    EnumDyField,
    ListDyField
)
from spaceone.inventory.libs.schema.resource import (
    CloudServiceTypeResource,
    CloudServiceTypeResponse,
    CloudServiceTypeMeta,
)

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
open_shard_total_count_conf = os.path.join(current_dir, 'widget/open_shard_total_count.yaml')
stream_count_by_region_conf = os.path.join(current_dir, 'widget/stream_count_by_region.yaml')
stream_count_by_account_conf = os.path.join(current_dir, 'widget/stream_count_by_account.yaml')

cst_kds = CloudServiceTypeResource()
cst_kds.name = "DataStream"
cst_kds.provider = "aws"
cst_kds.group = "KinesisDataStream"
cst_kds.labels = ["Analytics"]
cst_kds.is_primary = True
cst_kds.is_major = True
cst_kds.service_code = "AmazonKinesis"
cst_kds.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-Kinesis-Firehose.svg',
}

cst_kds._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source(
            "Status",
            "data.stream_status_display",
            default_state={
                "safe": ["Active"],
                "warning": ["Creating", "Deleting", "Updating"],
            },
        ),
        TextDyField.data_source("Open shards", "instance_size"),
        TextDyField.data_source(
            "Data retention period", "data.retention_period_display"
        ),
        TextDyField.data_source("Encryption", "data.encryption_display"),
        TextDyField.data_source(
            "Consumers with enhanced fan-out", "data.consumers_vo.num_of_consumers"
        ),
        TextDyField.data_source('ARN', 'data.stream_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Type', 'data.encryption_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Key ID', 'data.key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Closed Shards', 'data.closed_shards_num', options={
            'is_optional': True
        }),
        ListDyField.data_source('Shard IDs', 'data.shards', options={
            'delimiter': '<br>',
            'sub_key': 'shard_id',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
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
            key="instance_size",
            data_type="Integer",
        ),
        SearchField.set(
            name="Number of Closed Shards",
            key="data.closed_shards_num",
            data_type="Integer",
        ),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(open_shard_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(stream_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(stream_count_by_account_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_kds}),
]
