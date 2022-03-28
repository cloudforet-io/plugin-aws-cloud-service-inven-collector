from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_lightsail_connector.schema.data import Instance, Disk, DiskSnapshot, \
    Bucket, StaticIP, RelationDatabase, Domain
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

instance = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
])

metadata = CloudServiceMeta.set_layouts(layouts=[instance])


class LightsailResource(CloudServiceResource):
    cloud_service_group = StringType(default='Lightsail')


class InstanceResource(LightsailResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(Instance)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class InstanceResponse(CloudServiceResponse):
    resource = PolyModelType(InstanceResource)


class DiskResource(LightsailResource):
    cloud_service_type = StringType(default='Disk')
    data = ModelType(Disk)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class DiskResponse(CloudServiceResponse):
    resource = PolyModelType(DiskResource)


class DiskSnapshotResource(LightsailResource):
    cloud_service_type = StringType(default='Snapshot')
    data = ModelType(DiskSnapshot)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class DiskSnapshotResponse(CloudServiceResponse):
    resource = PolyModelType(DiskSnapshotResource)


class BucketResource(LightsailResource):
    cloud_service_type = StringType(default='Bucket')
    data = ModelType(Bucket)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class BucketResponse(CloudServiceResponse):
    resource = PolyModelType(BucketResource)


class StaticIPResource(LightsailResource):
    cloud_service_type = StringType(default='StaticIP')
    data = ModelType(StaticIP)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class StaticIPResponse(CloudServiceResponse):
    resource = PolyModelType(StaticIPResource)


class RelationDatabaseResource(LightsailResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(RelationDatabase)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class RelationDatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(RelationDatabaseResource)


class DomainResource(LightsailResource):
    cloud_service_type = StringType(default='Domain')
    data = ModelType(Domain)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class DomainResponse(CloudServiceResponse):
    resource = PolyModelType(DomainResource)
