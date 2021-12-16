import time
import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_ebs_connector.schema.data import Volume, Attribute, Snapshot
from spaceone.inventory.connector.aws_ebs_connector.schema.resource import VolumeResource, VolumeResponse, \
    SnapshotResource, SnapshotResponse
from spaceone.inventory.connector.aws_ebs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EBSConnector(SchematicAWSConnector):
    service_name = 'ec2'
    cloud_service_group = 'EC2'

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: EBS")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_volume_data,
                'resource': VolumeResource,
                'response_schema': VolumeResponse
            },
            {
                'request_method': self.request_snapshot_data,
                'resource': SnapshotResource,
                'response_schema': SnapshotResponse
            },
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: EBS ({time.time() - start_time} sec)')
        return resources

    def request_volume_data(self, region_name) -> List[Volume]:
        self.cloud_service_type = 'Volume'

        paginator = self.client.get_paginator('describe_volumes')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Volumes', []):
                try:
                    if name := self._get_name_from_tags(raw.get('Tags', [])):
                        raw['name'] = name

                    attr = self.client.describe_volume_attribute(Attribute='productCodes', VolumeId=raw['VolumeId'])
                    raw.update({
                        'attribute': Attribute(attr, strict=False),
                        'account_id': self.account_id,
                        'size': self.get_size_gb_to_bytes(raw.get('Size', 0)),
                        'arn': self.generate_arn(service=self.service_name, region=region_name,
                                                 account_id=self.account_id, resource_type="volume",
                                                 resource_id=raw.get('VolumeId'))
                    })

                    if kms_arn := raw.get('KmsKeyId'):
                        raw.update({
                            'kms_key_arn': kms_arn,
                            'kms_key_id': self._get_kms_key_id(kms_arn)
                        })

                    volume_vo = Volume(raw, strict=False)

                    yield {
                        'data': volume_vo,
                        'name': volume_vo.name,
                        'instance_size': float(volume_vo.size),
                        'instance_type': volume_vo.volume_type,
                        'launched_at': self.datetime_to_iso8601(volume_vo.create_time),
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('VolumeId', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_snapshot_data(self, region_name) -> List[Snapshot]:
        self.cloud_service_type = 'Snapshot'

        paginator = self.client.get_paginator('describe_snapshots')
        response_iterator = paginator.paginate(
            OwnerIds=[self.account_id],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Snapshots', []):
                try:
                    if name := self._get_name_from_tags(raw.get('Tags', [])):
                        raw['name'] = name

                    raw.update({
                        'account_id': self.account_id,
                        'arn': self.generate_arn(service=self.service_name, region=region_name,
                                                 account_id=self.account_id, resource_type="snapshot",
                                                 resource_id=raw.get('SnapshotId'))
                    })

                    if kms_arn := raw.get('KmsKeyId'):
                        raw.update({
                            'kms_key_arn': kms_arn,
                            'kms_key_id': self._get_kms_key_id(kms_arn)
                        })

                    snapshot_vo = Snapshot(raw, strict=False)
                    yield {
                        'data': snapshot_vo,
                        'name': snapshot_vo.name,
                        'instance_size': float(snapshot_vo.volume_size),
                        'launched_at': self.datetime_to_iso8601(snapshot_vo.start_time),
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('SnapshotId', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    @staticmethod
    def _get_name_from_tags(tags):
        for _tag in tags:
            if 'Name' in _tag.get('Key'):
                return _tag.get('Value')

        return None

    @staticmethod
    def _get_kms_key_id(kms_arn):
        try:
            return kms_arn.split('/')[1]
        except IndexError:
            return ''

    @staticmethod
    def get_size_gb_to_bytes(gb_size):
        return gb_size * 1024 * 1024 * 1024
