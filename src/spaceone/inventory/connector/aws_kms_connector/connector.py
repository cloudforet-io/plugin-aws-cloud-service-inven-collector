import time
import logging

from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_kms_connector.schema.data import Key
from spaceone.inventory.connector.aws_kms_connector.schema.resource import KeyResource, KeyResponse
from spaceone.inventory.connector.aws_kms_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KMSConnector(SchematicAWSConnector):
    service_name = 'kms'
    cloud_service_group = 'KMS'
    cloud_service_type = 'Key'

    def get_resources(self) -> List[KeyResource]:
        _LOGGER.debug("[get_resources] START: KMS")
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

        _LOGGER.debug(f'[get_resources] FINISHED: KMS ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Key]:
        kms_keys = self.list_keys()
        alias_list = self.list_aliases()

        for raw in kms_keys:
            try:
                response = self.client.describe_key(KeyId=raw.get('KeyId'))
                key = response.get('KeyMetadata')
                alias_info = next((alias for alias in alias_list if alias.get('TargetKeyId', '') == key.get('KeyId')), None)

                key.update({
                    'key_type_path': self._set_key_type_path(key.get('KeyManager')),
                    'region_name': region_name,
                    'account_id': self.account_id,
                    'key_rotated': self._set_key_rotated(key.get('KeyId'), key.get('KeyManager'))
                })

                if alias_info is not None:
                    key.update({
                        'alias_arn': alias_info['AliasArn'],
                        'alias_name': alias_info['AliasName']
                    })

                key_vo = Key(key, strict=False)
                yield {
                    'data': key_vo,
                    'name': key_vo.alias_name,
                    'launched_at': self.datetime_to_iso8601(key_vo.creation_date),
                    'account': self.account_id
                }

            except Exception as e:
                resource_id = raw.get('KeyId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

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

    def _set_key_rotated(self, key_id, key_manager):
        rot = False
        if key_manager == 'CUSTOMER':
            status = self.client.get_key_rotation_status(KeyId=key_id)
            rot = status.get('KeyRotationEnabled', False)

        return rot
