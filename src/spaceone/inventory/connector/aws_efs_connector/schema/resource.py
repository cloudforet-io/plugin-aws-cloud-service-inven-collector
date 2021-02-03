from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_efs_connector.schema.data import FileSystem
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, EnumDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout


base = ItemDynamicLayout.set_fields('File Systems', fields=[
    TextDyField.data_source('ID', 'data.file_system_id'),
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('File System State', 'data.life_cycle_state', default_state={
        'safe': ['available'],
        'warning': ['creating', 'updating', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Owner ID', 'data.owner_id'),
    SizeField.data_source('Metered Size', 'data.size_in_bytes.value'),
    TextDyField.data_source('Number of mount targets', 'data.number_of_mount_targets'),
    TextDyField.data_source('Performance mode', 'data.performance_mode'),
    TextDyField.data_source('Throughput mode', 'data.throughput_mode'),
    EnumDyField.data_source('Encrypted', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    ListDyField.data_source('Lifecycle policy', 'data.life_cycle_policies', options={
        'sub_key': 'transition_to_ia_display',
        'delimiter': '<br>'
    }),
    DateTimeDyField.data_source('Creation date', 'data.creation_time')
])

mount_target = TableDynamicLayout.set_fields('Mount Targets', 'data.mount_targets', fields=[
    TextDyField.data_source('Mount target ID', 'mount_target_id'),
    EnumDyField.data_source('State', 'life_cycle_state', default_state={
        'safe': ['available'],
        'warning': ['creating', 'updating', 'deleting'],
        'disable': ['deleted']
    }),
    TextDyField.data_source('Availability Zone', 'availability_zone_name'),
    TextDyField.data_source('Subnet', 'subnet_id'),
    TextDyField.data_source('IP Address', 'ip_address'),
    TextDyField.data_source('Network Interface ID', 'network_interface_id'),
    ListDyField.data_source('Security Groups', 'security_groups', default_badge={'type': 'outline'}),
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[base, mount_target, tags])


class EFSResource(CloudServiceResource):
    cloud_service_group = StringType(default='EFS')


class FileSystemResource(EFSResource):
    cloud_service_type = StringType(default='FileSystem')
    data = ModelType(FileSystem)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class FileSystemResponse(CloudServiceResponse):
    resource = PolyModelType(FileSystemResource)
