import time
import logging
from typing import List

from spaceone.inventory.connector.aws_rds_connector.schema.data import Database, Snapshot, SubnetGroup, \
    ParameterGroup, Parameter, Cluster, Instance, OptionGroup
from spaceone.inventory.connector.aws_rds_connector.schema.resource import DatabaseResource, DatabaseResponse, \
    SnapshotResource, SnapshotResponse, SubnetGroupResource, SubnetGroupResponse, \
    ParameterGroupResource, ParameterGroupResponse, DBClusterResource, DBInstanceResource, OptionGroupResource, \
    OptionGroupResponse
from spaceone.inventory.connector.aws_rds_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)
RDS_FILTER = ['aurora', 'mysql', 'mariadb', 'postgres',
              'oracle-ee', 'oracle-se', 'oracle-se1', 'oracle-se2',
              'sqlserver-ex', 'sqlserver-web', 'sqlserver-se', 'sqlserver-ee']


class RDSConnector(SchematicAWSConnector):
    db_response_schema = DatabaseResponse
    ss_response_schema = SnapshotResponse
    sg_response_schema = SubnetGroupResponse
    pg_response_schema = ParameterGroupResponse
    og_response_schema = OptionGroupResponse

    service_name = 'rds'

    def get_resources(self):
        print("** RDS START **")
        start_time = time.time()

        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        for region_name in self.region_names:
            # print(f'[ {region_name} ]')
            self.reset_region(region_name)

            for data in self.db_cluster_data(region_name):
                yield self.db_response_schema(
                    {'resource': DBClusterResource({'data': data,
                                                    'reference': ReferenceModel(data.reference)})})

            for data in self.db_instance_data(region_name):
                yield self.db_response_schema(
                    {'resource': DBInstanceResource({'data': data,
                                                     'reference': ReferenceModel(data.reference)})})

            for data in self.snapshot_request_data(region_name):
                yield self.ss_response_schema(
                    {'resource': SnapshotResource({'data': data,
                                                   'reference': ReferenceModel(data.reference)})})

            for data in self.subnet_group_request_data(region_name):
                yield self.sg_response_schema(
                    {'resource': SubnetGroupResource({'data': data,
                                                      'reference': ReferenceModel(data.reference)})})

            for data in self.parameter_group_request_data(region_name):
                yield self.pg_response_schema(
                    {'resource': ParameterGroupResource({'data': data,
                                                         'reference': ReferenceModel(data.reference)})})

            for data in self.option_group_request_data(region_name):
                yield self.og_response_schema(
                    {'resource': OptionGroupResource({'data': data,
                                                      'reference': ReferenceModel(data.reference)})})

        print(f' RDS Finished {time.time() - start_time} Seconds')

    def db_instance_data(self, region_name) -> List[Database]:
        for instance in self.describe_instances():
            db = {
                'arn': instance.db_instance_arn,
                'db_identifier': instance.db_instance_identifier,
                'status': instance.db_instance_status,
                'role': 'instance',
                'engine': instance.engine,
                'region_name': region_name,
                'availability_zone': instance.availability_zone,
                'size': instance.db_instance_class,
                'multi_az': instance.multi_az,
                'account_id': self.account_id,
                'instance': Instance(instance, strict=False),
            }
            yield Database(db, strict=False)

    def db_cluster_data(self, region_name) -> List[Database]:
        for cluster in self.describe_clusters():
            db = {
                'arn': cluster.db_cluster_arn,
                'db_identifier': cluster.db_cluster_identifier,
                'status': cluster.status,
                'role': 'cluster',
                'engine': cluster.engine,
                'region_name': region_name,
                'availability_zone': self.get_region(cluster.availability_zones),
                'size': f'{len(cluster.db_cluster_members)} instances',
                'multi_az': cluster.multi_az,
                'account_id': self.account_id,
                'cluster': Cluster(cluster, strict=False),
            }
            yield Database(db, strict=False)

    def describe_clusters(self) -> List[Cluster]:
        paginator = self.client.get_paginator('describe_db_clusters')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'engine',
                    'Values': RDS_FILTER
                },
            ],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBClusters', []):
                raw.update({
                    'db_cluster_role': 'Master',
                    'tags': self.list_tags_for_resource(raw['DBClusterArn'])
                })
                res = Cluster(raw, strict=False)
                yield res

    def describe_instances(self) -> List[Instance]:
        paginator = self.client.get_paginator('describe_db_instances')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'engine',
                    'Values': RDS_FILTER
                },
            ],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBInstances', []):
                raw.update({
                    'tags': self.list_tags_for_resource(raw['DBInstanceArn'])
                })
                yield Instance(raw, strict=False)

    def snapshot_request_data(self, region_name) -> List[Snapshot]:
        paginator = self.client.get_paginator('describe_db_snapshots')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'engine',
                    'Values': RDS_FILTER
                },
            ],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBSnapshots', []):
                raw.update({
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'tags': self.list_tags_for_resource(raw['DBSnapshotArn'])
                })
                yield Snapshot(raw, strict=False)

    def subnet_group_request_data(self, region_name) -> List[SubnetGroup]:
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
                    'tags': self.list_tags_for_resource(raw['DBSubnetGroupArn'])
                })
                yield SubnetGroup(raw, strict=False)

    def parameter_group_request_data(self, region_name) -> List[ParameterGroup]:
        paginator = self.client.get_paginator('describe_db_parameter_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBParameterGroups', []):
                raw.update({
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'db_parameter_group_type': 'DbParameterGroup',
                    'parameters': list(self.describe_db_parameters(raw.get('DBParameterGroupName'))),
                    'tags': self.list_tags_for_resource(raw['DBParameterGroupArn'])
                })
                yield ParameterGroup(raw, strict=False)

    def option_group_request_data(self, region_name) -> List[OptionGroup]:
        paginator = self.client.get_paginator('describe_option_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('OptionGroupsList', []):
                raw.update({
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'tags': self.list_tags_for_resource(raw['OptionGroupArn'])
                })
                yield OptionGroup(raw, strict=False)

    def describe_db_parameters(self, db_parameter_group_name) -> List[Parameter]:
        paginator = self.client.get_paginator('describe_db_parameters')
        response_iterator = paginator.paginate(
            DBParameterGroupName=db_parameter_group_name,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('Parameters', []):
                yield Parameter(raw, strict=False)

    def list_tags_for_resource(self, resource_name):
        response = self.client.list_tags_for_resource(ResourceName=resource_name)
        return response.get('TagList', [])

    @staticmethod
    def get_region(azs):
        if len(azs) > 0:
            return azs[0][:-1]

        return None


