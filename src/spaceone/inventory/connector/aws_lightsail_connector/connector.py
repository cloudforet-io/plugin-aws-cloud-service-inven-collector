import time
import logging
from typing import List
import json
from datetime import datetime, timedelta

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_lightsail_connector.schema.data import Instance, Disk, Bucket, DiskSnapshot, \
    StaticIP, RelationDatabase, ContainerService, LoadBalancer, Domain, Distribution
from spaceone.inventory.connector.aws_lightsail_connector.schema.resource import \
    InstanceResource, InstanceResponse, DiskResource, DiskResponse, DiskSnapshotResource, DiskSnapshotResponse, \
    BucketResource, BucketResponse, StaticIPResource, StaticIPResponse, RelationDatabaseResource, \
    RelationDatabaseResponse, ContainerServiceResource, ContainerServiceResponse, LoadBalancerResource, LoadBalancerResponse, \
    DomainResource, DomainResponse, DistributionResource, DistributionResponse
from spaceone.inventory.connector.aws_lightsail_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)
EXCLUDE_REGION = ['ap-northeast-3', 'sa-east-1', 'us-west-1', 'me-south-1', 'ap-east-1']


class LightsailConnector(SchematicAWSConnector):
    service_name = 'lightsail'
    cloud_service_group = 'Lightsail'
    cloud_service_type = 'Instance'
    cloud_service_types = CLOUD_SERVICE_TYPES

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
            {
                'request_method': self.request_container_service_data,
                'resource':  ContainerServiceResource,
                'response_schema': ContainerServiceResponse
            },
            {
                'request_method': self.request_loadbalancer_data,
                'resource':  LoadBalancerResource,
                'response_schema': LoadBalancerResponse
            },
            {
                'request_method': self.request_domain_data,
                'resource':  DomainResource,
                'response_schema': DomainResponse
            },
            {
                'request_method': self.request_distribution_data,
                'resource':  DistributionResource,
                'response_schema': DistributionResponse
            }
        ]

        resources.extend(self.set_service_code_in_cloud_service_type())

        for region_name in self.region_names:
            if region_name in EXCLUDE_REGION:
                continue

            self.reset_region(region_name)

            for collect_resource in collect_resources:
                # domain/distribution resources are global
                if (collect_resource['request_method'] == self.request_domain_data) or (collect_resource['request_method'] == self.request_distribution_data):
                    # Global resource query api to us-east-1 region
                    if region_name == 'us-east-1':
                        resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))
                else:
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
                size, count = self.get_bucket_count_and_size(data.get('name'))

                data.update({
                    'object_count': count,
                    'object_total_size': size
                })
                bucket = Bucket(data, strict=False)

                yield {
                    'data': bucket,
                    'name': bucket.name,
                    'instance_size': size,
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

    def request_container_service_data(self, region_name):
        cloud_service_type = 'Container'
        self.cloud_service_type = cloud_service_type

        responses = self.client.get_container_services()

        for raw in responses.get('containerServices', []):
            try:
                container_service = ContainerService(raw, strict=False)

                yield {
                    'data': container_service,
                    'name': container_service.container_service_name,
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = raw.get('arn', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def request_loadbalancer_data(self, region_name):
        cloud_service_type = 'LoadBalancer'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_load_balancers')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('loadBalancers', []):
                try:
                    lb = LoadBalancer(raw, strict=False)

                    yield {
                        'data': lb,
                        'name': lb.name,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_domain_data(self, region_name):
        cloud_service_type = 'Domain'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('get_domains')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
            }
        )

        for data in response_iterator:
            for raw in data.get('domains', []):
                try:
                    domain = Domain(raw, strict=False)

                    yield {
                        'data': domain,
                        'name': domain.name,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_distribution_data(self, region_name):
        cloud_service_type = 'Distribution'
        self.cloud_service_type = cloud_service_type

        responses = self.client.get_distributions()

        for data in responses.get('distributions', []):
            try:
                distribution = Distribution(data, strict=False)

                yield {
                    'data': distribution,
                    'name': distribution.name,
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = data.get('arn', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def get_bucket_count_and_size(self, bucket_name):
        count = float(self._get_bucket_metric_data(bucket_name, "NumberOfObjects"))
        size = float(self._get_bucket_metric_data(bucket_name, "BucketSizeBytes"))

        return size, count

    def _get_bucket_metric_data(self, bucket_name, metric_name):
        start_time, end_time = self._get_start_end_time()
        # Only two types available NumberOfObjects|BucketSizeBytes
        if metric_name == "NumberOfObjects":
            response = self.client.get_bucket_metric_data(
                bucketName=bucket_name,
                metricName="NumberOfObjects",
                startTime=start_time,
                endTime=end_time,
                period=86400, # Number of seconds, bucket storage metrics are reported once per day.
                statistics=["Average"],
                unit="Count"
            )
        else:
            # If metricName is BucketSizeBytes
            response = self.client.get_bucket_metric_data(
                bucketName=bucket_name,
                metricName="BucketSizeBytes",
                startTime=start_time,
                endTime=end_time,
                period=86400, # Number of seconds, bucket storage metrics are reported once per day.
                statistics=["Average"],
                unit="Bytes"
            )
        return response.get("metricData")[0].get("average", 0) if len(response.get("metricData")) > 0 else 0

    @staticmethod
    def _get_start_end_time():
        end = datetime.datetime.utcnow()
        start = end - timedelta(days=2)

        return start, end
