import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
queue_max_message_total_size_conf = os.path.join(current_dir, 'widget/queue_max_message_total_size.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')
queue_max_message_total_size_by_account_conf = os.path.join(current_dir, 'widget/queue_max_message_total_size_by_account.yaml')

cst_que = CloudServiceTypeResource()
cst_que.name = 'Queue'
cst_que.provider = 'aws'
cst_que.group = 'SQS'
cst_que.labels = ['Application Integration']
cst_que.is_primary = True
cst_que.is_major = True
cst_que.service_code = 'AWSQueueService'
cst_que.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-SQS.svg',
}

cst_que._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('url', 'data.url'),
        TextDyField.data_source('ARN', 'data.kms.alias', options={
            'is_optional': True
        }),
        TextDyField.data_source('Approximate Number of Messages', 'data.approximate_number_of_messages', options={
            'is_optional': True
        }),
        TextDyField.data_source('Approximate Number of Messages Delay', 'data.approximate_number_of_messages_delayed',
                                options={'is_optional': True}),
        TextDyField.data_source('Approximate Number of Messages Not Visible', 'data.approximate_number_of_messages_not_visible',
                                options={
                                    'is_optional': True
                                }),
        TextDyField.data_source('Delay Seconds', 'data.delay_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Maximum Message Size', 'data.maximum_message_size', options={
            'is_optional': True
        }),
        TextDyField.data_source('Message Retention Period', 'data.message_retention_period', options={
            'is_optional': True
        }),
        TextDyField.data_source('Receive Message Wait Time Seconds', 'data.receive_message_wait_time_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Visiblility Timeout', 'data.visibility_timeout', options={
            'is_optional': True
        }),
        TextDyField.data_source('FIFO Queue', 'data.fifo_queue', options={
            'is_optional': True
        }),
        TextDyField.data_source('Content Based Duplication', 'data.content_based_duplication', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Master Key ID', 'data.kms_master_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Reuse Period Seconds', 'data.kms_data_key_reuse_period_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Dead Letter Target ARN', 'data.redrive_policy.dead_letter_target_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Max Recieve Count', 'data.redrive_policy.max_receive_count', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='URL', key='data.url'),
        SearchField.set(name='Maximum Message Size (Bytes)', key='data.maximum_message_size', data_type='integer'),
        SearchField.set(name='Approximate Number of Messages', key='data.approximate_number_of_messages',
                        data_type='integer'),
        SearchField.set(name='Last Modified Time', key='data.last_modified_timestamp', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(queue_max_message_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(queue_max_message_total_size_by_account_conf)),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_que}),
]
