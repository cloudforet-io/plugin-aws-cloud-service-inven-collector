from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

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
        EnumDyField.data_source('Status', 'data.cache_cluster_status', default_state={
            'safe': ['available'],
        }),
        TextDyField.data_source('Nodes', 'data.num_cache_nodes'),
        TextDyField.data_source('Node Type', 'data.cache_node_type'),
        TextDyField.data_source('Zone', 'data.preferred_availability_zone'),
        TextDyField.data_source('Configuration Endpoint', 'data.configuration_endpoint_display'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Cache Node Type', 'instance_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Engine Version', 'data.engine_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Automatic Failover', 'data.automatic_failover', options={
            'is_optional': True
        }),
        TextDyField.data_source('Endpoint Address', 'data.configuration_endpoint.address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Port', 'data.configuration_endpoint.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Snapshot Retention Limit', 'data.snapshot_retention_limit', options={
            'is_optional': True
        }),
        TextDyField.data_source('Replication Group ID', 'data.replication_group_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Snapshot Window', 'data.snapshot_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Group Name', 'data.cache_subnet_group_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Auth Token Enabled', 'data.auth_token_enabled', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Nodes', key='data.num_cache_nodes', data_type='integer'),
        SearchField.set(name='Node Type', key='instance_type'),
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
        TextDyField.data_source('Mode', 'data.mode'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['available'],
            'warning': ['creating', 'modifying', 'deleting', 'snapshotting'],
            'alert': ['create-failed']
        }),
        TextDyField.data_source('Shard', 'data.shard_count'),
        TextDyField.data_source('Nodes', 'data.node_count'),
        TextDyField.data_source('Node Type', 'instance_type'),
        TextDyField.data_source('Encryption in-transit', 'data.transit_encryption_enabled'),
        TextDyField.data_source('Encryption at-rest', 'data.at_rest_encryption_enabled'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Cache Node Type', 'data.cache_node_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Engine Version', 'data.engine_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Automatic Failover', 'data.automatic_failover', options={
            'is_optional': True
        }),
        TextDyField.data_source('Endpoint Address', 'data.configuration_endpoint.address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Port', 'data.configuration_endpoint.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Snapshot Retention Limit', 'data.snapshot_retention_limit', options={
            'is_optional': True
        }),
        TextDyField.data_source('Parameter Group Name', 'data.parameter_group_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Replication Group ID', 'data.replication_group_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Snapshot Window', 'data.snapshot_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('Multi AZ', 'data.multi_az', options={
            'is_optional': True
        }),
        ListDyField.data_source('Availability Zones', 'data.availability_zones', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Group Name', 'data.subnet_group_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Auth Token Enabled', 'data.auth_token_enabled', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Mode', key='data.mode'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Shard Count', key='data.shard_count', data_type='integer'),
        SearchField.set(name='Node Count', key='data.node_count', data_type='integer'),
        SearchField.set(name='Node Type', key='instance_type'),
        SearchField.set(name='Multi AZ', key='data.multi_az'),
        SearchField.set(name='Configuration Endpoint Address', key='data.configuration_endpoint.address'),
        SearchField.set(name='Configuration Endpoint Port', key='data.configuration_endpoint.port'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_memcached}),
    CloudServiceTypeResponse({'resource': cst_redis}),
]
