from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_lightsail_connector.schema.data import Instance, Disk, DiskSnapshot, \
    Bucket, StaticIP, RelationDatabase, Domain, ContainerService, LoadBalancer, Distribution
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField, ListDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout


class LightsailResource(CloudServiceResource):
    cloud_service_group = StringType(default='Lightsail')

'''
Instance
'''
instance = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name'),
    TextDyField.data_source('Blue Print ID', 'data.blueprint_id'),
    TextDyField.data_source('Blue Print Name', 'data.blueprint_name'),
    TextDyField.data_source('Bundle ID', 'data.bundle_id'),
    EnumDyField.data_source('Static IP', 'data.is_static_ip', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Private IP', 'data.private_ip_address'),
    TextDyField.data_source('Public IP', 'data.public_ip_address'),
    ListDyField.data_source('IPv6', 'data.ipv6_address', default_badge={
        'type': 'outline'
    }),
    TextDyField.data_source('State', 'data.state.name'),
    TextDyField.data_source('User Name', 'data.username'),
    TextDyField.data_source('SSH Key Name', 'data.ssh_key_name')
])

instance_addon = TableDynamicLayout.set_fields('Snapshot Time', root_path='data.add_ons', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Status', 'status'),
    TextDyField.data_source('Snapshot Time Of Day', 'snapshot_time_of_day'),
    TextDyField.data_source('Next Snapshot Time Of Day', 'next_snapshot_time_of_day')
])

instance_hardware = TableDynamicLayout.set_fields('Hardware', root_path='data.hardware', fields=[
    TextDyField.data_source('CPU Count', 'cpu_count'),
    ListDyField.data_source('Disks', 'disks', default_badge={
        'type': 'outline',
        'sub_key': 'name'
    }),
    SizeField.data_source('Ram', 'ram_size_in_gb', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    })
])

instance_networking = TableDynamicLayout.set_fields('Networking', root_path='data.networking', fields=[
    TextDyField.data_source('Monthly Transfer', 'monthly_transfer.gb_per_month_allocated'),
    ListDyField.data_source('Ports', 'ports', default_badge={
        'type': 'outline',
        'sub_key': 'common_name'
    })
])

instance_tags = SimpleTableDynamicLayout.set_tags()

instance_metadata = CloudServiceMeta.set_layouts(layouts=[instance, instance_addon, instance_hardware, instance_networking, instance_tags])


