import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, SearchField, \
    EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
CLUSTER
"""
total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')

# CLUSTERS
cst_cluster = CloudServiceTypeResource()
cst_cluster.name = 'Cluster'
cst_cluster.provider = 'aws'
cst_cluster.group = 'MSK'
cst_cluster.labels = ['Analytics']
cst_cluster.service_code = 'AmazonMSK'
cst_cluster.is_primary = True
cst_cluster.is_major = True
cst_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-MSK.svg',
}

cst_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['ACTIVE'],
            'warning': ['CREATING', 'DELETING', 'HEALING', 'MAINTENANCE', 'REBOOTING_BROKER'],
            'alert': ['FAILED']
        }),
        TextDyField.data_source('Kafka Version', 'data.current_broker_software_info.kafka_version'),
        TextDyField.data_source('Broker Type', 'data.broker_node_group_info.instance_type'),
        TextDyField.data_source('Number Of  Broker Nodes', 'data.number_of_broker_nodes'),
        TextDyField.data_source('ARN', 'data.cluster_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Active Operation ARN', 'data.active_operation_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Zookeeper Connect String TLS', 'data.zookeeper_connect_string_tls', options={
            'is_optional': True
        }),
        TextDyField.data_source('Zookeeper Connect String', 'data.zookeeper_connect_string', options={
            'is_optional': True
        }),
        ListDyField.data_source('Nodes ARN', 'data.node_info_list', options={
            'delimiter': '<br>',
            'sub_key': 'node_arn',
            'is_optional': True
        }),
        TextDyField.data_source('Client Auth SASL', 'data.client_authentication.sasl', options={
            'is_optional': True
        }),
        TextDyField.data_source('Client Auth TLS', 'data.client_authentication.tls', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encryption At Rest', 'data.encryption_info.encryption_at_rest.data_volume_kms_key_id',
                                options={
                                    'is_optional': True
                                }),
        TextDyField.data_source('Encryption In Transit', 'data.encryption_info.encryption_in_transit.client_broker',
                                options={
                                    'is_optional': True
                                }),
        TextDyField.data_source('Enhance Monitoring', 'data.enhanced_monitoring', options={
            'is_optional': True
        }),
        TextDyField.data_source('Prometheus JMX Exporter', 'data.open_monitoring.prometheus.jmx_exporter', options={
            'is_optional': True
        }),
        TextDyField.data_source('Prometheus Node Exporter', 'data.open_monitoring.prometheus.node_exporter', options={
            'is_optional': True
        }),
        TextDyField.data_source('Logging (S3 Bucket)', 'data.logging_info.s3.bucket', options={
            'is_optional': True
        }),
        TextDyField.data_source('Logging (Firehose)', 'data.logging_info.firehose.delivery_stream', options={
            'is_optional': True
        }),
        TextDyField.data_source('Logging (Cloudwatch)', 'data.logging_info.broker_logs.cloud_watch_logs', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Cluster ARN', key='data.cluster_arn'),
        SearchField.set(name='Kafka Version', key='data.current_broker_software_info.kafka_version'),
        SearchField.set(name='Broker Type', key='data.broker_node_group_info.instance_type'),
        SearchField.set(name='Status', key='data.state')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
    ]
)

"""
CONFIGURATION
"""
# CONFIGURATION
cst_config = CloudServiceTypeResource()
cst_config.name = 'ClusterConfiguration'
cst_config.provider = 'aws'
cst_config.group = 'MSK'
cst_config.labels = ['Analytics']
cst_config.service_code = 'AmazonMSK'
cst_config.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-MSK.svg',
}

cst_config._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['ACTIVE'],
            'warning': ['DELETING'],
            'alert': ['DELETE_FAILED']
        }),
        TextDyField.data_source('Latest Revision', 'data.latest_revision.revision'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Kafka Version', 'data.kafka_versions', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Status', key='data.state'),
        SearchField.set(name='Configuration ARN', key='data.arn'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cluster}),
    CloudServiceTypeResponse({'resource': cst_config}),
]
