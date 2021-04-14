import time
import logging
from typing import List

from spaceone.inventory.connector.aws_rds_connector.schema.data import Database, Snapshot, SubnetGroup, \
    ParameterGroup, Parameter, Cluster, Instance, OptionGroup
from spaceone.inventory.connector.aws_rds_connector.schema.resource import DatabaseResource, DatabaseResponse, \
    SnapshotResource, SnapshotResponse, SubnetGroupResource, SubnetGroupResponse, ParameterGroupResource, \
    ParameterGroupResponse, OptionGroupResource, OptionGroupResponse, InstanceResource, InstanceResponse, \
    DBClusterResource, DBInstanceResource
from spaceone.inventory.connector.aws_rds_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel, CloudWatchModel


_LOGGER = logging.getLogger(__name__)
DEFAULT_RDS_FILTER = ['aurora', 'aurora-mysql', 'mysql', 'mariadb', 'postgres',
                      'oracle-ee', 'oracle-se1', 'oracle-se2', 'oracle-se',
                      'sqlserver-ex', 'sqlserver-web', 'sqlserver-se', 'sqlserver-ee']


class RDSConnector(SchematicAWSConnector):
    service_name = 'rds'

    def get_resources(self):
        print("** RDS START **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.instance_data,
                'resource': InstanceResource,
                'response_schema': InstanceResponse
            },
            {
                'request_method': self.snapshot_request_data,
                'resource': SnapshotResource,
                'response_schema': SnapshotResponse
            },
            {
                'request_method': self.subnet_group_request_data,
                'resource': SubnetGroupResource,
                'response_schema': SubnetGroupResponse
            },
            {
                'request_method': self.parameter_group_request_data,
                'resource': ParameterGroupResource,
                'response_schema': ParameterGroupResponse
            },
            {
                'request_method': self.option_group_request_data,
                'resource': OptionGroupResource,
                'response_schema': OptionGroupResponse
            }
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ {region_name} ]')
            self.reset_region(region_name)

            try:
                # For Database
                for database_vo, resource in self.db_cluster_data(region_name):
                    if getattr(database_vo, 'set_cloudwatch', None):
                        database_vo.cloudwatch = CloudWatchModel(database_vo.set_cloudwatch(region_name))

                    resources.append(DatabaseResponse(
                        {'resource': resource(
                            {'data': database_vo,
                             'tags': [{'key':tag.key, 'value': tag.value} for tag in database_vo.tags],
                             'region_code': region_name,
                             'reference': ReferenceModel(database_vo.reference(region_name))})}
                    ))
            except Exception as e:
                print(f'[ERROR RDS] REGION : {region_name} {e}')

            # For All except Database
            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))
        print(f' RDS Finished {time.time() - start_time} Seconds')
        return resources

    def db_cluster_data(self, region_name) -> List[Database]:
        # Cluster
        for cluster in self.describe_clusters(region_name):
            db = {
                'arn': cluster.db_cluster_arn,
                'db_identifier': cluster.db_cluster_identifier,
                'status': cluster.status,
                'role': 'cluster',
                'engine': cluster.engine,
                'availability_zone': self.get_region(cluster.availability_zones),
                'size': f'{len(cluster.db_cluster_members)} instances',
                'multi_az': cluster.multi_az,
                'account_id': self.account_id,
                'cluster': cluster,
                'tags': cluster.tags
            }

            yield Database(db, strict=False), DBClusterResource

        # Instance Only
        for instance in self.describe_instances(region_name):
            if not instance.db_cluster_identifier:
                db = {
                    'arn': instance.db_instance_arn,
                    'db_identifier': instance.db_instance_identifier,
                    'status': instance.db_instance_status,
                    'role': 'instance',
                    'engine': instance.engine,
                    'availability_zone': instance.availability_zone,
                    'size': instance.db_instance_class,
                    'multi_az': instance.multi_az,
                    'account_id': self.account_id,
                    'instance': instance,
                    'tags': instance.tags
                }
                yield Database(db, strict=False), DBInstanceResource

    def describe_clusters(self, region_name) -> List[Cluster]:
        paginator = self.client.get_paginator('describe_db_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('DBClusters', []):
                if raw.get('Engine') in DEFAULT_RDS_FILTER:
                    raw.update({
                        'db_cluster_role': 'Master',
                        'tags': self.list_tags_for_resource(raw['DBClusterArn'])
                    })
                    res = Cluster(raw, strict=False)
                    yield res

    def instance_data(self, region_name) -> List[Instance]:
        for instance in self.describe_instances(region_name):
            yield instance

    def describe_instances(self, region_name) -> List[Instance]:
        paginator = self.client.get_paginator('describe_db_instances')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBInstances', []):
                if raw.get('Engine') in DEFAULT_RDS_FILTER:
                    raw.update({
                        'tags': self.list_tags_for_resource(raw['DBInstanceArn'])
                    })
                    yield Instance(raw, strict=False)

    def snapshot_request_data(self, region_name) -> List[Snapshot]:
        paginator = self.client.get_paginator('describe_db_snapshots')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBSnapshots', []):
                if raw.get('Engine') in DEFAULT_RDS_FILTER:
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
        if azs:
            return azs[0][:-1]

        return None
