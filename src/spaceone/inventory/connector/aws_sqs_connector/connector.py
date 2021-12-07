import time
import logging
from typing import List
import json

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_sqs_connector.schema.data import QueData, RedrivePolicy
from spaceone.inventory.connector.aws_sqs_connector.schema.resource import SQSResponse, QueResource
from spaceone.inventory.connector.aws_sqs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class SQSConnector(SchematicAWSConnector):
    service_name = 'sqs'
    cloud_service_group = 'SQS'
    cloud_service_type = 'Queue'

    def get_resources(self) -> List[SQSResponse]:
        _LOGGER.debug("[get_resources] START: SQS")
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

        _LOGGER.debug(f'[get_resources] FINISHED: SQS ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[QueData]:
        resource = self.session.resource('sqs')

        for que in resource.queues.all():
            try:
                attr = que.attributes
                if 'RedrivePolicy' in attr:
                    attr['RedrivePolicy'] = RedrivePolicy(json.loads(attr.get('RedrivePolicy')), strict=False)

                result = QueData(attr)
                result.region_name = region_name
                result.url = que.url
                result.account_id = self.account_id
                yield {
                    'data': result,
                    'name': result.name,
                    'launched_at': datetime_to_iso8601(result.created_timestamp),
                    'account': self.account_id
                }
                
            except Exception as e:
                resource_id = ''
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}
