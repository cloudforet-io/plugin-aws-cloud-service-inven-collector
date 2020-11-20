from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_ebs_connector.schema.data import Volume, Snapshot
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout

# VOLUME
vol_base = ItemDynamicLayout.set_fields('Volumes', fields=[
    TextDyField.data_source('Volume ID', 'data.volume_id'),
    TextDyField.data_source('ARN', 'data.arn'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['in-use'],
        'available': ['available'],
        'warning': ['deleting', 'creating'],
        'disable': ['deleted'],
        'alert': ['error']
    }),
    TextDyField.data_source('Outpost ARN', 'data.outpost_arn'),
    TextDyField.data_source('Size (GB)', 'data.size_gb'),
    EnumDyField.data_source('Volume Type', 'data.volume_type',
                            default_outline_badge=['standard', 'io1', 'gp2', 'sc1', 'st1']),
    TextDyField.data_source('Snapshot', 'data.snapshot_id'),
    TextDyField.data_source('Availability Zone', 'data.availability_zone'),
    EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    ListDyField.data_source('Attachment information', 'data.attachments', default_badge={
        'type': 'outline',
        'sub_key': 'instance_id',
    }),
    TextDyField.data_source('KMS Key ID', 'data.kms_key_id'),
    TextDyField.data_source('KMS Key ARN', 'data.kms_key_arn'),
    TextDyField.data_source('IOPS', 'data.iops'),
    EnumDyField.data_source('Multi-Attach Enabled', 'data.multi_attach_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Created', 'data.create_time'),
])

vol_tags = SimpleTableDynamicLayout.set_tags()
vol_metadata = CloudServiceMeta.set_layouts(layouts=[vol_base, vol_tags])


# SNAPSHOT
ss_base = ItemDynamicLayout.set_fields('Snapshots', fields=[
    TextDyField.data_source('Snapshot ID', 'data.snapshot_id'),
    TextDyField.data_source('ARN', 'data.arn'),
    EnumDyField.data_source('Status', 'data.state', default_state={
        'safe': ['completed'],
        'warning': ['pending'],
        'alert': ['error']
    }),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Progress', 'data.progress'),
    TextDyField.data_source('Capacity', 'data.volume_size'),
    TextDyField.data_source('Volume', 'data.volume_id'),
    EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Owner', 'data.owner_id'),
    TextDyField.data_source('KMS Key ID', 'data.kms_key_id'),
    TextDyField.data_source('KMS Key ARN', 'data.kms_key_arn'),
    DateTimeDyField.data_source('Started', 'data.start_time'),
])

ss_tags = SimpleTableDynamicLayout.set_tags()
ss_metadata = CloudServiceMeta.set_layouts(layouts=[ss_base, ss_tags])


class EC2Resource(CloudServiceResource):
    cloud_service_group = StringType(default='EC2')


class VolumeResource(EC2Resource):
    cloud_service_type = StringType(default='Volume')
    data = ModelType(Volume)
    _metadata = ModelType(CloudServiceMeta, default=vol_metadata, serialized_name='metadata')


class VolumeResponse(CloudServiceResponse):
    resource = PolyModelType(VolumeResource)


class SnapshotResource(EC2Resource):
    cloud_service_type = StringType(default='Snapshot')
    data = ModelType(Snapshot)
    _metadata = ModelType(CloudServiceMeta, default=ss_metadata, serialized_name='metadata')


class SnapshotResponse(CloudServiceResponse):
    resource = PolyModelType(SnapshotResource)
