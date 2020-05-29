import logging
from typing import List

from spaceone.inventory.connector.aws_kms_connector.schema.data import Key
from spaceone.inventory.connector.aws_kms_connector.schema.resource import KeyResource, KeyResponse
from spaceone.inventory.connector.aws_kms_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class KMSConnector(SchematicAWSConnector):
    response_schema = KeyResponse
    service_name = 'kms'

    def get_resources(self) -> List[KeyResource]:
        print("** KMS START **")
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        for region_name in self.region_names:
            self.reset_region(region_name)

            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': KeyResource({'data': data,
                                              'reference': ReferenceModel(data.reference)})})

    def request_data(self, region_name) -> List[Key]:
        kms_keys = self.list_keys()
        alias_list = self.list_aliases()

        for raw in kms_keys:
            response = self.client.describe_key(KeyId=raw.get('KeyId'))
            key = response.get('KeyMetadata')
            alias_info = next((alias for alias in alias_list if alias.get('TargetKeyId', '') == key.get('KeyId')), None)

            key['key_type_path'] = self._set_key_type_path(key.get('KeyManager'))
            key['region_name'] = region_name
            key['account_id'] = self.account_id

            if alias_info is not None:
                key['alias_arn'] = alias_info['AliasArn']
                key['alias_name'] = alias_info['AliasName']

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
