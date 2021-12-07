import time
import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_redshift_connector.schema.data import Cluster, Snapshot, SnapshotSchedule, \
    ScheduledAction, Tags
from spaceone.inventory.connector.aws_redshift_connector.schema.resource import ClusterResource, ClusterResponse
from spaceone.inventory.connector.aws_redshift_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)


class RedshiftConnector(SchematicAWSConnector):
    service_name = 'redshift'
    cloud_service_group = 'Redshift'
    cloud_service_type = 'Cluster'

    def get_resources(self) -> List[ClusterResource]:
        _LOGGER.debug("[get_resources] START: Redshift")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': ClusterResource,
            'response_schema': ClusterResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: Redshift ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Cluster]:
        paginator = self.client.get_paginator('describe_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('Clusters', []):
                try:
                    raw.update({
                        'region_name': region_name,
                        'account_id': self.account_id,
                        'arn': self.generate_arn(service=self.service_name, region=region_name,
                                                 account_id=self.account_id, resource_type='cluster',
                                                 resource_id=raw.get('ClusterIdentifier')),
                        'tags': list(self.describe_tags({"service": self.service_name,
                                                         "region": region_name,
                                                         "account_id": self.account_id,
                                                         "resource_id": raw.get('ClusterIdentifier', '')}))
                    })

                    cluster_vo = Cluster(raw, strict=False)
                    yield {
                        'data': cluster_vo,
                        'name': cluster_vo.cluster_identifier,
                        'instance_type': cluster_vo.node_type,
                        'launched_at': datetime_to_iso8601(cluster_vo.cluster_create_time),
                        'account': self.account_id
                    }
                    
                except Exception as e:
                    resource_id = raw.get('ClusterIdentifier', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def describe_tags(self, arn_vo):
        response = {}
        tag_arn = self._generate_redshift_arn(service=arn_vo.get('service', ''),
                                              region=arn_vo.get('region', ''),
                                              account_id=arn_vo.get('account_id', ''),
                                              resource_id=arn_vo.get('resource_id', ''))
        try:
            response = self.client.describe_tags(ResourceName=tag_arn)
        except Exception as e:
            pass

        for tag_resource in response.get('TaggedResources', []):
            yield Tags(tag_resource.get('Tag', {}), strict=False)

    @staticmethod
    def _generate_redshift_arn(service="", region="", account_id="", resource_id=""):
        return f'arn:aws:{service}:{region}:{account_id}:cluster:{resource_id}'