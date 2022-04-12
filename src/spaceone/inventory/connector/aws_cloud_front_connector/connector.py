import time
import logging
from typing import List

from spaceone.inventory.connector.aws_cloud_front_connector.schema.data import DistributionData, Tags
from spaceone.inventory.connector.aws_cloud_front_connector.schema.resource import CloudFrontResponse,\
    DistributionResource
from spaceone.inventory.connector.aws_cloud_front_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel, CloudWatchModel

_LOGGER = logging.getLogger(__name__)


class CFConnector(SchematicAWSConnector):
    response_schema = CloudFrontResponse
    service_name = 'cloudfront'
    cloud_service_group = 'CloudFront'
    cloud_service_type = 'Distribution'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: Cloudfront")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        try:
            for data in self.request_data():
                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:
                    if getattr(data, 'set_cloudwatch', None):
                        data.cloudwatch = CloudWatchModel(data.set_cloudwatch())
    
                    resources.append(self.response_schema(
                        {'resource': DistributionResource({
                            'name': data.domain_name,
                            'data': data,
                            'account': self.account_id,
                            'reference': ReferenceModel(data.reference()),
                            'region_code': 'global'})
                        }))
        except Exception as e:
            resource_id = ''
            resources.append(self.generate_error('global', resource_id, e))

        _LOGGER.debug(f'[get_resources] Cloud Front Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self) -> List[DistributionData]:
        paginator = self.client.get_paginator('list_distributions')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DistributionList', {}).get('Items', []):
                try:
                    raw.update({
                        'state_display': self.get_state_display(raw.get('Enabled')),
                        'account_id': self.account_id,
                        'tags': list(self.list_tags_for_resource(raw.get('ARN')))
                    })
                    distribution_vo = DistributionData(raw, strict=False)
                    yield distribution_vo

                except Exception as e:
                    resource_id = raw.get('ARN', '')
                    error_resource_response = self.generate_error('global', resource_id, e)
                    yield error_resource_response

    def list_tags_for_resource(self, arn):
        response = self.client.list_tags_for_resource(Resource=arn)
        tags = response.get('Tags', {})
        for _tag in tags.get('Items', []):
            yield Tags(_tag, strict=False)

    @staticmethod
    def get_state_display(enabled):
        if enabled:
            return 'Enabled'
        else:
            return 'Disabled'
