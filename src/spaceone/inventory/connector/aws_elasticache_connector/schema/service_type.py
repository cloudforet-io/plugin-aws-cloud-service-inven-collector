from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_memcached = CloudServiceTypeResource()
cst_memcached.name = 'Memcached'
cst_memcached.provider = 'aws'
cst_memcached.group = 'ElastiCache'
cst_memcached.labels = ['Database']
cst_memcached.is_primary = True
cst_memcached.is_major = True
cst_memcached.service_code = 'AmazonElastiCache'
cst_memcached.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-ElastiCache.svg'
}

cst_memcached._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Cluster Name', 'data.cache_cluster_id'),
        EnumDyField.data_source('Status', 'data.cache_cluster_status', default_state={
            'safe': ['available'],
        }),
        TextDyField.data_source('Nodes', 'data.num_cache_nodes'),
        TextDyField.data_source('Node Type', 'data.cache_node_type'),
        TextDyField.data_source('Zone', 'data.preferred_availability_zone'),
        TextDyField.data_source('Configuration Endpoint', 'data.configuration_endpoint_display'),
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Cluster Name', key='data.cache_cluster_id'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Nodes', key='data.num_cache_nodes', data_type='integer'),
        SearchField.set(name='Node Type', key='data.cache_node_type'),
        SearchField.set(name='Zone', key='data.preferred_availability_zone'),
        SearchField.set(name='Configuration Endpoint Address', key='data.configuration_endpoint.address'),
        SearchField.set(name='Configuration Endpoint Port', key='data.configuration_endpoint.port'),
    ]
)


cst_redis = CloudServiceTypeResource()
cst_redis.name = 'Redis'
cst_redis.provider = 'aws'
cst_redis.group = 'ElastiCache'
cst_redis.labels = ['Database']
cst_redis.is_primary = True
cst_redis.is_major = True
cst_redis.service_code = 'AmazonElastiCache'
cst_redis.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-ElastiCache.svg'
}

cst_redis._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Cluster Name', 'data.replication_group_id'),
        TextDyField.data_source('Mode', 'data.mode'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['available'],
            'warning': ['creating', 'modifying', 'deleting', 'snapshotting'],
            'alert': ['create-failed']
        }),
        TextDyField.data_source('Shard', 'data.shard_count'),
        TextDyField.data_source('Nodes', 'data.node_count'),
        TextDyField.data_source('Node Type', 'data.cache_node_type'),
        TextDyField.data_source('Encryption in-transit', 'data.transit_encryption_enabled'),
        TextDyField.data_source('Encryption at-rest', 'data.at_rest_encryption_enabled'),
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Cluster Name', key='data.replication_group_id'),
        SearchField.set(name='Mode', key='data.mode'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Shard Count', key='data.shard_count', data_type='integer'),
        SearchField.set(name='Node Count', key='data.node_count', data_type='integer'),
        SearchField.set(name='Node Type', key='data.cache_node_type'),
        SearchField.set(name='Multi AZ', key='data.multi_az'),
        SearchField.set(name='Configuration Endpoint Address', key='data.configuration_endpoint.address'),
        SearchField.set(name='Configuration Endpoint Port', key='data.configuration_endpoint.port'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_memcached}),
    CloudServiceTypeResponse({'resource': cst_redis}),
]
