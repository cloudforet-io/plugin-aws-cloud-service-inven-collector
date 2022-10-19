import time
import logging
from typing import List

from spaceone.inventory.connector.aws_dynamodb_connector.schema.data import Table, TimeToLive, \
    ContinuousBackup, ContributorInsight
from spaceone.inventory.connector.aws_dynamodb_connector.schema.resource import TableResource, TableResponse
from spaceone.inventory.connector.aws_dynamodb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)


class DynamoDBConnector(SchematicAWSConnector):
    service_name = 'dynamodb'
    cloud_service_group = 'DynamoDB'
    cloud_service_type = 'Table'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[TableResource]:
        resources = []
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: DynamoDB")
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': TableResource,
            'response_schema': TableResponse
        }

        resources.extend(self.set_service_code_in_cloud_service_type())

        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: DynamoDB ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Table]:
        _auto_scaling_policies = None
        cloudwatch_namespace = 'AWS/DynamoDB'
        cloudwatch_dimension_name = 'TableName'
        cloudtrail_resource_type = 'AWS::DynamoDB::Table'

        paginator = self.client.get_paginator('list_tables')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for table_name in data.get('TableNames', []):
                try:
                    table = {}
                    response = self.client.describe_table(TableName=table_name)
                    table = response.get('Table')

                    partition_key, sort_key = self._get_key_info(table.get('KeySchema', []),
                                                                 table.get('AttributeDefinitions', []))

                    index_count, total_read_capacity, total_write_capacity = self._get_index_info(table.get('GlobalSecondaryIndexes', []))

                    if _auto_scaling_policies is None:
                        _auto_scaling_policies = self.describe_scaling_policies()

                    table.update({
                        'partition_key_display': partition_key,
                        'sort_key_display': sort_key,
                        'auto_scaling_policies': self._get_auto_scaling(_auto_scaling_policies, table_name),
                        'encryption_type': self._get_encryption_type(table.get('SSEDescription', {})),
                        'index_count': index_count,
                        'total_read_capacity': total_read_capacity,
                        'total_write_capacity': total_write_capacity,
                        'time_to_live': self._get_time_to_live(table_name),
                        'continuous_backup': self._get_continuous_backup(table_name),
                        'contributor_insight': self._get_contributor_insights(table_name),
                        'cloudwatch': self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                          table['TableName'], region_name),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, table['TableName']),
                    })
                    table_vo = Table(table, strict=False)

                    yield {
                        'data': table_vo,
                        'name': table_vo.table_name,
                        'instance_size': float(table_vo.table_size_bytes),
                        'account': self.account_id,
                        'tags': self.request_tags(table_vo.table_arn)
                    }

                except Exception as e:
                    resource_id = table.get('TableArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def _get_contributor_insights(self, table_name):
        response = self.client.describe_contributor_insights(TableName=table_name)
        del response['ResponseMetadata']

        return ContributorInsight(response, strict=False)

    def _get_continuous_backup(self, table_name):
        response = self.client.describe_continuous_backups(TableName=table_name)
        return ContinuousBackup(response.get('ContinuousBackupsDescription'), strict=False)

    def _get_time_to_live(self, table_name):
        response = self.client.describe_time_to_live(TableName=table_name)
        return TimeToLive(response.get('TimeToLiveDescription'), strict=False)

    def describe_scaling_policies(self):
        auto_scaling_client = self.session.client('application-autoscaling')
        response = auto_scaling_client.describe_scaling_policies(ServiceNamespace='dynamodb')
        return response.get('ScalingPolicies', [])

    def _get_key_info(self, keys, key_attrs):
        partition_key = ''
        sort_key = ''

        for key in keys:
            if partition_key == '':
                partition_key = self._search_key(key, 'HASH', key_attrs)
            if sort_key == '':
                sort_key = self._search_key(key, 'RANGE', key_attrs)

        return partition_key, sort_key

    @staticmethod
    def _get_auto_scaling(as_policies, table_name):
        auto_scalings = []

        for asp in as_policies:
            if asp.get('ResourceId') == f'table/{table_name}':
                if 'ReadCapacityUnits' in asp.get('ScalableDimension'):
                    auto_scalings.append('READ')
                if 'WriteCapacityUnits' in asp.get('ScalableDimension'):
                    auto_scalings.append('WRITE')

        return auto_scalings

    @staticmethod
    def _get_index_info(indexes):
        read_count = 0
        write_count = 0

        for _index in indexes:
            provisioned_throughput = _index.get('ProvisionedThroughput', {})

            if 'ReadCapacityUnits' in provisioned_throughput:
                read_count = read_count + provisioned_throughput.get('ReadCapacityUnits')

            if 'WriteCapacityUnits' in provisioned_throughput:
                write_count = write_count + provisioned_throughput.get('WriteCapacityUnits')

        return len(indexes), read_count, write_count

    @staticmethod
    def _get_encryption_type(sse_description):
        if sse_type := sse_description.get('SSEType'):
            return sse_type
        else:
            return 'DEFAULT'

    @staticmethod
    def _search_key(key, key_type, key_attrs):
        match_key_attr = {
            'S': 'String',
            'N': 'Number',
            'B': 'Binary'
        }

        if key.get('KeyType') == key_type:
            key_name = key.get('AttributeName', '')

            for attr in key_attrs:
                if key_name == attr.get('AttributeName'):
                    if attr.get('AttributeType') in match_key_attr:
                        return f'{key_name} ({match_key_attr.get(attr.get("AttributeType"))})'

    def request_tags(self, resource_arn):
        response = self.client.list_tags_of_resource(ResourceArn=resource_arn)
        return self.convert_tags_to_dict_type(response.get('Tags', []))

