import logging
from typing import List

from spaceone.inventory.connector.aws_directory_service_connector.schema.resource import (
    DirectoryResource, DirectoryResponse,
    SharedDirectoryResource, SharedDirectoryResponse
)
from spaceone.inventory.connector.aws_directory_service_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.connector.aws_directory_service_connector.schema.data import (
    Directory, SharedDirectory, VpcSettings
)
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)

PRE_SHARED_STATUES = {
    "PendingAcceptance",
    "Rejected",
    "Rejecting",
    "RejectedFailed",
    "ShareFailed",
}
class DirectoryServiceConnector(SchematicAWSConnector):
    service_name = "ds"
    cloud_service_group = "DirectoryService"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Directory Service")

        import time
        start_time = time.time()

        # 최종 리소스 리스트
        resources = []

        directory_resources = []
        shared_resources = []

        resources.extend(self.set_cloud_service_types())

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)

                owner_directory_ids: List[str] = []


                for directory_result in self.request_directory_list(region_name):

                    if directory_result.get("resource_type") == "inventory.ErrorResource":
                        resources.append(directory_result)
                        continue

                    vo = directory_result["data"]
                    # SharedMicrosoftAD → DirectoryResponse 에 포함 안하게끔
                    if vo.type == "SharedMicrosoftAD":

                        # OwnerDirectoryId 수집
                        owner_desc = getattr(vo, "OwnerDirectoryDescription", None)
                        if owner_desc:
                            owner_id = owner_desc.get("DirectoryId")
                            if owner_id:
                                owner_directory_ids.append(owner_id)

                        # 아직 Shared 상태가 아닌 데이터들도 shared with me에 추가
                        if vo.share_status in PRE_SHARED_STATUES:
                            pre_shared = self.create_pre_shared_directory(vo, directory_result)
                            if pre_shared:
                                shared_resources.append(
                                    SharedDirectoryResponse({
                                        "resource": SharedDirectoryResource(pre_shared)
                                    })
                                )
                        continue

                    # SharedMicrosoftAD 외 디렉토리 → DirectoryResponse
                    directory_resources.append(
                        DirectoryResponse({
                            "resource": DirectoryResource({
                                "name": directory_result["name"],
                                "account": directory_result["account"],
                                "region_code": directory_result["region_code"],
                                "data": vo,
                                "reference": directory_result["reference"],
                                "tags": {}
                            })
                        })
                    )

                for shared_result in self.request_shared_directory_data(region_name, owner_directory_ids):

                    if shared_result.get("resource_type") == "inventory.ErrorResource":
                        resources.append(shared_result)
                        continue

                    vo = shared_result["data"]

                    shared_resources.append(
                        SharedDirectoryResponse({
                            "resource": SharedDirectoryResource({
                                "name": shared_result["name"],
                                "account": shared_result["account"],
                                "region_code": shared_result["region_code"],
                                "data": vo,
                                "reference": shared_result["reference"],
                                "tags": {}
                            })
                        })
                    )

            except Exception as e:
                resources.append(self.generate_error(self.service_name, "", e))


        resources.extend(directory_resources)
        resources.extend(shared_resources)

        _LOGGER.debug(
            f"[get_resources][account_id: {self.account_id}] FINISHED: Directory Service ({time.time() - start_time} sec)"
        )
        return resources

    def create_pre_shared_directory(self, vo ,directory_result):
        try:
            owner_desc = getattr(vo, "owner_directory_description",None)
            data = {
                "OwnerDirectoryId": owner_desc.directory_id if owner_desc else None,
                "OwnerAccountId": owner_desc.account_id if owner_desc else None,
                "ShareMethod": None,
                "SharedAccountId": directory_result["account"],
                "SharedDirectoryId": vo.id,
                "ShareStatus": vo.share_status,
                "CreatedDateTime": vo.launch_time,
                "OwnerDirectoryStatus": vo.stage,
                "OwnerDirectoryName" : vo.name,
                "DirectoryType": "Shared Microsoft AD"
            }

            shared_vo = SharedDirectory(data, strict=False)

            return {
                "name": shared_vo.shared_directory_id,
                "account": directory_result["account"],
                "region_code": directory_result["region_code"],
                "data": shared_vo,
                "reference": ReferenceModel(shared_vo.reference(directory_result["region_code"])),
                "tags": {}
            }

        except Exception as e:
            return self.generate_error(self.region_name, vo.id, e)


    def request_directory_list(self, region_name):
        self.cloud_service_type = "Directories"
        paginator = self.client.get_paginator("describe_directories")
        response_iterator = paginator.paginate(
            PaginationConfig={"MaxItems": 10000, "PageSize": 50}
        )

        for page in response_iterator:
            for raw in page.get("DirectoryDescriptions", []):
                resource_id = raw["DirectoryId"]
                try:
                    vo = Directory(raw, strict=False)

                    directory_type = raw.get("Type")
                    if directory_type == "ADConnector":
                        connect_settings = raw.get("ConnectSettings")
                        if connect_settings:
                            vo.vpc_setting = VpcSettings({
                                "VpcId": connect_settings.get("VpcId"),
                                "SubnetIds": connect_settings.get("SubnetIds", []),
                                "AvailabilityZones": connect_settings.get("AvailabilityZones", []),
                            }, strict=False)

                    regions_info = raw.get("RegionsInfo", {})
                    additional_regions = regions_info.get("AdditionalRegions", [])

                    vo.multi_region = "Yes" if len(additional_regions) >= 1 else "Not applicable"

                    yield {
                        "data": vo,
                        "name": vo.name,
                        "account": self.account_id,
                        "region_code": region_name,
                        "reference": ReferenceModel(vo.reference(region_name))
                    }
                except Exception as e:
                    yield self.generate_error(region_name, resource_id, e)


    def request_shared_directory_data(self, region_name, owner_directory_ids):
        self.cloud_service_type = "Directories shared with me"

        for owner_id in owner_directory_ids:
            paginator = self.client.get_paginator("describe_shared_directories")
            response_iterator = paginator.paginate(
                OwnerDirectoryId=owner_id,
                PaginationConfig={"MaxItems": 10000, "PageSize": 50}
            )

            for page in response_iterator:
                for raw in page.get("SharedDirectories", []):
                    sd_id = raw.get("SharedDirectoryId")

                    try:
                        owner_dir_id = raw.get("OwnerDirectoryId")
                        if owner_dir_id:
                            vpc_settings, owner_directory_name = self.request_owner_directory_detail(owner_dir_id)
                        else:
                            vpc_settings = None
                            owner_directory_name = None
                        if vpc_settings:
                            raw["VpcSettings"] = vpc_settings
                            raw["OwnerDirectoryName"] = owner_directory_name

                        raw["DirectoryType"] = "Shared Microsoft AD"
                        vo = SharedDirectory(raw, strict=False)

                        yield {
                            "data": vo,
                            "name": sd_id,
                            "account": self.account_id,
                            "region_code": region_name,
                            "reference": ReferenceModel(vo.reference(region_name))
                        }

                    except Exception as e:
                        yield self.generate_error(region_name, sd_id, e)

    def request_owner_directory_detail(self, directory_id):
            response = self.client.describe_directories(
                DirectoryIds=[directory_id]
            )

            dirs = response.get("DirectoryDescriptions", [])
            if not dirs:
                return None

            owner_dir = dirs[0]
            vpc_settings = owner_dir.get("VpcSettings")
            owner_directory_name = owner_dir.get("Name")
            return vpc_settings, owner_directory_name