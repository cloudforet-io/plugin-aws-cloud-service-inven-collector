import time
import logging
from typing import List

from spaceone.inventory.connector.aws_documentdb_connector.schema.data import Cluster, Instance, SubnetGroup, \
    ParameterGroup, Parameter, Snapshot
from spaceone.inventory.connector.aws_documentdb_connector.schema.resource import ClusterResource, ClusterResponse,\
    SubnetGroupResource, SubnetGroupResponse, ParameterGroupResource, ParameterGroupResponse
from spaceone.inventory.connector.aws_documentdb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import AWSTags


_LOGGER = logging.getLogger(__name__)
EXCLUDE_REGION = ['us-west-1', 'af-south-1', 'ap-east-1', 'ap-southeast-3', 'ap-northeast-3', 'eu-north-1', 'me-south-1']


class DocumentDBConnector(SchematicAWSConnector):
    service_name = 'docdb'
    cloud_service_group = 'DocumentDB'
    cloud_service_types = CLOUD_SERVICE_TYPES

    _parameter_groups = []
    _subnet_groups = []

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: DocumentDB")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        for region_name in self.region_names:
            if region_name in EXCLUDE_REGION:
                continue

            self.reset_region(region_name)

            collect_resources = [
                {
                    'request_method': self.request_parameter_group_data,
                    'resource': ParameterGroupResource,
                    'response_schema': ParameterGroupResponse
                },
                {
                    'request_method': self.request_subnet_group_data,
                    'resource': SubnetGroupResource,
                    'response_schema': SubnetGroupResponse
                },
                {
                    'request_method': self.request_cluster_data,
                    'resource': ClusterResource,
                    'response_schema': ClusterResponse,
                    'kwargs': {
                        'raw_instances': self._describe_instances(),
                        'raw_snapshots': self._describe_snapshots()
                    }
                },
            ]

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: DocumentDB ({time.time() - start_time} sec)')
        return resources

    def request_cluster_data(self, region_name, **kwargs) -> List[Cluster]:
        self.cloud_service_type = 'Cluster'
        cloudtrail_resource_type = 'AWS::RDS::DBCluster'

        raw_instances = kwargs.get('raw_instances', [])
        raw_snapshots = kwargs.get('raw_snapshots', [])

        paginator = self.client.get_paginator('describe_db_clusters')
        response_iterator = paginator.paginate(
            Filters=[{'Name': 'engine', 'Values': ['docdb']}],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBClusters', []):
                try:
                    instances = self._match_instances(raw_instances, raw.get('DBClusterIdentifier'))
                    raw.update({
                        'instances': instances,
                        'instance_count': len(instances),
                        'snapshots': self._match_snapshots(raw_snapshots, raw.get('DBClusterIdentifier')),
                        'subnet_group': self._match_subnet_group(raw.get('DBSubnetGroup')),
                        'parameter_group': self._match_parameter_group(raw.get('DBClusterParameterGroup')),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                          raw['DBClusterIdentifier']),
                        'tags': self.request_tags(raw['DBClusterArn'])
                    })

                    if subnet_group := self._match_subnet_group(raw.get('DBSubnetGroup')):
                        raw.update({'subnet_group': subnet_group})

                    if parameter_group := self._match_parameter_group(raw.get('DBClusterParameterGroup')):
                        raw.update({'parameter_group': parameter_group})

                    cluster_vo = Cluster(raw, strict=False)
                    yield {
                        'data': cluster_vo,
                        'name': cluster_vo.db_cluster_identifier,
                        'instance_type': cluster_vo.engine_version,
                        'instance_size': float(cluster_vo.instance_count),
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('DBClusterArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_subnet_group_data(self, region_name) -> List[SubnetGroup]:
        self.cloud_service_type = 'SubnetGroup'
        cloudtrail_resource_type = 'AWS::RDS::DBSubnetGroup'

        paginator = self.client.get_paginator('describe_db_subnet_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBSubnetGroups', []):
                try:
                    raw.update({
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                          raw['DBSubnetGroupName']),
                        'tags': self.request_tags(raw['DBSubnetGroupArn'])
                    })
                    subnet_grp_vo = SubnetGroup(raw, strict=False)
                    yield {
                        'data': subnet_grp_vo,
                        'name': subnet_grp_vo.db_subnet_group_name,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('DBSubnetGroupName', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_parameter_group_data(self, region_name) -> List[ParameterGroup]:
        self.cloud_service_type = 'ParameterGroup'
        cloudtrail_resource_type = 'AWS::RDS::DBClusterParameterGroup'

        res_pgs = self.client.describe_db_cluster_parameter_groups()

        for pg_data in res_pgs.get('DBClusterParameterGroups', []):
            try:
                pg_data.update({
                    'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                      pg_data['DBClusterParameterGroupName']),
                    'parameters': self.request_parameter_data(pg_data['DBClusterParameterGroupName']),
                    'tags': self.request_tags(pg_data['DBClusterParameterGroupArn'])
                })
                param_group_vo = ParameterGroup(pg_data, strict=False)
                yield {
                    'data': param_group_vo,
                    'name': param_group_vo.db_cluster_parameter_group_name,
                    'instance_type': param_group_vo.db_parameter_group_family,
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = pg_data.get('DBClusterParameterGroupName', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def request_parameter_data(self, pg_name) -> List[Parameter]:
        res_params = self.client.describe_db_cluster_parameters(DBClusterParameterGroupName=pg_name)
        return list(map(lambda param: Parameter(param, strict=False), res_params.get('Parameters', [])))

    def request_tags(self, resource_arn):
        response = self.client.list_tags_for_resource(ResourceName=resource_arn)
        return list(map(lambda tag: AWSTags(tag, strict=False), response.get('TagList', [])))

    def _describe_instances(self):
        instances = []
        paginator = self.client.get_paginator('describe_db_instances')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            instances.extend([instance for instance in data.get('DBInstances', [])
                              if instance.get('Engine') == 'docdb'])

        return instances

    def _describe_snapshots(self):
        response = self.client.describe_db_cluster_snapshots()
        return [snapshot for snapshot in response.get('DBClusterSnapshots', []) if snapshot.get('Engine') == 'docdb']

        """
        CAN NOT operate paginated: describe_db_cluster_snapshot
        Need to check out why can't use it.
        """
        # snapshots = []
        # paginator = self.client.get_paginator('describe_db_cluster_snapshots')
        # response_iterator = paginator.paginate(
        #     PaginationConfig={
        #         'MaxItems': 10000,
        #         'PageSize': 50,
        #     }
        # )
        #
        # for data in response_iterator:
        #     snapshots.extend([snapshot for snapshot in data.get('DBClusterSnapshots', [])
        #                       if snapshot.get('Engine') == 'docdb'])
        # return snapshots

    @staticmethod
    def _match_instances(raw_instances, cluster_name):
        return [Instance(_ins, strict=False) for _ins in raw_instances if _ins['DBClusterIdentifier'] == cluster_name]

    @staticmethod
    def _match_snapshots(raw_snapshots, cluster_name):
        return [Snapshot(_ss, strict=False) for _ss in raw_snapshots if _ss['DBClusterIdentifier'] == cluster_name]

    def _match_subnet_group(self, subnet_group):
        for _sg in self._subnet_groups:
            if _sg.db_subnet_group_name == subnet_group:
                return _sg

        return None

    def _match_parameter_group(self, params_group):
        for _pg in self._parameter_groups:
            if _pg.db_cluster_parameter_group_name == params_group:
                return _pg

        return None
