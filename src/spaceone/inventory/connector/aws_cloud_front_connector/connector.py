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

    def get_resources(self):
        print("** Cloud Front START **")
        resources = []
        start_time = time.time()

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        try:
            for data in self.request_data():
                # print(f"[ CloudFront DATA ]")
                if getattr(data, 'set_cloudwatch', None):
                    data.cloudwatch = CloudWatchModel(data.set_cloudwatch())

                resources.append(self.response_schema(
                    {'resource': DistributionResource({'data': data,
                                                       'reference': ReferenceModel(data.reference()),
                                                       'region_code': 'global'})}))
        except Exception as e:
            print(f'[ERROR {self.service_name}] {e}')

        print(f' Cloud Front Finished {time.time() - start_time} Seconds')
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
                raw.update({
                    'state_display': self.get_state_display(raw.get('enabled')),
                    'account_id': self.account_id,
                    'tags': list(self.list_tags_for_resource(raw.get('ARN')))
                })
                res = DistributionData(raw, strict=False)
                yield res

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
