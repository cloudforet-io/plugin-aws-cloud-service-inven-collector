import logging

from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_elasticache_connector.schema.data import Redis, Memcached
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

logger = logging.getLogger(__name__)

'''
Memcached
'''
memcached_base = ItemDynamicLayout.set_fields('Description', fields=[
    TextDyField.data_source('Cluster Name', 'data.cache_cluster_id'),
    TextDyField.data_source('ARN', 'data.arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['available'],
    }),
    TextDyField.data_source('Configuration Endpoint', 'data.configuration_endpoint_display'),
    TextDyField.data_source('Engine', 'data.engine'),
    TextDyField.data_source('Engine Version Compatibility', 'data.engine_version'),
    TextDyField.data_source('Node Type', 'data.cache_node_type'),
    TextDyField.data_source('Number of Nodes', 'data.num_cache_nodes'),
    TextDyField.data_source('Availability Zones', 'data.preferred_availability_zone'),
    TextDyField.data_source('Parameter Group', 'data.cache_parameter_group.cache_parameter_group_name'),
    TextDyField.data_source('Subnet Group', 'data.cache_subnet_group_name'),
    ListDyField.data_source('Security Group', 'data.security_groups', options={
        'delimiter': '<br>',
        'sub_key': 'security_group_id'
    }),
    TextDyField.data_source('Notification ARN', 'data.notification_configuration.topic_arn'),
    TextDyField.data_source('Maintenance Window', 'data.preferred_maintenance_window'),
    TextDyField.data_source('Backup Retension Period', 'data.snapshot_retention_limit'),
    TextDyField.data_source('Backup Window', 'data.snapshot_window'),
])

memcached_node = TableDynamicLayout.set_fields('Nodes', 'data.nodes', fields=[
    TextDyField.data_source('Node Name', 'node_name'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['available'],
    }),
    TextDyField.data_source('Port', 'port'),
    TextDyField.data_source('Endpoint', 'endpoint'),
    TextDyField.data_source('Parameter Group Status', 'parameter_group_status'),
    DateTimeDyField.data_source('Created On', 'created_on')
])

memcached_tags = SimpleTableDynamicLayout.set_tags()
memcached_metadata = CloudServiceMeta.set_layouts(layouts=[memcached_base, memcached_node, memcached_tags])



'''
Redis
'''
redis_base = ItemDynamicLayout.set_fields('Description', fields=[
    TextDyField.data_source('Name', 'data.replication_group_id'),
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Mode', 'data.mode'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['available'],
        'warning': ['creating', 'modifying', 'deleting', 'snapshotting'],
        'alert': ['create-failed']
    }),
    TextDyField.data_source('Configuration Endpoint', 'data.configuration_endpoint.address'),
    TextDyField.data_source('Configuration Endpoint Port', 'data.configuration_endpoint.port'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Backup Retention Period', 'data.snapshot_retention_limit'),
    TextDyField.data_source('Encryption in-transit', 'data.transit_encryption_enabled'),
    TextDyField.data_source('Backup Window', 'data.snapshot_window'),
    TextDyField.data_source('Encryption at-rest', 'data.at_rest_encryption_enabled'),
    TextDyField.data_source('Redis AUTH Default User Access', 'data.auth_token_enabled'),
    TextDyField.data_source('Custom Managed CMK', 'data.kms_key_id'),
    ListDyField.data_source('User Group', 'data.user_group_ids', options={
        'delimiter': '<br>'
    }),
    DateTimeDyField.data_source('AUTH token last modified date', 'data.auth_token_last_modified_date'),
    ListDyField.data_source('Outpost ARN', 'data.member_clusters_outpost_arns', options={
        'delimiter': '<br>'
    })
])

redis_tags = SimpleTableDynamicLayout.set_tags()
redis_metadata = CloudServiceMeta.set_layouts(layouts=[redis_base, redis_tags])


# Memcached
class ElasticCacheResource(CloudServiceResource):
    cloud_service_group = StringType(default='ElastiCache')


class MemcachedResource(ElasticCacheResource):
    cloud_service_type = StringType(default='Memcached')
    data = ModelType(Memcached)
    _metadata = ModelType(CloudServiceMeta, default=memcached_metadata, serialized_name='metadata')


class MemcachedResponse(CloudServiceResponse):
    resource = PolyModelType(MemcachedResource)


# Redis
class RedisResource(ElasticCacheResource):
    cloud_service_type = StringType(default='Redis')
    data = ModelType(Redis)
    _metadata = ModelType(CloudServiceMeta, default=redis_metadata, serialized_name='metadata')


class RedisResponse(CloudServiceResponse):
    resource = PolyModelType(RedisResource)


