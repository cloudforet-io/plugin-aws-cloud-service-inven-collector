import logging

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_elasticache_connector.schema.data import Redis, Memcached, Valkey
from spaceone.inventory.connector.aws_elasticache_connector.schema.resource import RedisResource, RedisResponse, \
    MemcachedResource, MemcachedResponse, ValkeyResponse, ValkeyResource
from spaceone.inventory.connector.aws_elasticache_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel, CloudWatchModel


_LOGGER = logging.getLogger(__name__)


class ElastiCacheConnector(SchematicAWSConnector):
    service_name = 'elasticache'
    cloud_service_group = 'ElastiCache'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: ElastiCache")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)
                cache_clusters = [cluster for cluster in self.describe_clusters()]

                for memcached_vo in self.get_memcached_data(region_name, cache_clusters):
                    if getattr(memcached_vo, 'resource_type', None) and memcached_vo.resource_type == 'inventory.ErrorResource':
                        # Error Resource
                        resources.append(memcached_vo)
                    else:
                        if getattr(memcached_vo, 'set_cloudwatch', None):
                            memcached_vo.cloudwatch = CloudWatchModel(memcached_vo.set_cloudwatch(region_name))

                        resources.append(MemcachedResponse({'resource': memcached_vo}))

                replication_groups = [cluster for cluster in self.describe_replication_groups()]

                for redis_vo in self.get_redis_data(region_name, replication_groups, cache_clusters):
                    if getattr(redis_vo, 'resource_type', None) and redis_vo.resource_type == 'inventory.ErrorResource':
                        # Error Resource
                        resources.append(redis_vo)
                    else:
                        if getattr(redis_vo, 'set_cloudwatch', None):
                            redis_vo.cloudwatch = CloudWatchModel(redis_vo.set_cloudwatch(region_name))

                        resources.append(RedisResponse({'resource': redis_vo}))

                for valkey_vo in self.get_valkey_data(region_name, replication_groups, cache_clusters):
                    if getattr(valkey_vo, 'resource_type', None) and valkey_vo.resource_type == 'inventory.ErrorResource':
                        # Error Resource
                        resources.append(valkey_vo)
                    else:
                        if getattr(valkey_vo, 'set_cloudwatch', None):
                            valkey_vo.cloudwatch = CloudWatchModel(valkey_vo.set_cloudwatch(region_name))

                        resources.append(ValkeyResponse({'resource': valkey_vo}))
            except Exception as e:
                error_resource_response = self.generate_error(region_name, '', e)
                resources.append(error_resource_response)

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: ElastiCache ({time.time() - start_time} sec)')
        return resources

    def get_memcached_data(self, region_name, cache_clusters):
        self.cloud_service_type = 'Memcached'
        cloudtrail_resource_type = None

        for cluster in cache_clusters:
            try:
                if cluster.get('Engine') == 'memcached':
                    cluster.update({
                        'configuration_endpoint_display': self.set_configuration_endpoint_display(cluster.get('ConfigurationEndpoint')),
                        'nodes': self.get_memcached_nodes(cluster),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                          cluster['CacheClusterId'])
                    })

                    memcached_vo = Memcached(cluster, strict=False)

                    yield MemcachedResource({
                        'data': memcached_vo,
                        'name': memcached_vo.cache_cluster_id,
                        'instance_type': memcached_vo.cache_node_type,
                        'launched_at': self.datetime_to_iso8601(memcached_vo.cache_cluster_create_time),
                        'account': self.account_id,
                        'tags': self.list_tags(memcached_vo.arn),
                        'region_code': region_name,
                        'reference': ReferenceModel(memcached_vo.reference(region_name))
                    })

            except Exception as e:
                resource_id = cluster.get('ARN', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def get_redis_data(self, region_name, replication_groups, cache_clusters):
        self.cloud_service_type = 'Redis'
        cloudtrail_resource_type = None

        for replication_group in replication_groups:
            try:
                if replication_group.get('Engine') == 'redis':
                    replication_group.update({
                        'mode': self.set_redis_mode(replication_group.get('ClusterEnabled')),
                        'engine': 'redis',
                        'engine_version': self.get_engine_version(replication_group, cache_clusters),
                        'shard_count': self.get_shard_count(replication_group.get('NodeGroups', [])),
                        'availability_zones': self.get_availability_zones(replication_group.get('NodeGroups', [])),
                        'subnet_group_name': self.get_subnet_group_name(replication_group, cache_clusters),
                        'parameter_group_name': self.get_parameter_group_name(replication_group, cache_clusters),
                        'node_count': self.get_node_count(replication_group.get('MemberClusters', [])),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                          replication_group['ReplicationGroupId']),
                        'nodes': self.get_nodes_info(replication_group, cache_clusters),
                    })

                    if replication_group.get('mode') == 'Redis':
                        replication_group.update({
                            'primary_endpoint': self.get_primary_endpoint(replication_group),
                            'reader_endpoint': self.get_reader_endpoint(replication_group)
                        })
                    elif replication_group.get('mode') == 'Clustered Redis':
                        replication_group.update({
                            'shards': self.get_shards_info(replication_group)
                        })

                    redis_vo = Redis(replication_group, strict=False)

                    yield RedisResource({
                        'data': redis_vo,
                        'name': redis_vo.replication_group_id,
                        'instance_type': redis_vo.cache_node_type,
                        'account': self.account_id,
                        'region_code': region_name,
                        'tags': self.list_tags(redis_vo.arn),
                        'reference': ReferenceModel(redis_vo.reference(region_name))
                    })

            except Exception as e:
                resource_id = replication_group.get('ARN', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def get_valkey_data(self, region_name, replication_groups, cache_clusters):
        self.cloud_service_type = 'Valkey'
        cloudtrail_resource_type = None

        for replication_group in replication_groups:
            try:
                if replication_group.get('Engine') == 'valkey':
                    replication_group.update({
                        'mode': self.set_valkey_mode(replication_group.get('ClusterEnabled')),
                        'engine': 'valkey',
                        'engine_version': self.get_engine_version(replication_group, cache_clusters),
                        'shard_count': self.get_shard_count(replication_group.get('NodeGroups', [])),
                        'availability_zones': self.get_availability_zones(
                            replication_group.get('NodeGroups', [])),
                        'subnet_group_name': self.get_subnet_group_name(replication_group, cache_clusters),
                        'parameter_group_name': self.get_parameter_group_name(replication_group, cache_clusters),
                        'node_count': self.get_node_count(replication_group.get('MemberClusters', [])),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                          replication_group['ReplicationGroupId']),
                        'nodes': self.get_nodes_info(replication_group, cache_clusters),
                    })

                    if replication_group.get('mode') == 'Valkey':
                        replication_group.update({
                            'primary_endpoint': self.get_primary_endpoint(replication_group),
                            'reader_endpoint': self.get_reader_endpoint(replication_group)
                        })
                    elif replication_group.get('mode') == 'Clustered Valkey':
                        replication_group.update({
                            'shards': self.get_shards_info(replication_group)
                        })

                    valkey_vo = Valkey(replication_group, strict=False)

                    yield ValkeyResource({
                        'data': valkey_vo,
                        'name': valkey_vo.replication_group_id,
                        'instance_type': valkey_vo.cache_node_type,
                        'account': self.account_id,
                        'region_code': region_name,
                        'tags': self.list_tags(valkey_vo.arn),
                        'reference': ReferenceModel(valkey_vo.reference(region_name))
                    })

            except Exception as e:
                resource_id = replication_group.get('ARN', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

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
        try:
            response = self.client.list_tags_for_resource(ResourceName=arn)
            return self.convert_tags_to_dict_type(response.get('TagList', []))
        except Exception as e:
            return {}

    @staticmethod
    def get_memcached_nodes(cluster):
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

    @staticmethod
    def set_configuration_endpoint_display(endpoint):
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
    def set_valkey_mode(cluster_enabled):
        if cluster_enabled:
            return 'Clustered Valkey'
        else:
            return 'Valkey'

    @staticmethod
    def get_node_count(member_clusters):
        return len(member_clusters)

    @staticmethod
    def get_shard_count(node_groups):
        return len(node_groups)

    @staticmethod
    def get_primary_endpoint(replication_group):
        for node_group in replication_group.get('NodeGroups', []):
            primary_endpoint = node_group.get("PrimaryEndpoint", {})
            return f'{primary_endpoint.get("Address", "")}:{primary_endpoint.get("Port", "")}'

    @staticmethod
    def get_reader_endpoint(replication_group):
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
    def get_availability_zones(node_groups):
        azs = []

        for node_group in node_groups:
            members = node_group.get('NodeGroupMembers', [])
            for member in members:
                if member.get('PreferredAvailabilityZone'):
                    azs.append(member.get('PreferredAvailabilityZone'))

        return list(set(azs))

    @staticmethod
    def get_subnet_group_name(replication_group, cache_clusters):
        for member in replication_group.get('MemberClusters', []):
            for cache_cluster in cache_clusters:
                if cache_cluster.get('CacheClusterId') == member:
                    return cache_cluster.get('CacheSubnetGroupName', '')

        return ''

    @staticmethod
    def get_parameter_group_name(replication_group, cache_clusters):
        for member in replication_group.get('MemberClusters', []):
            for cache_cluster in cache_clusters:
                if cache_cluster.get('CacheClusterId') == member:
                    return cache_cluster.get('CacheParameterGroup', {}).get('CacheParameterGroupName', '')

        return ''

    def get_nodes_info(self, replication_group, cache_clusters):
        nodes = []

        for member in replication_group.get('MemberClusters', []):
            node_dic = {}
            for cache_cluster in cache_clusters:
                if cache_cluster.get('CacheClusterId') == member:
                    node_dic.update({
                        'node_name': member,
                        'arn': cache_cluster.get('ARN'),
                        'status': cache_cluster.get('CacheClusterStatus', ''),
                        'parameter_group_status': cache_cluster.get('CacheParameterGroup', {}).get('ParameterApplyStatus', ''),
                        'created_on': cache_cluster.get('CacheClusterCreateTime', '')
                    })
                    break

            for node_group in replication_group.get('NodeGroups', []):
                for node_group_member in node_group.get('NodeGroupMembers', []):
                    if node_group_member.get('CacheClusterId') == member:
                        if replication_group.get('ClusterEnabled') is False:
                            node_dic.update({
                                'current_role': node_group_member.get('CurrentRole', ''),
                                'endpoint': node_group_member.get('ReadEndpoint', {}).get('Address', ''),
                                'port': node_group_member.get('ReadEndpoint', {}).get('Port', ''),
                                'zone': node_group_member.get('PreferredAvailabilityZone', ''),
                            })
                        else:
                            node_dic.update({
                                'endpoint': self.set_cluster_node_endpoint(member, replication_group.get('ConfigurationEndpoint', {}).get('Address')),
                                'port': replication_group.get('ConfigurationEndpoint', {}).get('Port', ''),
                                'zone': node_group_member.get('PreferredAvailabilityZone', ''),
                            })

            nodes.append(node_dic)

        return nodes

    @staticmethod
    def get_shards_info(replication_group):
        shards = []

        for node_group in replication_group.get('NodeGroups', []):
             shards.append({
                'shard_name': f'{replication_group.get("ReplicationGroupId", "")}-{node_group.get("NodeGroupId", "")}',
                'nodes': len(node_group.get('NodeGroupMembers', [])),
                'status': node_group.get('Status', ''),
                'slots': node_group.get('Slots', '')
            })

        return shards

    @staticmethod
    def set_cluster_node_endpoint(member, address):
        if address:
            address_split = address.split('.')[1:]
            address_split.insert(0, member)
            return '.'.join(address_split)