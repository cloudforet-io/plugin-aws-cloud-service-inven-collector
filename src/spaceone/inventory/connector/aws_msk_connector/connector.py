import time
import logging
from typing import List
from spaceone.inventory.connector.aws_msk_connector.schema.data import Cluster, Configuration
from spaceone.inventory.connector.aws_msk_connector.schema.resource import MSKResource, ClusterResource, ClusterResponse,\
                                                                            ConfigurationResource, ConfigurationResponse
from spaceone.inventory.connector.aws_msk_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)

PAGINATOR_MAX_ITEMS = 10000
PAGINATOR_PAGE_SIZE = 50


class MSKConnector(SchematicAWSConnector):
    service_name = 'kafka'

    def get_resources(self):
        print("** Managed Streaming for Apache Kafka Start **")
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

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' Managed Streaming for Apache Kafka Finished {time.time() - start_time} Seconds')
        return resources

    def request_cluster_data(self, region_name) -> List[Cluster]:
        paginator = self.client.get_paginator('list_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('ClusterInfoList', []):
                raw.update({
                    'tags': self.convert_tags(raw.get('Tags',{})),
                    'node_info_list': self.get_nodes(raw.get('ClusterArn')),
                    'cluster_operation_info': self.get_operation_cluster(raw.get('ClusterArn'))
                })

                res = Cluster(raw, strict=False)
                yield res

    def request_configuration_data(self, region_name) -> List[Configuration]:
        paginator = self.client.get_paginator('list_configurations')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50
            }
        )

        for data in response_iterator:
            for raw in data.get('Configurations'):
                raw.update({
                    'revisions_configurations': self.get_revisions(raw.get('Arn'))
                })
                res = Configuration(raw, strict=False)
                yield res


    def get_nodes(self,arn):
        node_response = self.client.list_nodes(ClusterArn=arn)
        node_info = node_response.get('NodeInfoList', [])
        return node_info

    def get_operation_cluster(self,arn):
        operation_response = self.client.list_cluster_operations(ClusterArn=arn)
        operation_info = operation_response.get('ClusterOperationInfoList',[])
        return operation_info

    def get_revisions(self, arn):
        revisions_response = self.client.list_configuration_revisions(Arn=arn)
        revisions_iter = revisions_response.get('Revisions')
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
        properties_list = decode_str.split('\n')
        return properties_list

    @staticmethod
    def convert_tags(tags):
        return [{'key': tag, 'value': tags[tag]} for tag in tags]








