from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_rds_connector.schema.data import Database, Snapshot, SubnetGroup, ParameterGroup, \
    OptionGroup
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField, \
    DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

summary = ItemDynamicLayout.set_fields('Summary', fields=[
    TextDyField.data_source('DB Identifier', 'data.db_identifier'),
    EnumDyField.data_source('Role', 'data.role', default_badge={
        'indigo.500': ['cluster'], 'coral.600': ['instance']
    }),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['available'],
        'warning': ['creating', 'deleting', 'maintenance', 'modifying', 'rebooting',
                    'renaming', 'starting', 'stopping', 'upgrading'],
        'alert': ['failed', 'inaccessible-encryption-credentials', 'restore-error', 'stopped', 'storage-full']
    }),
    EnumDyField.data_source('Engine', 'data.engine',
                            default_outline_badge=['aurora', 'aurora-mysql', 'docdb', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                   'oracle-se1', 'oracle-se2', 'sqlserver-ex', 'sqlserver-web',
                                                   'sqlserver-se', 'sqlserver-ee']),
    TextDyField.data_source('Class', 'data.size'),
    TextDyField.data_source('Region & AZ', 'data.availability_zone'),
])

instance_conn = ItemDynamicLayout.set_fields('Connectivity', fields=[
    TextDyField.data_source('Endpoint', 'data.instance.endpoint.address'),
    TextDyField.data_source('Port', 'data.instance.endpoint.port'),
    TextDyField.data_source('Availability Zone', 'data.instance.availability_zone'),
    TextDyField.data_source('VPC', 'data.instance.db_subnet_group.vpc_id'),
    TextDyField.data_source('Subnet Group', 'data.instance.db_subnet_group.db_subnet_group_name'),
    ListDyField.data_source('Subnets', 'data.instance.db_subnet_group.subnets', default_badge={
        'type': 'outline',
        'sub_key': 'subnet_identifier',
        'delimiter': '<br>'
    }),
])

