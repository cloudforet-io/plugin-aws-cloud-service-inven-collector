from spaceone.inventory.libs.schema.dynamic_field import SearchField, TextDyField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_delivery_streams = CloudServiceTypeResource()
cst_delivery_streams.name = "DeliveryStreams"
cst_delivery_streams.provider = "aws"
cst_delivery_streams.group = "KinesisDataFirehose"
cst_delivery_streams.labels = ["Analytics"]
cst_delivery_streams.is_primary = True
cst_delivery_streams.is_major = True
cst_delivery_streams.service_code = "AmazonKinesisFirehose"
cst_delivery_streams.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-kinesis-firehose.svg',
}

cst_delivery_streams._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.delivery_stream_name'),
        EnumDyField.data_source('Status', 'data.delivery_stream_status_display', default_state={
            'safe': ['Active'],
            'warning': ['Creating', 'Deleting'],
            'alert': ['Creating Failed', 'Deleting Failed']
        }),
        DateTimeDyField.data_source('Creation Time', 'data.create_timestamp'),
        TextDyField.data_source('Source', 'data.source_display'),
        TextDyField.data_source('Data Transformation', 'data.data_transformation'),
        TextDyField.data_source('Destination', 'data.destination_display')
    ],
    search=[
        # SearchField.set(name='Stream Name', key='data.stream_name'),
        # SearchField.set(name='Stream ARN', key='data.stream_arn'),
        # SearchField.set(name='Stream Status', key='data.stream_status'),
        # SearchField.set(name='Consumer Name', key='data.consumer_name'),
        # SearchField.set(name='Consumer ARN', key='data.consumer_arn'),
        # # SearchField.set(name='Shard Status', key='data.shard_status'),
        # SearchField.set(name='Shard ID', key='data.shard_id'),
        # SearchField.set(name='Parent Shard Id', key='data.parent_shard_id'),
        # # SearchField.set(name='Retention Hours', key='data.retention_period_hours'),
        # # SearchField.set(name='Retention Days', key='data.retention_period_days'),
        # # SearchField.set(name='Hash Key', key='data.hash_key_list'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_delivery_streams}),
]
