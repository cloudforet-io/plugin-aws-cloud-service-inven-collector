import time
import logging
from typing import List

from spaceone.inventory.connector.aws_efs_connector.schema.data import FileSystem, MountTarget, LifecyclePolicy
from spaceone.inventory.connector.aws_efs_connector.schema.resource import FileSystemResource, FileSystemResponse
from spaceone.inventory.connector.aws_efs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EFSConnector(SchematicAWSConnector):
    service_name = 'efs'

    def get_resources(self) -> List[FileSystemResource]:
        print("** EFS START **")
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

        print(f' EFS Finished {time.time() - start_time} Seconds')
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
                res = FileSystem(raw, strict=False)
                yield res

    def describe_lifecycle_configuration(self, file_system_id):
        response = self.client.describe_lifecycle_configuration(FileSystemId=file_system_id)
        return list(map(lambda _lcpolicy: LifecyclePolicy(_lcpolicy, strict=False),
                        response.get('LifecyclePolicies', [])))

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