import time
import logging
from typing import List

from spaceone.inventory.connector.aws_cloud_front_connector.schema.data import DistributionData, Tags
from spaceone.inventory.connector.aws_cloud_front_connector.schema.resource import CloudFrontResponse,DistributionResource
from spaceone.inventory.connector.aws_cloud_front_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class CFConnector(SchematicAWSConnector):
    response_schema = CloudFrontResponse
    service_name = 'cloudfront'

    def get_resources(self) -> List[DistributionResource]:
        print("** Cloud Front START **")
        start_time = time.time()

        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for data in self.request_data():
            # print(f"[ CloudFront DATA ]")
            yield self.response_schema(
                {'resource': DistributionResource({'data': data,
                                                   'reference': ReferenceModel(data.reference)})})

        print(f' Cloud Front Finished {time.time() - start_time} Seconds')

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

