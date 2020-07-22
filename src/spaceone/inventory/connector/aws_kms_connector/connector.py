import time
import logging
from typing import List

from spaceone.inventory.connector.aws_kms_connector.schema.data import Key
from spaceone.inventory.connector.aws_kms_connector.schema.resource import KeyResource, KeyResponse
from spaceone.inventory.connector.aws_kms_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KMSConnector(SchematicAWSConnector):
    service_name = 'kms'

    def get_resources(self) -> List[KeyResource]:
        print("** KMS START **")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': KeyResource,
            'response_schema': KeyResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' KMS Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[Key]:
        kms_keys = self.list_keys()
        alias_list = self.list_aliases()

        for raw in kms_keys:
            response = self.client.describe_key(KeyId=raw.get('KeyId'))
            key = response.get('KeyMetadata')
            alias_info = next((alias for alias in alias_list if alias.get('TargetKeyId', '') == key.get('KeyId')), None)

            key.update({
                'key_type_path': self._set_key_type_path(key.get('KeyManager')),
                'region_name': region_name,
                'account_id': self.account_id
            })

            if alias_info is not None:
                key.update({
                    'alias_arn': alias_info['AliasArn'],
                    'alias_name': alias_info['AliasName']
                })

            res = Key(key, strict=False)
            yield res

    def list_keys(self):
        paginator = self.client.get_paginator('list_keys')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data['Keys']:
                yield raw

    def list_aliases(self):
        paginator = self.client.get_paginator('list_aliases')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data['Aliases']:
                yield raw

    @staticmethod
    def _set_key_type_path(key_manager):
        if key_manager == 'AWS':
            return 'defaultKeys'
        elif key_manager == 'CUSTOMER':
            return 'keys'
        else:
            return ''
