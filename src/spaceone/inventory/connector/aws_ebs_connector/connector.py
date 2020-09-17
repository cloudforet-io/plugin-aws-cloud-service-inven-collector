import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ebs_connector.schema.data import Volume, Attribute, Snapshot
from spaceone.inventory.connector.aws_ebs_connector.schema.resource import VolumeResource, VolumeResponse, \
    SnapshotResource, SnapshotResponse
from spaceone.inventory.connector.aws_ebs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EBSConnector(SchematicAWSConnector):
    service_name = 'ec2'

    def get_resources(self):
        print("** EBS START **")
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

        print(f' EBS Finished {time.time() - start_time} Seconds')
        return resources

    def request_volume_data(self, region_name) -> List[Volume]:
        paginator = self.client.get_paginator('describe_volumes')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Volumes', []):
                if name := self._get_name_from_tags(raw.get('Tags', [])):
                    raw['name'] = name

                attr = self.client.describe_volume_attribute(Attribute='productCodes', VolumeId=raw['VolumeId'])
                raw.update({
                    'attribute': Attribute(attr, strict=False),
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.service_name, region=region_name,
                                             account_id=self.account_id, resource_type="volume",
                                             resource_id=raw.get('VolumeId'))
                })

                if kms_arn := raw.get('KmsKeyId'):
                    raw.update({
                        'kms_key_arn': kms_arn,
                        'kms_key_id': self._get_kms_key_id(kms_arn)
                    })

                yield Volume(raw, strict=False)

    def request_snapshot_data(self, region_name) -> List[Snapshot]:
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

                yield Snapshot(raw, strict=False)

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

