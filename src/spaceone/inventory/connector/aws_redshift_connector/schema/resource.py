from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_redshift_connector.schema.data import Cluster
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout

base = ItemDynamicLayout.set_fields('Clusters', fields=[
    TextDyField.data_source('Cluster', 'data.cluster_identifier'),
    EnumDyField.data_source('Status', 'data.cluster_status', default_state={
        'safe': ['available'],
        'warning': ['prep-for-resize', 'resize-cleanup', 'cancelling-resize', 'creating', 'deleting', 'final-snapshot',
                    'modifying', 'rebooting', 'renaming', 'resizing', 'rotating-keys', 'updating-hsm'],
        'disable': ['paused'],
        'alert': ['hardware-failure', 'incompatible-hsm', 'incompatible-network', 'incompatible-parameters',
                  'incompatible-restore', 'storage-full']
    }),
    TextDyField.data_source('Endpoint', 'data.endpoint.address'),
    TextDyField.data_source('Cluster Version', 'data.cluster_version'),
    EnumDyField.data_source('Cluster Availability Status', 'data.cluster_availability_status', default_state={
        'safe': ['Available'],
        'warning': ['Maintenance', 'Modifying'],
        'disable': ['Unavailable'],
        'alert': ['Failed']
    }),
    TextDyField.data_source('Node Count', 'data.number_of_nodes'),
    TextDyField.data_source('Node Type', 'data.node_type'),
    TextDyField.data_source('Automated Snapshot Retention Period', 'data.automated_snapshot_retention_period'),
    TextDyField.data_source('Manual Snapshot Retention Period', 'data.manual_snapshot_retention_period'),
    EnumDyField.data_source('Allow Version Upgrade', 'data.allow_version_upgrade', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Cluster Revision Number', 'data.cluster_revision_number'),
])

db_conf = ItemDynamicLayout.set_fields('Database configurations', fields=[
    TextDyField.data_source('Database Name', 'data.db_name'),
    TextDyField.data_source('Port', 'data.endpoint.port'),
    TextDyField.data_source('Master User Name', 'data.master_username'),
    EnumDyField.data_source('Encrypted', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

net_sec = ItemDynamicLayout.set_fields('Network and Security', fields=[
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('Availability Zone', 'data.availability_zone'),
    TextDyField.data_source('Subnet Group', 'data.cluster_subnet_group_name'),
    ListDyField.data_source('Security Groups', 'data.vpc_security_groups', options={
        'sub_key': 'vpc_security_group_id',
        'delimiter': '<br>'
    }),
    EnumDyField.data_source('Enhanced VPC Routing', 'data.enhanced_vpc_routing', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Publicly Accessible', 'data.publicly_accessible', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    })
])

param_group = ItemDynamicLayout.set_fields('Parameter Groups', 'data.cluster_parameter_groups', fields=[
    TextDyField.data_source('Parameter Group Name', 'parameter_group_name'),
    EnumDyField.data_source('Apply status', 'parameter_apply_status', default_state={
        'safe': ['available']
    }),
])

nodes = TableDynamicLayout.set_fields('Nodes', 'data.cluster_nodes', fields=[
    TextDyField.data_source('Node Role', 'node_role'),
    TextDyField.data_source('Private IP', 'private_ip_address'),
    TextDyField.data_source('Public IP', 'public_ip_address'),
])

snapshots = TableDynamicLayout.set_fields('Snapshots', 'data.snapshots', fields=[
    TextDyField.data_source('Snapshot Identifier', 'snapshot_identifier'),
    TextDyField.data_source('Snapshot Type', 'snapshot_type'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['active']
    }),
    TextDyField.data_source('Size(MB)', 'total_backup_size_in_mega_bytes'),
    TextDyField.data_source('Actual Incremental Size(MB)', 'actual_incremental_backup_size_in_mega_bytes'),
    EnumDyField.data_source('Encrypted', 'encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Creation Time', 'snapshot_create_time'),
])

snpashot_schedule = TableDynamicLayout.set_fields('Snapshot Schedules', 'data.snapshot_schedules', fields=[
    TextDyField.data_source('Schedule Identifier', 'schedule_identifier'),
    TextDyField.data_source('Schedule Description', 'schedule_description'),
    TextDyField.data_source('Schedule Definition', 'schedule_definitions'),
    EnumDyField.data_source('State', 'associated_state', default_state={
        'safe': ['active']
    }),
])

scheduled_action = TableDynamicLayout.set_fields('Scheduled Actions', 'data.scheduled_actions', fields=[
    TextDyField.data_source('Action name', 'scheduled_action_name'),
    TextDyField.data_source('Description', 'scheduled_action_description'),
    TextDyField.data_source('Schedule', 'schedule'),
    EnumDyField.data_source('State', 'state', default_state={
        'safe': ['available']
    }),
    TextDyField.data_source('IAM Role', 'iam_role'),
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[base, db_conf, net_sec, param_group, nodes, snapshots,
                                                 snpashot_schedule, scheduled_action, tags])


class RedshiftResource(CloudServiceResource):
    cloud_service_group = StringType(default='Redshift')


class ClusterResource(RedshiftResource):
    cloud_service_type = StringType(default='Cluster')
    data = ModelType(Cluster)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class ClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterResource)
