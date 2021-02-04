from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, SearchField, \
    EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

# CLUSTERS
cst_cluster = CloudServiceTypeResource()
cst_cluster.name = 'Cluster'
cst_cluster.provider = 'aws'
cst_cluster.group = 'msk'
cst_cluster.labels = ['Analytics']
cst_cluster.service_code = 'AmazonMSK'
cst_cluster.tags = {
    'spaceone:icon': 'https://assets-console-spaceone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon_MSK.svg',
}

cst_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Cluster name', 'data.cluster_name'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['ACTIVE'],
            'warning': ['CREATING', 'DELETING', 'HEALING', 'MAINTENANCE', 'REBOOTING_BROKER'],
            'alert': ['FAILED']
        }),
        TextDyField.data_source('Kafka Version', 'data.current_broker_software_info.kafka_version'),
        TextDyField.data_source('Broker Type', 'data.broker_node_group_info.instance_type'),
        TextDyField.data_source('Number Of  Broker Nodes', 'data.number_of_broker_nodes'),
        DateTimeDyField.data_source('Creation time', 'data.creation_time'),
    ],
    search=[
        SearchField.set(name='Cluster name', key='data.cluster_name'),
        SearchField.set(name='Cluster ARN', key='data.cluster_arn'),
        SearchField.set(name='Kafka Version', key='data.current_broker_software_info.kafka_version'),
        SearchField.set(name='Broker Type', key='data.broker_node_group_info.instance_type'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Creation Time', key='data.creation_time', data_type='datetime'),
    ]
)

# CONFIGURATION
cst_config = CloudServiceTypeResource()
cst_config.name = 'Configuration'
cst_config.provider = 'aws'
cst_config.group = 'msk'
cst_config.labels = ['Analytics']
cst_config.service_code = 'AmazonMSK'
cst_config.tags = {
    'spaceone:icon': 'https://assets-console-spaceone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon_MSK.svg',
}

cst_config._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Configuration name', 'data.name'),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['ACTIVE'],
            'warning': ['DELETING'],
            'alert': ['DELETE_FAILED']
        }),
        TextDyField.data_source('Latest Revision', 'data.latest_revision.revision'),
        DateTimeDyField.data_source('Creation time', 'data.creation_time'),
    ],
    search=[
        SearchField.set(name='Configuration name', key='data.name'),
        SearchField.set(name='Status', key='data.state'),
        SearchField.set(name='Creation time', key='data.creation_time', data_type='datetime'),
        SearchField.set(name='Configuration ARN', key='data.arn'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cluster}),
    CloudServiceTypeResponse({'resource': cst_config}),
]
