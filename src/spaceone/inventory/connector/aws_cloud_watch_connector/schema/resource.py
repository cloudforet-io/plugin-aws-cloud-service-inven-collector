from schematics.types import PolyModelType, StringType, ModelType

from spaceone.inventory.connector.aws_cloud_watch_connector.schema.data import Alarms
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource, CloudServiceMeta


# cloud_watch_alarms =

cloud_watch_metadata = CloudServiceMeta.set_layouts(
    # layouts=[cloud_watch_alarms]
)


class CloudWatchResource(CloudServiceResource):
    cloud_service_group = StringType(default="CloudWatch")


class AlarmsResource(CloudWatchResource):
    cloud_service_type = StringType(default="Alarms")
    data = ModelType(Alarms)
    _metadata = ModelType(
        CloudServiceMeta, default=cloud_watch_metadata, serialized_name="metadata"
    )


class AlarmsResponse(CloudServiceResponse):
    resource = PolyModelType(AlarmsResource)