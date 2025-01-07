import logging
from typing import List
from spaceone.core.utils import *
from spaceone.inventory.connector.aws_sqs_connector.schema.data import QueData, RedrivePolicy
from spaceone.inventory.connector.aws_sqs_connector.schema.resource import SQSResponse, QueResource
from spaceone.inventory.connector.aws_sqs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class SQSConnector(SchematicAWSConnector):
    service_name = 'sqs'
    cloud_service_group = 'SQS'
    cloud_service_type = 'Queue'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[SQSResponse]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: SQS")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': QueResource,
            'response_schema': SQSResponse
        }

        resources.extend(self.set_cloud_service_types())

        # merge data
        for region_name in self.region_names:
            try:
                self.reset_region(region_name)
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))
            except Exception as e:
                error_resource_response = self.generate_error(region_name, '', e)
                resources.append(error_resource_response)

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: SQS ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[QueData]:
        cloudwatch_namespace = 'AWS/SQS'
        cloudwatch_dimension_name = 'QueueName'
        cloudtrail_resource_type = 'AWS::SQS::Queue'
        resource = self.session.resource('sqs', verify=BOTO3_HTTPS_VERIFIED)

        for que in resource.queues.all():
            try:
                attr = que.attributes
                if 'RedrivePolicy' in attr:
                    attr['RedrivePolicy'] = RedrivePolicy(json.loads(attr.get('RedrivePolicy')), strict=False)

                result = QueData(attr)
                result.region_name = region_name
                result.url = que.url
                result.cloudwatch = self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                        result.name, region_name)
                result.cloudtrail = self.set_cloudtrail(region_name, cloudtrail_resource_type, result.url)

                yield {
                    'data': result,
                    'name': result.name,
                    'launched_at': self.datetime_to_iso8601(result.created_timestamp),
                    'account': self.account_id
                }
                
            except Exception as e:
                resource_id = ''
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}
