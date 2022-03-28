import time
import logging
from typing import List
import json

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_lightsail_connector.schema.data import Instance, Disk, Bucket, DiskSnapshot, \
    StaticIP, RelationDatabase
from spaceone.inventory.connector.aws_lightsail_connector.schema.resource import \
    InstanceResource, InstanceResponse, DiskResource, DiskResponse, DiskSnapshotResource, DiskSnapshotResponse, \
    BucketResource, BucketResponse, StaticIPResource, StaticIPResponse, RelationDatabaseResource, \
    RelationDatabaseResponse
from spaceone.inventory.connector.aws_lightsail_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class LightsailConnector(SchematicAWSConnector):
    service_name = 'lightsail'
    cloud_service_group = 'Lightsail'
    cloud_service_type = 'Instance'

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: Lightsail")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_instances_data,
                'resource': InstanceResource,
                'response_schema': InstanceResponse
            },
            {
                'request_method': self.request_disks_data,
                'resource': DiskResource,
                'response_schema': DiskResponse
            },
            {
                'request_method': self.request_disk_snapshots_data,
                'resource': DiskSnapshotResource,
                'response_schema': DiskSnapshotResponse
            },
            {
                'request_method': self.request_buckets_data,
                'resource': BucketResource,
                'response_schema': BucketResponse
            },
            {
                'request_method': self.request_static_ips_data,
                'resource': StaticIPResource,
                'response_schema': StaticIPResponse
            },
            {
                'request_method': self.request_relation_database_data,
                'resource': RelationDatabaseResource,
                'response_schema': RelationDatabaseResponse
            },
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: Lightsail ({time.time() - start_time} sec)')
        return resources

    def request_instances_data(self, region_name):
        cloud_service_type = 'Instance'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_instances')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('instances', []):
                try:
                    instance = Instance(raw, strict=False)

                    yield {
                        'data': instance,
                        'name': instance.name,
                        'instance_type': instance.bundle_id,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_disks_data(self, region_name):
        cloud_service_type = 'Disk'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_disks')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('disks', []):
                try:
                    disk = Disk(raw, strict=False)

                    yield {
                        'data': disk,
                        'name': disk.name,
                        'instance_size': float(disk.size_in_gb),
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_disk_snapshots_data(self, region_name):
        cloud_service_type = 'Snapshot'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_disk_snapshots')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('diskSnapshots', []):
                try:
                    disk_snapshot = DiskSnapshot(raw, strict=False)

                    yield {
                        'data': disk_snapshot,
                        'name': disk_snapshot.name,
                        'instance_size': float(disk_snapshot.size_in_gb),
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_buckets_data(self, region_name):
        cloud_service_type = 'Bucket'
        self.cloud_service_type = cloud_service_type

        for data in self.client.get_buckets().get('buckets', []):
            try:
                bucket = Bucket(data, strict=False)

                yield {
                    'data': bucket,
                    'name': bucket.name,
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = data.get('arn', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def request_static_ips_data(self, region_name):
        cloud_service_type = 'StaticIP'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_static_ips')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('staticIps', []):
                try:
                    static_ip = StaticIP(raw, strict=False)

                    yield {
                        'data': static_ip,
                        'name': static_ip.name,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_relation_database_data(self, region_name):
        cloud_service_type = 'Database'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_relational_databases')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('relationalDatabases', []):
                try:
                    rdb = RelationDatabase(raw, strict=False)

                    yield {
                        'data': rdb,
                        'name': rdb.name,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}