instance_sec = ItemDynamicLayout.set_fields('Security', fields=[
    ListDyField.data_source('VPC Security Groups', 'data.instance.vpc_security_groups', default_badge={
        'type': 'outline',
        'sub_key': 'vpc_security_group_id',
    }),
    EnumDyField.data_source('Public Accessibility', 'data.instance.publicly_accessible', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Certificate Authority', 'data.instance.ca_certificate_identifier')
])

instance_conf = ItemDynamicLayout.set_fields('Configuraiton', fields=[
    TextDyField.data_source('DB Instance ID', 'data.instance.db_instance_identifier'),
    TextDyField.data_source('Engine Version', 'data.instance.engine_version'),
    TextDyField.data_source('License Model', 'data.instance.license_model'),
    ListDyField.data_source('Option Groups', 'data.instance.option_group_memberships', default_badge={
        'type': 'outline',
        'sub_key': 'option_group_name',
    }),
    TextDyField.data_source('ARN', 'data.instance.db_instance_arn'),
    TextDyField.data_source('Resource ID', 'data.instance.dbi_resource_id'),
    ListDyField.data_source('Parameter Group', 'data.instance.db_parameter_groups', default_badge={
        'type': 'outline',
        'sub_key': 'db_parameter_group_name',
    }),
    EnumDyField.data_source('Deletion Protection', 'data.instance.deletion_protection', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Instance Class', 'data.instance.db_instance_class'),
    EnumDyField.data_source('IAM DB Authentication', 'data.instance.iam_database_authentication_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Master username', 'data.instance.master_username'),
    EnumDyField.data_source('Multi AZ', 'data.instance.multi_az', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Performance Insights enabled', 'data.instance.performance_insights_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Created Time', 'data.instance.instance_create_time'),
])

instance_storage = ItemDynamicLayout.set_fields('Storage', fields=[
    EnumDyField.data_source('Storage Encryption', 'data.instance.storage_encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Storage Type', 'data.instance.storage_type',
                            default_outline_badge=['standard', 'io1', 'gp2', 'st1', 'sc1']),
    TextDyField.data_source('IOPS', 'data.instance.iops'),
    TextDyField.data_source('Storage (GB)', 'data.instance.allocated_storage'),
    TextDyField.data_source('Maximum Storage Threshold (GB)', 'data.instance.max_allocated_storage'),
])

instance_maintenance = ItemDynamicLayout.set_fields('Maintenance', fields=[
    EnumDyField.data_source('Auto Minor Version Upgrade', 'data.instance.auto_minor_version_upgrade', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Maintenance Window', 'data.instance.preferred_maintenance_window'),
])

instance_backup = ItemDynamicLayout.set_fields('Backup', fields=[
    TextDyField.data_source('Automated Backup (Period Day)', 'data.instance.backup_retention_period'),
    EnumDyField.data_source('Copy tags to snapshots', 'data.instance.copy_tags_to_snapshot', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Latest Restore Time', 'data.instance.latest_restorable_time'),
    TextDyField.data_source('Backup Window', 'data.instance.preferred_backup_window'),
])

instance_tags = SimpleTableDynamicLayout.set_tags()
instance_metadata = CloudServiceMeta.set_layouts(layouts=[summary, instance_conn, instance_sec, instance_conf,
                                                          instance_storage, instance_maintenance, instance_backup,
                                                          instance_tags])

cluster_endpoint = ItemDynamicLayout.set_fields('Endpoints', fields=[
    TextDyField.data_source('Endpoint', 'data.cluster.endpoint'),
    TextDyField.data_source('Port', 'data.cluster.port'),
    TextDyField.data_source('Reader Endpoint', 'data.cluster.reader_endpoint'),
])

cluster_conf = ItemDynamicLayout.set_fields('Configuration', fields=[
    TextDyField.data_source('DB Cluster ID', 'data.cluster.db_cluster_identifier'),
    TextDyField.data_source('ARN', 'data.cluster.db_cluster_arn'),
    BadgeDyField.data_source('DB Cluster Role', 'data.cluster.db_cluster_role'),
    TextDyField.data_source('Engine Version', 'data.cluster.engine_version'),
    TextDyField.data_source('Resource ID', 'data.cluster.db_cluster_resource_id'),
    BadgeDyField.data_source('Engine Mode', 'data.cluster.engine_mode'),
    TextDyField.data_source('DB Cluster Parameter Group', 'data.cluster.db_cluster_parameter_group'),
    EnumDyField.data_source('Deletion Protection', 'data.cluster.deletion_protection', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('IAM DB Authentication', 'data.cluster.iam_database_authentication_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Master username', 'data.cluster.master_username'),
    EnumDyField.data_source('Multi AZ', 'data.cluster.multi_az', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Encrypted', 'data.cluster.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('KSM Key', 'data.cluster.kms_key_id'),
    DateTimeDyField.data_source('Created Time', 'data.cluster_create_time')
])

cluster_maintenance = ItemDynamicLayout.set_fields('Maintenance', fields=[
    TextDyField.data_source('Maintenance Window', 'data.cluster.preferred_maintenance_window'),
])

cluster_backup = ItemDynamicLayout.set_fields('Backup', fields=[
    TextDyField.data_source('Automated Backup (Period Day)', 'data.cluster.backup_retention_period'),
    EnumDyField.data_source('Copy tags to snapshots', 'data.cluster.copy_tags_to_snapshot', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Earliest Restorable Time', 'data.cluster.earliest_restorable_time'),
    DateTimeDyField.data_source('Latest Restore Time', 'data.cluster.latest_restorable_time'),
    TextDyField.data_source('Backup Window', 'data.cluster.preferred_backup_window'),
])

cluster_tags = SimpleTableDynamicLayout.set_tags()
cluster_metadata = CloudServiceMeta.set_layouts(layouts=[summary, cluster_endpoint, cluster_conf, cluster_maintenance,
                                                         cluster_backup, cluster_tags])


snapshot = ItemDynamicLayout.set_fields('Snapshot', fields=[
    TextDyField.data_source('Name', 'data.db_snapshot_identifier'),
    TextDyField.data_source('ARN', 'data.db_snapshot_arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['available'],
        'warning': ['creating', 'pending']
    }),
    TextDyField.data_source('Cluster/Instance Name', 'data.db_instance_identifier'),
    EnumDyField.data_source('Type', 'data.snapshot_type', default_outline_badge=['manual', 'automated']),
    EnumDyField.data_source('Storage Type', 'data.storage_type',
                             default_outline_badge=['standard', 'io1', 'gp2', 'st1', 'sc1']),
    TextDyField.data_source('Allocated Size', 'data.allocated_storage'),
    EnumDyField.data_source('DB Engine', 'data.engine',
                            default_outline_badge=['aurora', 'aurora-mysql', 'docdb', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                   'oracle-se1', 'oracle-se2', 'sqlserver-ex', 'sqlserver-web',
                                                   'sqlserver-se', 'sqlserver-ee']),
    TextDyField.data_source('DB Engine Version', 'data.engine_version'),
    TextDyField.data_source('Master username', 'data.master_username'),
    TextDyField.data_source('License Model', 'data.license_model'),
    TextDyField.data_source('Option Group', 'data.option_group_name'),
    TextDyField.data_source('VPC', 'data.vpc_id'),
    TextDyField.data_source('Availability Zone', 'data.availability_zone'),
    TextDyField.data_source('KMS Key ID', 'data.kms_key_id'),
    TextDyField.data_source('Port', 'data.port'),
    DateTimeDyField.data_source('Snapshot Creation Time', 'data.snapshot_create_time'),
])
snapshot_tags = SimpleTableDynamicLayout.set_tags()
snapshot_metadata = CloudServiceMeta.set_layouts(layouts=[snapshot, snapshot_tags])

subnetgrp = ItemDynamicLayout.set_fields('Subnet Group', fields=[
    TextDyField.data_source('Name', 'data.db_subnet_group_name'),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('ARN', 'data.db_subnet_group_arn'),
    TextDyField.data_source('Description', 'data.db_subnet_group_description'),
])

subnets = TableDynamicLayout.set_fields('Subnets', 'data.subnets', fields=[
    TextDyField.data_source('Availability Zone', 'subnet_availability_zone.name'),
    TextDyField.data_source('Subnet ID', 'subnet_identifier'),
    EnumDyField.data_source('Status', 'subnet_status', default_state={
        'safe': ['Active']
    }),
])
subnetgrp_tags = SimpleTableDynamicLayout.set_tags()
subnetgrp_metadata = CloudServiceMeta.set_layouts(layouts=[subnetgrp, subnets, subnetgrp_tags])

paramgrp = ItemDynamicLayout.set_fields('Parameter Group', fields=[
    TextDyField.data_source('Name', 'data.db_parameter_group_name'),
    TextDyField.data_source('ARN', 'data.db_parameter_group_arn'),
    BadgeDyField.data_source('Family', 'data.db_parameter_group_family'),
    TextDyField.data_source('Type', 'data.description'),
    TextDyField.data_source('Description', 'data.db_parameter_group_type'),
])

params = TableDynamicLayout.set_fields('Parameters', 'data.parameters', fields=[
    TextDyField.data_source('Name', 'parameter_name'),
    TextDyField.data_source('Value', 'parameter_value'),
    TextDyField.data_source('Allowed Values', 'allowed_values'),
    EnumDyField.data_source('Modifiable', 'is_modifiable', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Source', 'source', default_outline_badge=['engine-default', 'system']),
    EnumDyField.data_source('Apply Type', 'apply_method', default_outline_badge=['pending-reboot', 'immediate']),
    EnumDyField.data_source('Data Type', 'data_type', default_outline_badge=['string', 'boolean', 'integer', 'list']),
    TextDyField.data_source('Description', 'description'),
])
paramgrp_tags = SimpleTableDynamicLayout.set_tags()
paramgrp_metadata = CloudServiceMeta.set_layouts(layouts=[paramgrp, params, paramgrp_tags])


optgrp = ItemDynamicLayout.set_fields('Option Groups', fields=[
    TextDyField.data_source('Name', 'data.option_group_name'),
    TextDyField.data_source('ARN', 'data.option_group_arn'),
    TextDyField.data_source('Description', 'data.option_group_description'),
    EnumDyField.data_source('Engine', 'data.engine_name',
                            default_outline_badge=['aurora', 'aurora-mysql', 'docdb', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                   'oracle-se1', 'oracle-se2', 'sqlserver-ex', 'sqlserver-web',
                                                   'sqlserver-se', 'sqlserver-ee']),
    TextDyField.data_source('Major Engine Version', 'data.major_engine_version'),
    TextDyField.data_source('VPC ID', 'data.vpc_id')
])

optgrp_opt = TableDynamicLayout.set_fields('Options', 'data.options', fields=[
    TextDyField.data_source('Name', 'option_name'),
    EnumDyField.data_source('Persistent', 'persistent', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Permanent', 'permanent', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Port', 'port'),
    ListDyField.data_source('Security Groups', 'db_security_group_memberships', default_badge={
        'type': 'outline',
        'sub_key': 'db_security_group_name'
    }),
    TextDyField.data_source('Version', 'option_version'),
    ListDyField.data_source('Settings Name', 'option_settings', default_badge={
        'type': 'outline',
        'sub_key': 'name'
    }),
    ListDyField.data_source('Settings Value', 'option_settings', default_badge={
        'type': 'outline',
        'sub_key': 'value'
    }),
])
optgrp_tags = SimpleTableDynamicLayout.set_tags()
optgrp_metadata = CloudServiceMeta.set_layouts(layouts=[optgrp, optgrp_opt, optgrp_tags])


class RDSResource(CloudServiceResource):
    cloud_service_group = StringType(default='RDS')


class DatabaseResource(RDSResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(Database)


class DBInstanceResource(DatabaseResource):
    _metadata = ModelType(CloudServiceMeta, default=instance_metadata, serialized_name='metadata')


class DBClusterResource(DatabaseResource):
    _metadata = ModelType(CloudServiceMeta, default=cluster_metadata, serialized_name='metadata')


class DatabaseResponse(CloudServiceResponse):
    resource = PolyModelType([DBInstanceResource, DBClusterResource])


class SnapshotResource(RDSResource):
    cloud_service_type = StringType(default='Snapshot')
    data = ModelType(Snapshot)
    _metadata = ModelType(CloudServiceMeta, default=snapshot_metadata, serialized_name='metadata')


class SnapshotResponse(CloudServiceResponse):
    resource = PolyModelType(SnapshotResource)


class SubnetGroupResource(RDSResource):
    cloud_service_type = StringType(default='SubnetGroup')
    data = ModelType(SubnetGroup)
    _metadata = ModelType(CloudServiceMeta, default=subnetgrp_metadata, serialized_name='metadata')


class SubnetGroupResponse(CloudServiceResponse):
    resource = PolyModelType(SubnetGroupResource)


class ParameterGroupResource(RDSResource):
    cloud_service_type = StringType(default='ParameterGroup')
    data = ModelType(ParameterGroup)
    _metadata = ModelType(CloudServiceMeta, default=paramgrp_metadata, serialized_name='metadata')


class ParameterGroupResponse(CloudServiceResponse):
    resource = PolyModelType(ParameterGroupResource)


class OptionGroupResource(RDSResource):
    cloud_service_type = StringType(default='OptionGroup')
    data = ModelType(OptionGroup)
    _metadata = ModelType(CloudServiceMeta, default=optgrp_metadata, serialized_name='metadata')


class OptionGroupResponse(CloudServiceResponse):
    resource = PolyModelType(OptionGroupResource)
