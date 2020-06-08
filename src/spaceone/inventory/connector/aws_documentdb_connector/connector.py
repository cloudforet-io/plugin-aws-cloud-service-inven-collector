import time
import logging
from typing import List

from spaceone.inventory.connector.aws_documentdb_connector.schema.data import Cluster, Instance, SubnetGroup, \
    ParameterGroup, Parameter, Snapshot, Tag
from spaceone.inventory.connector.aws_documentdb_connector.schema.resource import ClusterResource, ClusterResponse,\
    SubnetGroupResource, SubnetGroupResponse, ParameterGroupResource, ParameterGroupResponse
from spaceone.inventory.connector.aws_documentdb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)
EXCLUDE_REGION = ['us-west-1', 'ap-east-1', 'eu-north-1', 'me-south-1', 'sa-east-1']


class DocumentDBConnector(SchematicAWSConnector):
    cluster_response_schema = ClusterResponse
    subnet_group_response_schema = SubnetGroupResponse
    parameter_group_response_schema = ParameterGroupResponse

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

            # request parameter group
            for data in self.request_parameter_group_data(region_name):
                self._parameter_groups.append(data)
                resources.append(self.parameter_group_response_schema(
                    {'resource': ParameterGroupResource({'data': data,
                                                         'reference': ReferenceModel(data.reference)})}))

            # request subnet group
            for data in self.request_subnet_group_data(region_name):
                self._subnet_groups.append(data)
                resources.append(self.subnet_group_response_schema(
                    {'resource': SubnetGroupResource({'data': data,
                                                      'reference': ReferenceModel(data.reference)})}))

            raw_instances = self._describe_instances()
            raw_snapshots = self._describe_snapshots()

            # request cluster
            for data in self.request_cluster_data(raw_instances, raw_snapshots, region_name):
                resources.append(self.cluster_response_schema(
                    {'resource': ClusterResource({'data': data,
                                                  'reference': ReferenceModel(data.reference)})}))

        print(f' DocumentDB Finished {time.time() - start_time} Seconds')
        return resources

    def request_cluster_data(self, raw_instances, raw_snapshots, region_name) -> List[Cluster]:
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
                raw.update({
                    'instances': self._match_instances(raw_instances, raw.get('DBClusterIdentifier')),
                    'snapshots': self._match_snapshots(raw_snapshots, raw.get('DBClusterIdentifier')),
                    'subnet_group': self._match_subnet_group(raw.get('DBSubnetGroup')),
                    'parameter_group': self._match_parameter_group(raw.get('DBClusterParameterGroup')),
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'tags': self.request_tags(raw['DBClusterArn'])
                })

                if subnet_group := self._match_subnet_group(raw.get('DBSubnetGroup')):
                    raw.update({'subnet_group': subnet_group})

                if parameter_group := self._match_parameter_group(raw.get('DBClusterParameterGroup')):
                    raw.update({'parameter_group': parameter_group})

                res = Cluster(raw, strict=False)
                yield res

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
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'tags': self.request_tags(raw['DBSubnetGroupArn'])
                })
                res = SubnetGroup(raw, strict=False)
                yield res

    def request_parameter_group_data(self, region_name) -> List[ParameterGroup]:
        res_pgs = self.client.describe_db_cluster_parameter_groups()

        for pg_data in res_pgs.get('DBClusterParameterGroups', []):
            pg_data.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'parameters': self.request_parameter_data(pg_data['DBClusterParameterGroupName']),
                'tags': self.request_tags(pg_data['DBClusterParameterGroupArn'])
            })
            param_group = ParameterGroup(pg_data, strict=False)
            yield param_group

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
