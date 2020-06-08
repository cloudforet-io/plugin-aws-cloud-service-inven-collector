import time
import logging
from typing import List

from spaceone.inventory.connector.aws_elasticache_connector.schema.data import Redis, Memcached, Cluster, \
    ReplicationGroup
from spaceone.inventory.connector.aws_elasticache_connector.schema.resource import RedisResource, RedisResponse, \
    MemcachedResource, MemcachedResponse
from spaceone.inventory.connector.aws_elasticache_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class ElastiCacheConnector(SchematicAWSConnector):
    redis_response_schema = RedisResponse
    memcached_response_schema = MemcachedResponse

    service_name = 'elasticache'

    _elasticache_clusters: List[RedisResource] = None

    def get_resources(self) -> List[RedisResource]:
        print("** ElastiCache START **")
        resources = []
        start_time = time.time()

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for func in self.request_data():
            resources.append(self.redis_response_schema(
                {'resource': RedisResource({'data': func,
                                            'reference': ReferenceModel(func.reference)})}))

            resources.append(self.redis_response_schema(
                {'resource': RedisResource({'data': func,
                                            'reference': ReferenceModel(func.reference)})}))

        print(f' ElastiCache Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self):
        clusters = self.describe_clusters()
        replication_groups = self.describe_replication_groups()

        for replication_group in replication_groups:
            redis_cluster = ReplicationGroup(replication_group, strict=False)

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