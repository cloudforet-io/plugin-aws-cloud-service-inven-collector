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

            for memcached_vo in self.get_memcached_data(region_name):
                if getattr(memcached_vo, 'set_cloudwatch', None):
                    memcached_vo.cloudwatch = CloudWatchModel(memcached_vo.set_cloudwatch(region_name))

                resources.append(MemcachedResponse(
                    {'resource': MemcachedResource(
                        {'data': memcached_vo,
                         'tags': [{'key':tag.key, 'value': tag.value} for tag in memcached_vo.tags],
                         'region_code': region_name,
                         'reference': ReferenceModel(memcached_vo.reference(region_name))})}
                ))

            for redis_vo in self.get_redis_data(region_name):
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

    def get_memcached_data(self, region_name):
        for cluster in self.describe_clusters():
            if cluster.get('Engine') == 'memcached':
                cluster.update({
                    'configuration_endpoint_display': self.set_configuration_endpoint_display(cluster.get('ConfigurationEndpoint')),
                    'nodes': self.get_memcached_nodes(cluster),
                    'tags': self.list_tags(cluster['ARN']),
                    'account_id': self.account_id,
                })

                yield Memcached(cluster, strict=False)

    def get_redis_data(self, region_name):
        for replication_group in self.describe_replication_groups():
            replication_group.update({
                'mode': self.set_redis_mode(replication_group.get('ClusterEnabled')),
                'account_id': self.account_id
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

    def set_redis_mode(self, cluster_enabled):
        if cluster_enabled:
            return 'Clustered Redis'
        else:
            return 'Redis'