class InstanceResource(LightsailResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(Instance)
    _metadata = ModelType(CloudServiceMeta, default=instance_metadata, serialized_name='metadata')


class InstanceResponse(CloudServiceResponse):
    resource = PolyModelType(InstanceResource)


'''
Disk
'''

disk = ItemDynamicLayout.set_fields('Disk', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name'),
    SizeField.data_source('Size', 'data.size_in_gb', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    EnumDyField.data_source('System Disk', 'data.is_system_disk', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('IOPS', 'disk.iops'),
    TextDyField.data_source('Path', 'disk.path'),
    TextDyField.data_source('State', 'disk.state'),
    TextDyField.data_source('Attached To', 'disk.attached_to'),
    EnumDyField.data_source('Attached', 'data.is_attached', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Attachment State', 'data.attachment_state'),
    SizeField.data_source('GB In Use', 'data.gb_in_use', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    })
])

disk_addons = TableDynamicLayout.set_fields('Snapshot Time', root_path='data.add_ons', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Status', 'status'),
    TextDyField.data_source('Snapshot Time Of Day', 'snapshot_time_of_day'),
    TextDyField.data_source('Next Snapshot Time Of Day', 'next_snapshot_time_of_day')
])

disk_tags = SimpleTableDynamicLayout.set_tags()

disk_metadata = CloudServiceMeta.set_layouts(layouts=[disk, disk_addons, disk_tags])


class DiskResource(LightsailResource):
    cloud_service_type = StringType(default='Disk')
    data = ModelType(Disk)
    _metadata = ModelType(CloudServiceMeta, default=disk_metadata, serialized_name='metadata')


class DiskResponse(CloudServiceResponse):
    resource = PolyModelType(DiskResource)

'''
DiskSnapshot
'''

disk_snapshot = ItemDynamicLayout.set_fields('DiskSnapshot', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name'),
    SizeField.data_source('Size', 'data.size_in_gb', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    TextDyField.data_source('State', 'data.state'),
    TextDyField.data_source('Progress', 'data.progress'),
    TextDyField.data_source('From Disk Name', 'data.from_disk_name'),
    TextDyField.data_source('From Disk Arn', 'data.from_disk_arn'),
    TextDyField.data_source('From Instance Name', 'data.from_instance_name'),
    TextDyField.data_source('From Instance Arn', 'data.from_instance_arn'),
    EnumDyField.data_source('Auto Snapshot', 'data.is_from_auto_snapshot', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

disk_snapshot_tags = SimpleTableDynamicLayout.set_tags()

disk_snapshot_metadata = CloudServiceMeta.set_layouts(layouts=[disk_snapshot, disk_snapshot_tags])


class DiskSnapshotResource(LightsailResource):
    cloud_service_type = StringType(default='Snapshot')
    data = ModelType(DiskSnapshot)
    _metadata = ModelType(CloudServiceMeta, default=disk_snapshot_metadata, serialized_name='metadata')


class DiskSnapshotResponse(CloudServiceResponse):
    resource = PolyModelType(DiskSnapshotResource)


'''
Bucket
'''

bucket = ItemDynamicLayout.set_fields('Bucket', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name'),
    TextDyField.data_source('URL', 'data.url'),
    TextDyField.data_source('Object Versioning', 'data.object_versioning'),
    EnumDyField.data_source('Able To Update Bundle', 'data.able_to_update_bundle', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    ListDyField.data_source('Readonly Access Accounts', 'readonly_access_accounts', default_badge={
        'type': 'outline'
    }),

])

bucket_access_rule = ItemDynamicLayout.set_fields('Access Rule', root_path='data.access_rules', fields=[
    TextDyField.data_source('Get Object', 'get_object'),
    EnumDyField.data_source('Allow Public Overrides', 'data.allow_public_overrides', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    })
])

bucket_resource_receiving_access = TableDynamicLayout.set_fields('Resource Receiving Access', root_path='data.readonly_access_accounts', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Resource Type', 'resource_type')
])

bucket_state = ItemDynamicLayout.set_fields('State', root_path='data.state', fields=[
    TextDyField.data_source('Code', 'code'),
    TextDyField.data_source('Message', 'message')
])

bucket_access_log_config = ItemDynamicLayout.set_fields('Access Log Config', root_path='data.access_log_config', fields=[
    EnumDyField.data_source('Enabled', 'enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Destination', 'destination'),
    TextDyField.data_source('Prefix', 'prefix')
])

bucket_tags = SimpleTableDynamicLayout.set_tags()

bucket_metadata = CloudServiceMeta.set_layouts(layouts=[bucket, bucket_access_rule, bucket_resource_receiving_access,
                                                        bucket_state, bucket_access_log_config, bucket_tags])


class BucketResource(LightsailResource):
    cloud_service_type = StringType(default='Bucket')
    data = ModelType(Bucket)
    _metadata = ModelType(CloudServiceMeta, default=bucket_metadata, serialized_name='metadata')


class BucketResponse(CloudServiceResponse):
    resource = PolyModelType(BucketResource)


'''
StaticIP
'''
staticip = ItemDynamicLayout.set_fields('StaticIP', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name'),
    TextDyField.data_source('IP', 'data.ip_address'),
    TextDyField.data_source('Attached To', 'data.attached_to'),
    EnumDyField.data_source('Attached', 'data.is_attached', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

staticip_metadata = CloudServiceMeta.set_layouts(layouts=[staticip])


class StaticIPResource(LightsailResource):
    cloud_service_type = StringType(default='StaticIP')
    data = ModelType(StaticIP)
    _metadata = ModelType(CloudServiceMeta, default=staticip_metadata, serialized_name='metadata')


class StaticIPResponse(CloudServiceResponse):
    resource = PolyModelType(StaticIPResource)


'''
RDS
'''
rds = ItemDynamicLayout.set_fields('RDS', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name'),
    TextDyField.data_source('Blueprint ID', 'data.relation_database_blueprint_id'),
    TextDyField.data_source('Bundle ID', 'data.relation_database_bundle_id'),
    TextDyField.data_source('Master Database Name', 'data.master_database_name'),
    TextDyField.data_source('State', 'data.state'),
    TextDyField.data_source('Secondary Availability Zone', 'data.secondary_availability_zone'),
    EnumDyField.data_source('Backup Retention Enabled', 'data.backup_retention_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Engine', 'data.engine'),
    TextDyField.data_source('Engine Version', 'data.engine_version'),
    DateTimeDyField.data_source('Latest Restorable Time', 'data.latest_restorable_time'),
    TextDyField.data_source('Master User Name', 'data.master_user_name'),
    TextDyField.data_source('Parameter Apply Status', 'data.parameter_apply_status'),
    TextDyField.data_source('Preferred Backup Window', 'data.preferred_backup_window'),
    TextDyField.data_source('Preferred Maintenance Window', 'data.preferred_maintenance_window'),
    EnumDyField.data_source('Publicly Accessible', 'data.publicly_accessible', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('CA Certificate Identifier', 'data.ca_certificate_identifier')
])

rds_hardware = ItemDynamicLayout.set_fields('Hardware', root_path='data.hardware', fields=[
    TextDyField.data_source('CPU Count', 'cpu_count'),
    SizeField.data_source('Disk Size', 'disk_size_in_gb', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    }),
    SizeField.data_source('Ram Size', 'ram_size_in_gb', options={
        'display_unit': 'GB',
        'source_unit': 'GB'
    })
])

rds_pending_modified_values = ItemDynamicLayout.set_fields('Pending Modified Values', root_path='data.pending_modified_values', fields=[
    TextDyField.data_source('Engine Version', 'engine_version'),
    EnumDyField.data_source('Backup Retention Enabled', 'backup_retention_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

rds_master_endpoint = ItemDynamicLayout.set_fields('Master Endpoint', root_path='data.master_endpoint', fields=[
    TextDyField.data_source('Port', 'port'),
    TextDyField.data_source('Address', 'address')
])

rds_pending_maintenance_actions = TableDynamicLayout.set_fields('Pending Maintenance Actions', root_path='data.pending_maintenance_actions', fields=[
    TextDyField.data_source('Action', 'action'),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Current Apply Date', 'current_apply_date')
])

rds_tags = SimpleTableDynamicLayout.set_tags()

rds_metadata = CloudServiceMeta.set_layouts(layouts=[rds, rds_hardware, rds_pending_modified_values, rds_master_endpoint,
                                                     rds_pending_maintenance_actions, rds_tags])


class RelationDatabaseResource(LightsailResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(RelationDatabase)
    _metadata = ModelType(CloudServiceMeta, default=rds_metadata, serialized_name='metadata')


class RelationDatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(RelationDatabaseResource)

'''
Domain
'''
domain = ItemDynamicLayout.set_fields('Domain', fields=[
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Support Code', 'data.support_code'),
    DateTimeDyField.data_source('Created At', 'data.created_at'),
    TextDyField.data_source('Availability Zone', 'data.location.availability_zone'),
    TextDyField.data_source('Region', 'data.location.region_name')
])

domain_entry = TableDynamicLayout.set_fields('Entry', root_path='data.domain_entry', fields=[
    TextDyField.data_source('ID', 'id'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Target', 'target'),
    TextDyField.data_source('Type', 'type'),
    EnumDyField.data_source('Is Alias', 'is_alias', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    })
])

domain_tags = SimpleTableDynamicLayout.set_tags()

domain_metadata = CloudServiceMeta.set_layouts(layouts=[domain, domain_entry, domain_tags])


class DomainResource(LightsailResource):
    cloud_service_type = StringType(default='Domain')
    data = ModelType(Domain)
    _metadata = ModelType(CloudServiceMeta, default=domain_metadata, serialized_name='metadata')


class DomainResponse(CloudServiceResponse):
    resource = PolyModelType(DomainResource)
