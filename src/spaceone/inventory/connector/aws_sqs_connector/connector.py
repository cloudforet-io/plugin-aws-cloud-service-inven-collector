import time
import logging
from typing import List
import json

from spaceone.inventory.connector.aws_sqs_connector.schema.data import QueData, RedrivePolicy
from spaceone.inventory.connector.aws_sqs_connector.schema.resource import SQSResponse, QueResource
from spaceone.inventory.connector.aws_sqs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class SQSConnector(SchematicAWSConnector):
    service_name = 'sqs'

    def get_resources(self) -> List[SQSResponse]:
        print("** SQS START **")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': QueResource,
            'response_schema': SQSResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' SQS Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[QueData]:
        resource = self.session.resource('sqs')

        for que in resource.queues.all():
            attr = que.attributes
            if 'RedrivePolicy' in attr:
                attr['RedrivePolicy'] = RedrivePolicy(json.loads(attr.get('RedrivePolicy')), strict=False)

            result = QueData(attr)
            result.region_name = region_name
            result.url = que.url
            result.account_id = self.account_id
            yield result, result.name()

