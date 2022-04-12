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
    cloud_service_group = 'RDS'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: RDS")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.instance_request_data,
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

        resources.extend(self.set_service_code_in_cloud_service_type())

        for region_name in self.region_names:
            self.reset_region(region_name)

            try:
                # For Database
                for database_vo, resource, identifier in self.db_cluster_data(region_name):
                    if getattr(database_vo, 'resource_type', None) and database_vo.resource_type == 'inventory.ErrorResource':
                        # Error Resource
                        resources.append(database_vo)
                    else:
                        if getattr(database_vo, 'set_cloudwatch', None):
                            database_vo.cloudwatch = CloudWatchModel(database_vo.set_cloudwatch(region_name))

                        resources.append(DatabaseResponse(
                            {'resource': resource({
                                'name': identifier,
                                'data': database_vo,
                                'instance_type': database_vo.engine,
                                'tags': [{'key':tag.key, 'value': tag.value} for tag in database_vo.tags],
                                'region_code': region_name,
                                'account': self.account_id,
                                'reference': ReferenceModel(database_vo.reference(region_name))})}
                        ))
            except Exception as e:
                resource_id = ''
                resources.append(self.generate_error(region_name, resource_id, e))

            # For All except Database
            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: RDS ({time.time() - start_time} sec)')
        return resources

    def db_cluster_data(self, region_name) -> List[Database]:
        self.cloud_service_type = 'Database'

        # Cluster
        for cluster, cluster_identifier in self.describe_clusters(region_name):
            try:
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
                yield Database(db, strict=False), DBClusterResource, cluster_identifier
            except Exception as e:
                resource_id = cluster.db_cluster_arn
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response, '', ''

        # Instance Only
        for instance, instance_identifier in self.describe_instances(region_name):
            try:
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
                    yield Database(db, strict=False), DBInstanceResource, instance_identifier
            except Exception as e:
                resource_id = instance.db_instance_arn
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response, '', ''

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
                    yield res, res.db_cluster_identifier

    def instance_request_data(self, region_name) -> List[Instance]:
        self.cloud_service_type = 'Instance'

        for instance, instance_identifier in self.describe_instances(region_name):
            yield {
                'data': instance,
                'name': instance_identifier,
                'account': self.account_id
            }

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
                    yield Instance(raw, strict=False), raw.get('DBInstanceIdentifier', '')

    def snapshot_request_data(self, region_name) -> List[Snapshot]:
        self.cloud_service_type = 'Snapshot'

        paginator = self.client.get_paginator('describe_db_snapshots')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBSnapshots', []):
                try:
                    if raw.get('Engine') in DEFAULT_RDS_FILTER:
                        raw.update({
                            'region_name': region_name,
                            'account_id': self.account_id,
                            'tags': self.list_tags_for_resource(raw['DBSnapshotArn'])
                        })
                        snapshot_vo = Snapshot(raw, strict=False)
                        yield {
                            'data': snapshot_vo,
                            'name': snapshot_vo.db_snapshot_identifier,
                            'instance_type': snapshot_vo.engine,
                            'account': self.account_id
                        }

                except Exception as e:
                    resource_id = raw.get('DBSnapshotArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def subnet_group_request_data(self, region_name) -> List[SubnetGroup]:
        self.cloud_service_type = 'SubnetGroup'

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
                        'region_name': region_name,
                        'account_id': self.account_id,
                        'tags': self.list_tags_for_resource(raw['DBSubnetGroupArn'])
                    })
                    subnet_group_vo = SubnetGroup(raw, strict=False)
                    yield {
                        'data': subnet_group_vo,
                        'name': subnet_group_vo.db_subnet_group_name,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('DBSubnetGroupArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def parameter_group_request_data(self, region_name) -> List[ParameterGroup]:
        self.cloud_service_type = 'ParameterGroup'

        paginator = self.client.get_paginator('describe_db_parameter_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBParameterGroups', []):
                try:
                    raw.update({
                        'region_name': region_name,
                        'account_id': self.account_id,
                        'db_parameter_group_type': 'DbParameterGroup',
                        'parameters': list(self.describe_db_parameters(raw.get('DBParameterGroupName'))),
                        'tags': self.list_tags_for_resource(raw['DBParameterGroupArn'])
                    })
                    param_group_vo = ParameterGroup(raw, strict=False)
                    yield {
                        'data': param_group_vo,
                        'name': param_group_vo.db_parameter_group_name,
                        'instance_type': param_group_vo.db_parameter_group_family,
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('DBParameterGroupArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def option_group_request_data(self, region_name) -> List[OptionGroup]:
        self.cloud_service_type = 'OptionGroup'

        paginator = self.client.get_paginator('describe_option_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('OptionGroupsList', []):
                try:
                    raw.update({
                        'region_name': region_name,
                        'account_id': self.account_id,
                        'tags': self.list_tags_for_resource(raw['OptionGroupArn'])
                    })
                    option_group_vo = OptionGroup(raw, strict=False)
                    yield {
                        'data': option_group_vo,
                        'name': option_group_vo.option_group_name,
                        'instance_type': option_group_vo.engine_name,
                        'account': self.account_id
                    }
                    
                except Exception as e:
                    resource_id = raw.get('OptionGroupArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

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
