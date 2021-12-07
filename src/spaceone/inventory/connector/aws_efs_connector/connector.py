import time
import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_efs_connector.schema.data import FileSystem, MountTarget, LifecyclePolicy
from spaceone.inventory.connector.aws_efs_connector.schema.resource import FileSystemResource, FileSystemResponse
from spaceone.inventory.connector.aws_efs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EFSConnector(SchematicAWSConnector):
    service_name = 'efs'
    cloud_service_group = 'EFS'
    cloud_service_type = 'FileSystem'

    def get_resources(self) -> List[FileSystemResource]:
        _LOGGER.debug("[get_resources] START: EFS")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': FileSystemResource,
            'response_schema': FileSystemResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: EFS ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[FileSystem]:
        paginator = self.client.get_paginator('describe_file_systems')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('FileSystems', []):
                try:
                    size = raw.get('SizeInBytes', {})
                    raw.update({
                        'size': float(size.get('Value', 0.0)),
                        'life_cycle_policies': self.describe_lifecycle_configuration(raw['FileSystemId']),
                        'mount_targets': list(self.describe_mount_targets(raw['FileSystemId'])),
                        'account_id': self.account_id,
                        'arn': self.generate_arn(service="elasticfilesystem", region=region_name,
                                                 account_id=self.account_id, resource_type='file-system',
                                                 resource_id=raw['FileSystemId'])
                    })
                    filesystem_vo = FileSystem(raw, strict=False)

                    yield {
                        'data': filesystem_vo,
                        'name': filesystem_vo.name,
                        'instance_size': float(filesystem_vo.size),
                        'launched_at': datetime_to_iso8601(filesystem_vo.creation_time),
                        'account': self.account_id
                    }

                except Exception as e:
                    resource_id = raw.get('FileSystemId', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def describe_lifecycle_configuration(self, file_system_id):
        response = self.client.describe_lifecycle_configuration(FileSystemId=file_system_id)
        lifecycle_policies = response.get('LifecyclePolicies', [])

        for lifecycle_policy in lifecycle_policies:
            if lifecycle_policy.get('TransitionToIA'):
                lifecycle_policy.update({
                    'transition_to_ia_display':
                        f'{lifecycle_policy.get("TransitionToIA").split("_")[1]} days since last access'
                })

        return lifecycle_policies

    def describe_mount_targets(self, file_system_id):
        paginator = self.client.get_paginator('describe_mount_targets')
        response_iterator = paginator.paginate(
            FileSystemId=file_system_id,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('MountTargets', []):
                mtsg_response = self.client.describe_mount_target_security_groups(MountTargetId=raw['MountTargetId'])
                raw['security_groups'] = mtsg_response.get('SecurityGroups', [])
                yield MountTarget(raw, strict=False)