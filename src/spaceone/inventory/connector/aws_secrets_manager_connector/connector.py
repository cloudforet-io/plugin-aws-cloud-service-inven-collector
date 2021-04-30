import time
import logging
from typing import List

import boto3

from spaceone.inventory.connector.aws_secrets_manager_connector.schema.data import Secret
from spaceone.inventory.connector.aws_secrets_manager_connector.schema.resource import SecretResource, \
    SecretResponse
from spaceone.inventory.connector.aws_secrets_manager_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)


class SecretsManagerConnector(SchematicAWSConnector):
    service_name = 'secretsmanager'

    def get_resources(self) -> List[SecretResource]:
        print("** Secret Manager START **")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': SecretResource,
            'response_schema': SecretResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' Secret Manager Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[Secret]:
        paginator = self.client.get_paginator('list_secrets')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('SecretList', []):
                raw['region_name'] = region_name
                raw['account_id'] = self.account_id

                result = Secret(raw, strict=False)
                yield result, result.name
