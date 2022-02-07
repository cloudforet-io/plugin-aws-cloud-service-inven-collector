import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField, \
    ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')

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
        TextDyField.data_source("Name", "name"),
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
        ListDyField.data_source('Destination', 'data.destinations', options={
            'sub_key': 'destination_id',
            'delimiter': '<br>'
        }),
        DateTimeDyField.data_source("Creation time", "data.create_timestamp"),
        TextDyField.data_source('ARN', 'data.delivery_stream_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Type', 'data.delivery_stream_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Version ID', 'data.version_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption Configuration Status',
                                'data.delivery_stream_encryption_configuration.status',
                                options={'is_optional': True}),
        TextDyField.data_source('Failure Description', 'data.failure_description', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name="Stream Name", key="name"),
        SearchField.set(name="Stream ARN", key="data.delivery_stream_arn"),
        SearchField.set(name="Stream Status", key="data.delivery_stream_status"),
        SearchField.set(name="Source Name", key="data.source.source_name"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(stream_count_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(stream_count_per_account_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_firehose}),
]
