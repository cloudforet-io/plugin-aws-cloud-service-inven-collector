import time
import logging
from typing import List

from spaceone.inventory.connector.aws_elasticache_connector.schema.data import Redis, Memcached
from spaceone.inventory.connector.aws_elasticache_connector.schema.resource import RedisResource, RedisResponse, \
    MemcachedResource, MemcachedResponse
from spaceone.inventory.connector.aws_elasticache_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class ElastiCacheConnector(SchematicAWSConnector):
    service_name = 'elasticache'

    def get_resources(self):
        print("** ElastiCache START **")
        resources = []
        start_time = time.time()

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ {region_name} ]')
            self.reset_region(region_name)

            cache_clusters = [cluster for cluster in self.describe_clusters()]

            for memcached_vo in self.get_memcached_data(region_name, cache_clusters):
                if getattr(memcached_vo, 'set_cloudwatch', None):
                    memcached_vo.cloudwatch = CloudWatchModel(memcached_vo.set_cloudwatch(region_name))

                resources.append(MemcachedResponse(
                    {'resource': MemcachedResource(
                        {'data': memcached_vo,
                         'tags': [{'key':tag.key, 'value': tag.value} for tag in memcached_vo.tags],
                         'region_code': region_name,
                         'reference': ReferenceModel(memcached_vo.reference(region_name))})}
                ))

            for redis_vo in self.get_redis_data(region_name, cache_clusters):
                if getattr(redis_vo, 'set_cloudwatch', None):
                    redis_vo.cloudwatch = CloudWatchModel(redis_vo.set_cloudwatch(region_name))

                resources.append(RedisResponse(
                    {'resource': RedisResource(
                        {'data': redis_vo,
                         'region_code': region_name,
                         'reference': ReferenceModel(redis_vo.reference(region_name))})}
                ))

        print(f' ElastiCache Finished {time.time() - start_time} Seconds')
        return resources

    def get_memcached_data(self, region_name, cache_clusters):
        for cluster in cache_clusters:
            if cluster.get('Engine') == 'memcached':
                cluster.update({
                    'configuration_endpoint_display': self.set_configuration_endpoint_display(cluster.get('ConfigurationEndpoint')),
                    'nodes': self.get_memcached_nodes(cluster),
                    'tags': self.list_tags(cluster['ARN']),
                    'account_id': self.account_id,
                })

                yield Memcached(cluster, strict=False)

    def get_redis_data(self, region_name, cache_clusters):
        for replication_group in self.describe_replication_groups():
            replication_group.update({
                'mode': self.set_redis_mode(replication_group.get('ClusterEnabled')),
                'engine': 'redis',
                'engine_version': self.get_engine_version(replication_group, cache_clusters),
                'shard_count': self.get_shard_count(replication_group.get('MemberClusters', [])),
                'availability_zones': self.get_redis_availability_zones(replication_group.get('NodeGroups', [])),
                'subnet_group_name': self.get_redis_subnet_group_name(replication_group, cache_clusters),
                'parameter_group_name': self.get_redis_parameter_group_name(replication_group, cache_clusters),
                'node_count': self.get_node_count(replication_group.get('NodeGroups', [])),
                'account_id': self.account_id
            })

            if replication_group.get('mode') == 'Redis':
                replication_group.update({
                    'primary_endpoint': self.get_redis_primary_endpoint(replication_group),
                    'reader_endpoint': self.get_redis_reader_endpoint(replication_group)
                })

            yield Redis(replication_group, strict=False)

    def describe_clusters(self):
        paginator = self.client.get_paginator('describe_cache_clusters')
        response_iterator = paginator.paginate(
            ShowCacheNodeInfo=True,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data['CacheClusters']:
                yield raw

    def describe_replication_groups(self):
        paginator = self.client.get_paginator('describe_replication_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data['ReplicationGroups']:
                yield raw

    def list_tags(self, arn):
        response = self.client.list_tags_for_resource(ResourceName=arn)
        return [{'key': tag.get('Key'), 'value': tag.get('Value')}for tag in response.get('TagList', [])]

    def get_memcached_nodes(self, cluster):
        nodes = []
        for i in range(cluster.get('NumCacheNodes', 0)):
            nodes.append({
                'node_name': '{:004}'.format(i+1),
                'status': cluster.get('CacheClusterStatus', ''),
                'port': cluster.get('ConfigurationEndpoint', {}).get('Port'),
                'endpoint': cluster.get('ConfigurationEndpoint', {}).get('Address', ''),
                'parameter_group_status': cluster.get('CacheParameterGroup', {}).get('ParameterApplyStatus', ''),
                'created_on': cluster.get('CacheClusterCreateTime'),
            })

        return nodes

    def set_configuration_endpoint_display(self, endpoint):
        if endpoint:
            return f'{endpoint.get("Address")}:{endpoint.get("Port")}'
        else:
            return ''

    @staticmethod
    def set_redis_mode(cluster_enabled):
        if cluster_enabled:
            return 'Clustered Redis'
        else:
            return 'Redis'

    @staticmethod
    def get_node_count(member_clusters):
        return len(member_clusters)

    @staticmethod
    def get_shard_count(node_groups):
        return len(node_groups)

    @staticmethod
    def get_redis_primary_endpoint(replication_group):
        for node_group in replication_group.get('NodeGroups', []):
            primary_endpoint = node_group.get("PrimaryEndpoint", {})
            return f'{primary_endpoint.get("Address", "")}:{primary_endpoint.get("Port", "")}'

    @staticmethod
    def get_redis_reader_endpoint(replication_group):
        for node_group in replication_group.get('NodeGroups', []):
            reader_endpoint = node_group.get("ReaderEndpoint", {})
            return f'{reader_endpoint.get("Address", "")}:{reader_endpoint.get("Port", "")}'

    @staticmethod
    def get_engine_version(replication_group, cache_clusters):
        for member in replication_group.get('MemberClusters', []):
            for cache_cluster in cache_clusters:
                if cache_cluster.get('CacheClusterId') == member:
                    return cache_cluster.get('EngineVersion', '')

        return ''

    @staticmethod
    def get_redis_availability_zones(node_groups):
        azs = []

        for node_group in node_groups:
            members = node_group.get('NodeGroupMembers', [])
            for member in members:
                if member.get('PreferredAvailabilityZone'):
                    azs.append(member.get('PreferredAvailabilityZone'))

        return list(set(azs))

    @staticmethod
    def get_redis_subnet_group_name(replication_group, cache_clusters):
        for member in replication_group.get('MemberClusters', []):
            for cache_cluster in cache_clusters:
                if cache_cluster.get('CacheClusterId') == member:
                    return cache_cluster.get('CacheSubnetGroupName', '')

        return ''

    @staticmethod
    def get_redis_parameter_group_name(replication_group, cache_clusters):
        for member in replication_group.get('MemberClusters', []):
            for cache_cluster in cache_clusters:
                if cache_cluster.get('CacheClusterId') == member:
                    return cache_cluster.get('CacheParameterGroup', {}).get('CacheParameterGroupName', '')

        return ''
