import logging

from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_elasticache_connector.schema.data import Redis, Memcached
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

logger = logging.getLogger(__name__)


# meta data details (Memcached)
# memcached_base_detail = ItemDynamicView({'name': "Base Information"})
# memcached_base_detail.data_source = [
#     TextDyField.data_source('Cluster', 'data.cluster_name'),
#     TextDyField.data_source('Cluster Endpoint', 'data.configuration_endpoint'),
#     TextDyField.data_source('Status ', 'data.status'),
#     TextDyField.data_source('Engine ', 'data.engine'),
#     TextDyField.data_source('Engine Version Compatibility ', 'data.engine_version_compatibility'),
#     TextDyField.data_source('Availability Zones ', 'data.availability_zone'),
#     TextDyField.data_source('Nodes Pending Deletion ', 'data.nodes_pending_deletion'),
#     TextDyField.data_source('Parameter Group ', 'data.parameter_group'),
#     ListDyField.data_source('Security Groups ', 'data.security_groups'),
#     TextDyField.data_source('Maintenance Window ', 'data.maintenance_window'),
#     TextDyField.data_source('Backup Window ', 'data.backup_window'),
#     TextDyField.data_source('Creation Time ', 'data.creation_time'),
#     TextDyField.data_source('Update Status ', 'data.update_status'),
#     TextDyField.data_source('Node type', 'data.node_type'),
#     TextDyField.data_source('Number of Nodes', 'data.number_of_nodes'),
#     TextDyField.data_source('Number of Nodes Pending Creation', 'data.number_of_nodes_pending_creation'),
#     TextDyField.data_source('Subnet Group', 'data.subnet_group'),
#     TextDyField.data_source('Notification ARN', 'data.notification_arn'),
#     TextDyField.data_source('Backup Retention Period', 'data.backup_retention_period'),
# ]
#
# memcached_node = TableDynamicView({'name': 'Nodes', 'key_path': 'data.nodes'})
# memcached_node.data_source = [
#     TextDyField.data_source('Node Name', 'data.cache_node_id'),
#     TextDyField.data_source('Status', 'data.cache_node_status'),
#     TextDyField.data_source('Port', 'data.endpoint.port'),
#     TextDyField.data_source('Endpoint', 'data.endpoint.address'),
#     TextDyField.data_source('Parameter Group Status', 'data.parameter_group_status'),
#     TextDyField.data_source('Availability Zone', 'data.customer_availability_zone'),
#     TextDyField.data_source('Created on', 'data.cache_node_create_time'),
# ]
#
# memcached_metadata = BaseMetaData()
# memcached_metadata.details = [memcached_base_detail, ]
# memcached_metadata.sub_data = [memcached_node, ]
#
#
#
# # meta data details (Redis)
# redis_base_detail = ItemDynamicView({'name': "Base Information"})
# redis_base_detail.data_source = [
#     TextDyField.data_source('Name', 'data.cluster_name'),
#     TextDyField.data_source('Configuration Endpoint', 'data.configuration_endpoint'),
#     TextDyField.data_source('Creation Time', 'data.creation_time'),
#     TextDyField.data_source('Status', 'data.status'),
#     TextDyField.data_source('Primary Endpoint', 'data.primary_endpoint'),
#     TextDyField.data_source('Update Status', 'data.update_action_status'),
#     TextDyField.data_source('Engine', 'data.engine'),
#     TextDyField.data_source('Engine Version Compatibility', 'data.engine_version_compatibility'),
#     TextDyField.data_source('Reader Endpoint', 'data.reader_endpoint'),
#     TextDyField.data_source('Node Type', 'data.cluster.cache_node_type'),
#     ListDyField.data_source('Availability Zones', 'data.availability_zones'),
#     TextDyField.data_source('Shards', 'data.shard_count'),
#     TextDyField.data_source('Number of Nodes', 'data.node_count'),
#     TextDyField.data_source('Automatic Failover', 'data.cluster.automatic_failover'),
#     TextDyField.data_source('Description', 'data.cluster.description'),
#     TextDyField.data_source('Parameter Group', 'data.parameter_group'),
#     TextDyField.data_source('Subnet Group', 'data.subnet_group'),
#     ListDyField.data_source('Security Groups', 'data.security_groups'),
#     TextDyField.data_source('Notification ARN', 'data.notification_arn'),
#     TextDyField.data_source('Notification status', 'data.notification_status'),
#     TextDyField.data_source('Maintenance Window', 'data.maintenance_window'),
#     TextDyField.data_source('Backup retention Period', 'data.backup_retention_period'),
#     TextDyField.data_source('Backup window', 'data.backup_window'),
#     TextDyField.data_source('Backup Node ID', 'data.backup_node_id'),
#     TextDyField.data_source('Encryption in-transit', 'data.cluster.transit_encryption_enabled'),
#     TextDyField.data_source('Encryption at-rest', 'data.cluster.at_rest_encryption_enabled'),
#     TextDyField.data_source('Redis AUTH', 'data.auth_enabled'),
#     TextDyField.data_source('AUTH Token Last Modified Date', 'data.auth_token_last_modified_date'),
#     TextDyField.data_source('Customer Managed CMK', 'data.cluster.kms_key_id'),
# ]
#
# redis_node = TableDynamicView({'name': 'Nodes', 'key_path': 'data.nodes'})
# redis_node.data_source = [
#     TextDyField.data_source('Name', 'data.cluster_name'),
# ]
#
# redis_metadata = BaseMetaData()
# redis_metadata.details = [redis_base_detail, ]
# redis_metadata.sub_data = [redis_node, ]


memcached_metadata = CloudServiceMeta.set()
redis_metadata = CloudServiceMeta.set()


# Memcached
class ElasticCacheResource(CloudServiceResource):
    cloud_service_group = StringType(default='ElastiCache')


class MemcachedResource(ElasticCacheResource):
    cloud_service_type = StringType(default='Memcached')
    data = ModelType(Memcached)
    cloud_service_meta = ModelType(CloudServiceMeta, default=memcached_metadata)


class MemcachedResponse(CloudServiceResponse):
    resource = PolyModelType(MemcachedResource)


# Redis
class RedisResource(ElasticCacheResource):
    cloud_service_type = StringType(default='Redis')
    data = ModelType(Memcached)
    cloud_service_meta = ModelType(CloudServiceMeta, default=redis_metadata)


class RedisResponse(CloudServiceResponse):
    resource = PolyModelType(RedisResource)


