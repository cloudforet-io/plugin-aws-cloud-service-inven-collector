import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_msk_connector.schema.data import Cluster, Configuration
from spaceone.inventory.connector.aws_msk_connector.schema.resource import ClusterResource, ClusterResponse,\
    ConfigurationResource, ConfigurationResponse
from spaceone.inventory.connector.aws_msk_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)

PAGINATOR_MAX_ITEMS = 10000
PAGINATOR_PAGE_SIZE = 50
EXCLUDE_REGION = ['ap-northeast-3']


class MSKConnector(SchematicAWSConnector):
    service_name = 'kafka'
    cloud_service_group = 'MSK'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: MSK")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_cluster_data,
                'resource': ClusterResource,
                'response_schema': ClusterResponse
            },
            {
                'request_method': self.request_configuration_data,
                'resource': ConfigurationResource,
                'response_schema': ConfigurationResponse
            }
        ]

        resources.extend(self.set_service_code_in_cloud_service_type())

        for region_name in self.region_names:
            if region_name in EXCLUDE_REGION:
                continue
                
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: MSK ({time.time() - start_time} sec)')
        return resources

    def request_cluster_data(self, region_name) -> List[Cluster]:
        cloud_service_group = 'MSK'
        cloud_service_type = 'Cluster'
        cloudtrail_resource_type = 'AWS::MSK::Cluster'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('list_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('ClusterInfoList', []):
                try:
                    raw.update({
                        'tags': self.convert_tags(raw.get('Tags', {})),
                        'node_info_list': self.get_nodes(raw.get('ClusterArn')),
                        'cluster_operation_info': self.get_operation_cluster(raw.get('ClusterArn')),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['ClusterArn']),
                    })

                    cluster_vo = Cluster(raw, strict=False)
                    yield {
                        'data': cluster_vo,
                        'name': cluster_vo.cluster_name,
                        'launched_at': self.datetime_to_iso8601(cluster_vo.creation_time),
                        'account': self.account_id
                    }
                    
                except Exception as e:
                    resource_id = raw.get('ClusterArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_configuration_data(self, region_name) -> List[Configuration]:
        cloud_service_group = 'MSK'
        cloud_service_type = 'ClusterConfiguration'
        self.cloud_service_type = cloud_service_type
        cloudtrail_resource_type = 'AWS::MSK::Cluster'

        paginator = self.client.get_paginator('list_configurations')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50
            }
        )

        for data in response_iterator:
            for raw in data.get('Configurations'):
                try:
                    raw.update({
                        'revisions_configurations': self.get_revisions(raw.get('Arn')),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['Arn']),
                    })
                    configuration_vo = Configuration(raw, strict=False)
                    yield {
                        'data': configuration_vo,
                        'name': configuration_vo.name,
                        'account': self.account_id
                    }
                    
                except Exception as e:
                    resource_id = raw.get('Arn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def get_nodes(self, arn):
        node_response = self.client.list_nodes(ClusterArn=arn)
        node_info = node_response.get('NodeInfoList', [])
        return node_info

    def get_operation_cluster(self, arn):
        operation_response = self.client.list_cluster_operations(ClusterArn=arn)
        operation_info = operation_response.get('ClusterOperationInfoList', [])
        return operation_info

    def get_revisions(self, arn):
        revisions_response = self.client.list_configuration_revisions(Arn=arn)
        revisions_iter = revisions_response.get('Revisions', [])
        revision = []

        for data in revisions_iter:
            config = self.client.describe_configuration_revision(Arn=arn, Revision=data.get('Revision'))
            config.update({
                'ServerProperties': self.byte_to_list(config.get('ServerProperties'))
            })
            revision.append(config)

        return revision

    @staticmethod
    def byte_to_list(properties):
        decode_str = properties.decode("UTF-8")
        properties_list = decode_str.splitlines()
        return properties_list

    @staticmethod
    def convert_tags(tags):
        return [{'key': tag, 'value': tags[tag]} for tag in tags]








