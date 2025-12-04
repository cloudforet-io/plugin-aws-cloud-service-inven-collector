import os

from spaceone.inventory.conf.cloud_service_conf import ASSET_URL
from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, DateTimeDyField, SearchField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeMeta, \
    CloudServiceTypeResponse

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, "widget/total_count.yaml")
count_by_region_conf = os.path.join(current_dir, "widget/count_by_region.yaml")
count_by_account_conf = os.path.join(current_dir, "widget/count_by_account.yaml")

cst_directory = CloudServiceTypeResource()
cst_directory.name = "Directories"
cst_directory.provider = "aws"
cst_directory.group = "DirectoryService"
cst_directory.labels = ["Security"]
cst_directory.is_primary = True
cst_directory.is_major = True
cst_directory.service_code = "AWSDirectoryService"
cst_directory.tags = {
    "spaceone:icon" : f"{ASSET_URL}/AWS-Directory-Service.svg"
}

cst_directory._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Directory ID", "data.id"),
        EnumDyField.data_source("Type", "data.type",
                                default_badge={"indigo.500":["ADConnector"],"coral.600":["MicrosoftAD"],"green.500":["SimpleAD"]}),
        TextDyField.data_source("Edition","data.edition"),
        TextDyField.data_source("Multi-Region","data.multi_region"),
        EnumDyField.data_source("Status","data.stage", default_state={
            "safe":["Created","Active"],
            "warning" : ["Requested","Creating","Inoperable","Restoring","Deleting","Updating"],
            "alert" : ["Impaired","RestoreFailed", "Deleted","Failed"]
        }),
        DateTimeDyField.data_source("Launch date", "data.launch_time")
    ],
    search=[
        SearchField.set("ID","data.id"),
        SearchField.set(name = "Type",key ="data.type",
                        enums={
                            "ADConnector":{"label":"ADConnector","icon":{"color":"indigo.500"}},
                            "MicrosoftAD":{"label":"Microsoft AD","icon":{"color":"coral.600"}},
                            "SimpleAD":{"label":"SimpleAD","icon":{"color":"green.500"}},
                        }),
    ],
    widget=[
            CardWidget.set(**get_data_from_yaml(total_count_conf)),
            ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
            ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
        ]
)

cst_sd = CloudServiceTypeResource()
cst_sd.name = "Directories shared with me"
cst_sd.provider = "aws"
cst_sd.group = "DirectoryService"
cst_sd.labels = ["Security"]
cst_sd.service_code = "AWSDirectoryService"
cst_sd.tags = {
    "spaceone:icon" : f"{ASSET_URL}/AWS-Directory-Service.svg"
}

cst_sd._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Owner account ID","data.owner_account_id"),
        TextDyField.data_source("Owner directory name","data.owner_directory_name"),
        EnumDyField.data_source("Shared state","data.shared_state",
                                default_state={
                                    "safe": ["Shared", "Sharing"],
                                    "warning": ["PendingAcceptance", "Deleting", "Rejecting", "Rejected"],
                                    "alert": ["RejectFailed", "ShareFiled", "Deleted"]
                                }),
        DateTimeDyField.data_source("Date shared", "data.data_shared",),
    ],
    search=[
        SearchField.set(name = "Shared directory ID", key = "data.shared_directory_id"),
        SearchField.set(name = "Owner account ID", key = "data.owner_account_id"),
        SearchField.set(name = "Owner directory name", key = "data.owner_directory_name"),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_directory}),
    CloudServiceTypeResponse({"resource": cst_sd}),
]

