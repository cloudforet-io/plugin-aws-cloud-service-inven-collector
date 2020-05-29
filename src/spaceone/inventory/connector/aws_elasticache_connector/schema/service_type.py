from spaceone.inventory.libs.schema.dynamic_field import TextDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_memcached = CloudServiceTypeResource()
cst_memcached.name = 'Memcached'
cst_memcached.provider = 'aws'
cst_memcached.group = 'ElastiCache'
cst_memcached.tags = {
    'spaceone:icon': '',
    'spaceone:is_major': 'true',
}

cst_memcached._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Cluster Name', 'data.cluster_name'),
    TextDyField.data_source('Nodes', 'data.node_count'),
    TextDyField.data_source('Node Type', 'data.node_type'),
    TextDyField.data_source('Zone', 'data.zone'),
    TextDyField.data_source('Configuration Endpoint', 'data.configuration_endpoint'),
    TextDyField.data_source('Status', 'data.status'),
    TextDyField.data_source('Update Action Status', 'data.update_action_status'),
])


cst_redis = CloudServiceTypeResource()
cst_redis.name = 'Redis'
cst_redis.provider = 'aws'
cst_redis.group = 'ElastiCache'
cst_redis.tags = {
    'spaceone:icon': '',
    'spaceone:is_major': 'true',
}

cst_redis._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Cluster Name', 'data.cluster_name'),
    TextDyField.data_source('Mode', 'data.mode'),
    TextDyField.data_source('Shard', 'data.shard_count'),
    TextDyField.data_source('Nodes', 'data.node_count'),
    TextDyField.data_source('Node Type', 'data.node_type'),
    TextDyField.data_source('Status', 'data.status'),
    TextDyField.data_source('Update Action Status', 'data.update_action_status'),
    TextDyField.data_source('Encryption in-transit', 'data.encryption_in_transit'),
    TextDyField.data_source('Encryption at-rest', 'data.encryption_at_rest'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_memcached}),
    CloudServiceTypeResponse({'resource': cst_redis}),
]
