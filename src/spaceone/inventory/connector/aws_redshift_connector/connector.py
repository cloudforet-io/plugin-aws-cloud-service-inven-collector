import time
import logging
from typing import List

from spaceone.inventory.connector.aws_redshift_connector.schema.data import Cluster, Snapshot, SnapshotSchedule, \
    ScheduledAction, Tags
from spaceone.inventory.connector.aws_redshift_connector.schema.resource import ClusterResource, ClusterResponse
from spaceone.inventory.connector.aws_redshift_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class RedshiftConnector(SchematicAWSConnector):
    response_schema = ClusterResponse
    service_name = 'redshift'

    def get_resources(self) -> List[ClusterResource]:
        print("** Redshift START **")
        start_time = time.time()
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': ClusterResource({'data': data,
                                                  'reference': ReferenceModel(data.reference)})})

        print(f' Redshift Finished {time.time() - start_time} Seconds')

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
                raw.update({
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.service_name, region=region_name,
                                             account_id=self.account_id, resource_type='cluster',
                                             resource_id=raw.get('ClusterIdentifier')),
                    'tags': list(self.describe_tags(raw.get('Cluster')))
                })

                res = Cluster(raw, strict=False)
                yield res

    def describe_tags(self, resource_name, resource_type):
        response = self.client.describe_tags(ResourceName=resource_name, ResourceType=resource_type)

        for tag_resource in response.get('TaggedResources', []):
            yield Tags(tag_resource.get('Tag', {}), strict=False)
