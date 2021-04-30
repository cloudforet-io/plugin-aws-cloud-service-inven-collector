import time
import logging
from typing import List

from spaceone.inventory.connector.aws_documentdb_connector.schema.data import Cluster, Instance, SubnetGroup, \
    ParameterGroup, Parameter, Snapshot, Tag
from spaceone.inventory.connector.aws_documentdb_connector.schema.resource import ClusterResource, ClusterResponse,\
    SubnetGroupResource, SubnetGroupResponse, ParameterGroupResource, ParameterGroupResponse
from spaceone.inventory.connector.aws_documentdb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)
EXCLUDE_REGION = ['us-west-1', 'ap-east-1', 'eu-north-1', 'me-south-1', 'sa-east-1', 'ap-northeast-3']


class DocumentDBConnector(SchematicAWSConnector):
    service_name = 'docdb'

    _parameter_groups = []
    _subnet_groups = []

    def get_resources(self):
        print("** DocumentDB START **")
        resources = []
        start_time = time.time()

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

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

        print(f' DocumentDB Finished {time.time() - start_time} Seconds')
        return resources

    def request_cluster_data(self, region_name, **kwargs) -> List[Cluster]:
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
                instances = self._match_instances(raw_instances, raw.get('DBClusterIdentifier'))
                raw.update({
                    'instances': instances,
                    'instance_count': len(instances),
                    'snapshots': self._match_snapshots(raw_snapshots, raw.get('DBClusterIdentifier')),
                    'subnet_group': self._match_subnet_group(raw.get('DBSubnetGroup')),
                    'parameter_group': self._match_parameter_group(raw.get('DBClusterParameterGroup')),
                    'account_id': self.account_id,
                    'tags': self.request_tags(raw['DBClusterArn'])
                })

                if subnet_group := self._match_subnet_group(raw.get('DBSubnetGroup')):
                    raw.update({'subnet_group': subnet_group})

                if parameter_group := self._match_parameter_group(raw.get('DBClusterParameterGroup')):
                    raw.update({'parameter_group': parameter_group})

                res = Cluster(raw, strict=False)
                yield res, res.db_cluster_identifier

    def request_subnet_group_data(self, region_name) -> List[SubnetGroup]:
        paginator = self.client.get_paginator('describe_db_subnet_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBSubnetGroups', []):
                raw.update({
                    'account_id': self.account_id,
                    'tags': self.request_tags(raw['DBSubnetGroupArn'])
                })
                res = SubnetGroup(raw, strict=False)
                yield res, res.db_subnet_group_name

    def request_parameter_group_data(self, region_name) -> List[ParameterGroup]:
        res_pgs = self.client.describe_db_cluster_parameter_groups()

        for pg_data in res_pgs.get('DBClusterParameterGroups', []):
            pg_data.update({
                'account_id': self.account_id,
                'parameters': self.request_parameter_data(pg_data['DBClusterParameterGroupName']),
                'tags': self.request_tags(pg_data['DBClusterParameterGroupArn'])
            })
            param_group = ParameterGroup(pg_data, strict=False)
            yield param_group, param_group.db_cluster_parameter_group_name

    def request_parameter_data(self, pg_name) -> List[Parameter]:
        res_params = self.client.describe_db_cluster_parameters(DBClusterParameterGroupName=pg_name)
        return list(map(lambda param: Parameter(param, strict=False), res_params.get('Parameters', [])))

    def request_tags(self, resource_arn):
        response = self.client.list_tags_for_resource(ResourceName=resource_arn)
        return list(map(lambda tag: Tag(tag, strict=False), response.get('TagList', [])))

    def _describe_instances(self):
        response = self.client.describe_db_instances(
            Filters=[{
                'Name': 'engine',
                'Values': ['docdb']
            }]
        )

        return response.get('DBInstances', [])

    def _describe_snapshots(self):
        response = self.client.describe_db_cluster_snapshots(
            Filters=[{
                'Name': 'engine',
                'Values': ['docdb']
            }]
        )

        return response.get('DBClusterSnapshots', [])

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
