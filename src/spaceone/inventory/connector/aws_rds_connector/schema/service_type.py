import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

'''
Database
'''
database_total_count_conf = os.path.join(current_dir, 'widget/database_total_count.yaml')
database_count_by_region_conf = os.path.join(current_dir, 'widget/database_count_by_region.yaml')
database_count_by_account_conf = os.path.join(current_dir, 'widget/database_count_by_account.yaml')
database_count_by_engine_conf = os.path.join(current_dir, 'widget/database_count_by_engine.yaml')

cst_rds_database = CloudServiceTypeResource()
cst_rds_database.name = 'Database'
cst_rds_database.provider = 'aws'
cst_rds_database.group = 'RDS'
cst_rds_database.labels = ['Database']
cst_rds_database.is_primary = True
cst_rds_database.is_major = True
cst_rds_database.service_code = 'AmazonRDS'
cst_rds_database.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-RDS.svg',
}

cst_rds_database._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Role', 'data.role'),
        TextDyField.data_source('Engine', 'data.engine'),
        TextDyField.data_source('Engine Version', 'data.engine_version', options={
            'is_optional': True
        }),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['available'],
            'warning': ['creating', 'deleting', 'maintenance', 'modifying', 'rebooting',
                        'renaming', 'starting', 'stopping', 'upgrading'],
            'alert': ['failed', 'inaccessible-encryption-credentials', 'restore-error', 'stopped', 'storage-full']
        }),
        TextDyField.data_source('Size', 'data.size'),
        TextDyField.data_source('Region & AZ', 'data.availability_zone'),
        TextDyField.data_source('Multi-AZ', 'data.multi_az'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Auto Minor Version Upgrade', 'data.auto_minor_version_upgrade', options={
            'is_optional': True
        }),
        TextDyField.data_source('Preferred Maintenance Window', 'data.preferred_maintenance_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('Deletion Protection', 'data.deletion_protection', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Role', key='data.role',
                        enums={
                            'cluster': {'label': 'Cluster'},
                            'instance': {'label': 'Instance'},
                        }),
        SearchField.set(name='Status', key='data.status',
                        enums={
                            "available": {'label': 'Available', 'icon': {'color': 'green.500'}},
                            "creating": {'label': 'Creating', 'icon': {'color': 'yellow.400'}},
                            "deleting": {'label': 'Deleting', 'icon': {'color': 'yellow.400'}},
                            "maintenance": {'label': 'Maintenance', 'icon': {'color': 'yellow.400'}},
                            "modifying": {'label': 'Modifying', 'icon': {'color': 'yellow.400'}},
                            "rebooting": {'label': 'Rebooting', 'icon': {'color': 'yellow.400'}},
                            "renaming": {'label': 'Renaming', 'icon': {'color': 'yellow.400'}},
                            "starting": {'label': 'Starting', 'icon': {'color': 'yellow.400'}},
                            "stopping": {'label': 'Stopping', 'icon': {'color': 'yellow.400'}},
                            "upgrading": {'label': 'Upgrading', 'icon': {'color': 'yellow.400'}},
                            "failed": {'label': 'Failed', 'icon': {'color': 'red.500'}},
                            "inaccessible-encryption-credentials": {'label': 'Inaccessible Encryption Credentials',
                                                                    'icon': {'color': 'red.500'}},
                            "restore-error": {'label': 'Restore Error', 'icon': {'color': 'red.500'}},
                            "stopped": {'label': 'Stopped', 'icon': {'color': 'red.500'}},
                            "storage-full": {'label': 'Storage Full', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Engine', key='data.engine'),
        SearchField.set(name='Engine Version', key='data.engine_version'),
        SearchField.set(name='Cluster member counts', key='data.cluster.db_cluster_member_counts'),
        SearchField.set(name='Instance Class', key='data.instance.db_instance_class'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='Multi AZ', key='data.multi_az', data_type='boolean'),
        SearchField.set(name='Cluster Endpoint', key='data.cluster.endpoint'),
        SearchField.set(name='Cluster Reader Endpoint', key='data.cluster.reader_endpoint'),
        SearchField.set(name='Cluster Custom Endpoint', key='data.cluster.custom_endpoints'),
        SearchField.set(name='Cluster Port', key='data.cluster.port', data_type='integer'),
        SearchField.set(name='Instance Endpoint', key='data.instance.endpoint.address'),
        SearchField.set(name='Auto Minor Version Upgrade', key='data.cluster.auto_minor_version_upgrade'),
        SearchField.set(name='Preferred Maintenance Window', key='data.preferred_maintenance_window'),
        SearchField.set(name='Deletion Protection', key='data.deletion_protection'),
        SearchField.set(name='Instance Port', key='data.instance.endpoint.port', data_type='integer'),
        SearchField.set(name='AWS Account ID', key='account'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(database_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(database_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(database_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(database_count_by_engine_conf))
    ]
)

'''
Instance
'''
instance_total_count_conf = os.path.join(current_dir, 'widget/instance_total_count.yaml')
instance_storage_total_size_conf = os.path.join(current_dir, 'widget/instance_storage_total_size.yaml')
instance_count_by_region_conf = os.path.join(current_dir, 'widget/instance_count_by_region.yaml')
instance_count_by_account_conf = os.path.join(current_dir, 'widget/instance_count_by_account.yaml')
instance_storage_total_size_by_account_conf = os.path.join(current_dir, 'widget/instance_storage_total_size_by_account.yaml')
instance_count_by_instance_type_conf = os.path.join(current_dir, 'widget/instance_count_by_instance_type.yaml')

cst_rds_instance = CloudServiceTypeResource()
cst_rds_instance.name = 'Instance'
cst_rds_instance.provider = 'aws'
cst_rds_instance.group = 'RDS'
cst_rds_instance.labels = ['Database']
cst_rds_instance.service_code = 'AmazonRDS'
cst_rds_instance.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-RDS.svg',
}

cst_rds_instance._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Engine', 'data.engine'),
        EnumDyField.data_source('Status', 'data.db_instance_status', default_state={
            'safe': ['available'],
            'warning': ['creating', 'deleting', 'maintenance', 'modifying', 'rebooting',
                        'renaming', 'starting', 'stopping', 'upgrading'],
            'alert': ['failed', 'inaccessible-encryption-credentials', 'restore-error', 'stopped', 'storage-full']
        }),
        TextDyField.data_source('Instance Class', 'data.db_instance_class'),
        TextDyField.data_source('VPC ID', 'data.db_subnet_group.vpc_id'),
        TextDyField.data_source('Availability Zone', 'data.availability_zone'),
        TextDyField.data_source('Multi-AZ', 'data.multi_az'),
        TextDyField.data_source('ARN', 'data.db_instance_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Engine Version', 'data.engine_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Storage Type', 'data.storage_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Endpoint Address', 'data.endpoint.address', options={
            'is_optional': True
        }),
        TextDyField.data_source('Endpoint Port', 'data.endpoint.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Publicly Accessible', 'data.publicly_accessible', options={
            'is_optional': True
        }),
        TextDyField.data_source('IAM Database Authentication Enabled', 'data.iam_database_authentication_enabled',
                                options={
                                    'is_optional': True
                                }),
        TextDyField.data_source('Master Username', 'data.master_username', options={
            'is_optional': True
        }),
        TextDyField.data_source('CA Certificate Identifier', 'data.ca_certificate_identifier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Hosted Zone ID', 'data.endpoint.hosted_zone_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Deletion Protection', 'data.deletion_protection', options={
            'is_optional': True
        }),
        TextDyField.data_source('VPC ID', 'data.db_subnet_group.vpc_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Group Name', 'data.db_subnet_group.db_subnet_group_name', options={
            'is_optional': True
        }),
        ListDyField.data_source('Subnet IDs', 'data.db_subnet_group.subnets', options={
            'delimiter': '<br>',
            'sub_key': 'subnet_identifier',
            'is_optional': True
        }),
        ListDyField.data_source('Availability Zones', 'data.db_subnet_group.subnets', options={
            'delimiter': '<br>',
            'sub_key': 'subnet_availability_zone.name',
            'is_optional': True
        }),
        ListDyField.data_source('Security Group IDs', 'data.vpc_security_groups', options={
            'delimiter': '<br>',
            'sub_key': 'vpc_security_group_id',
            'is_optional': True
        }),
        TextDyField.data_source('Monitoring Interval', 'data.monitoring_interval', options={
            'is_optional': True
        }),
        TextDyField.data_source('Auto Minor Version Upgrade', 'data.auto_minor_version_upgrade', options={
            'is_optional': True
        }),
        ListDyField.data_source('DB Parameter Group Names', 'data.db_parameter_groups', options={
            'delimiter': '<br>',
            'sub_key': 'db_parameter_group_name',
            'is_optional': True
        }),
        TextDyField.data_source('License Model', 'data.license_model', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Retention Period', 'data.backup_retention_period', options={
            'is_optional': True
        }),
        TextDyField.data_source('DBI Resource ID', 'data.dbi_resource_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Storage Encrypted', 'data.storage_encrypted', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allocated Storage', 'data.allocated_storage', options={
            'is_optional': True
        }),
        TextDyField.data_source('Max Allocated Storage', 'data.max_allocated_storage', options={
            'is_optional': True
        }),
        TextDyField.data_source('Multi AZ', 'data.multi_az', options={
            'is_optional': True
        }),
        TextDyField.data_source('Preferred Backup Window', 'data.preferred_backup_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('Preferred Maintenance Window', 'data.preferred_maintenance_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('DB Name', 'data.db_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Performance Insights Enabled', 'data.performance_insights_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.db_instance_arn'),
        SearchField.set(name='Status', key='data.db_instance_status',
                        enums={
                            "available": {'label': 'Available', 'icon': {'color': 'green.500'}},
                            "creating": {'label': 'Creating', 'icon': {'color': 'yellow.400'}},
                            "deleting": {'label': 'Deleting', 'icon': {'color': 'yellow.400'}},
                            "maintenance": {'label': 'Maintenance', 'icon': {'color': 'yellow.400'}},
                            "modifying": {'label': 'Modifying', 'icon': {'color': 'yellow.400'}},
                            "rebooting": {'label': 'Rebooting', 'icon': {'color': 'yellow.400'}},
                            "renaming": {'label': 'Renaming', 'icon': {'color': 'yellow.400'}},
                            "starting": {'label': 'Starting', 'icon': {'color': 'yellow.400'}},
                            "stopping": {'label': 'Stopping', 'icon': {'color': 'yellow.400'}},
                            "upgrading": {'label': 'Upgrading', 'icon': {'color': 'yellow.400'}},
                            "failed": {'label': 'Failed', 'icon': {'color': 'red.500'}},
                            "inaccessible-encryption-credentials": {'label': 'Inaccessible Encryption Credentials',
                                                                    'icon': {'color': 'red.500'}},
                            "restore-error": {'label': 'Restore Error', 'icon': {'color': 'red.500'}},
                            "stopped": {'label': 'Stopped', 'icon': {'color': 'red.500'}},
                            "storage-full": {'label': 'Storage Full', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Engine', key='data.engine'),
        SearchField.set(name='Engine Version', key='data.engine_version'),
        SearchField.set(name='Instance Class', key='data.db_instance_class'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='Multi AZ', key='data.multi_az', data_type='boolean'),
        SearchField.set(name='Endpoint Address', key='data.endpoint.address'),
        SearchField.set(name='Endpoint Port', key='data.endpoint.port', data_type='integer'),
        SearchField.set(name='Auto Minor Version Upgrade', key='data.auto_minor_version_upgrade'),
        SearchField.set(name='Deletion Protection', key='data.deletion_protection'),
        SearchField.set(name='Preferred Maintenance Window', key='data.preferred_maintenance_window'),
        SearchField.set(name='AWS Account ID', key='account'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(instance_storage_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(instance_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(instance_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(instance_storage_total_size_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(instance_count_by_instance_type_conf))
    ]
)


'''
Snapshot
'''
snapshot_total_count_conf = os.path.join(current_dir, 'widget/snapshot_total_count.yaml')
snapshot_total_size_conf = os.path.join(current_dir, 'widget/snapshot_total_size.yaml')
snapshot_count_by_region_conf = os.path.join(current_dir, 'widget/snapshot_count_by_region.yaml')
snapshot_count_by_az_conf = os.path.join(current_dir, 'widget/snapshot_count_by_az.yaml')
snapshot_count_by_account_conf = os.path.join(current_dir, 'widget/snapshot_count_by_account.yaml')
snapshot_storage_total_size_by_account_conf = os.path.join(current_dir, 'widget/snapshot_storage_total_size_by_account.yaml')
snapshot_count_by_engine_conf = os.path.join(current_dir, 'widget/snapshot_count_by_engine.yaml')

cst_rds_snapshot = CloudServiceTypeResource()
cst_rds_snapshot.name = 'Snapshot'
cst_rds_snapshot.provider = 'aws'
cst_rds_snapshot.group = 'RDS'
cst_rds_snapshot.labels = ['Database']
cst_rds_snapshot.service_code = 'AmazonRDS'
cst_rds_snapshot.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-RDS.svg',
}
cst_rds_snapshot._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('DB Type', 'data.db_type', default_badge={
            'indigo.500': ['instance'], 'coral.600': ['cluster']
        }),
        TextDyField.data_source('DB Instance/Cluster', 'data.db_identifier'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'warning': ['creating', 'deleting'],
            'safe': ['available'],
        }),
        TextDyField.data_source('Snapshot Type', 'data.snapshot_type'),
        TextDyField.data_source('Engine', 'data.engine'),
        TextDyField.data_source('AZ', 'data.availability_zone'),
        EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        DateTimeDyField.data_source('Snapshot Creation Time', 'data.snapshot_create_time'),
        TextDyField.data_source('ARN', 'data.db_snapshot_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Engine Version', 'data.engine_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Storage Type', 'data.storage_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('IOPS', 'data.iops', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allocated Storage', 'data.allocated_storage', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS ID', 'data.kms_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('DB Resource ID', 'data.db_resource_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Option Group Name', 'data.option_group_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('License Model', 'data.license_model', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.db_snapshot_arn'),
        SearchField.set(name='DB Instance Identifier', key='data.db_identifier'),
        SearchField.set(name='Engine', key='data.engine'),
        SearchField.set(name='Allocated Storage', key='data.allocated_storage', data_type='integer'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Created Time', key='data.snapshot_create_time', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='account'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(snapshot_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(snapshot_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_count_by_az_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_storage_total_size_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_count_by_engine_conf))
    ]
)

'''
SubnetGroup
'''
cst_rds_subnetgrp = CloudServiceTypeResource()
cst_rds_subnetgrp.name = 'SubnetGroup'
cst_rds_subnetgrp.provider = 'aws'
cst_rds_subnetgrp.group = 'RDS'
cst_rds_subnetgrp.labels = ['Database']
cst_rds_subnetgrp.service_code = 'AmazonRDS'
cst_rds_subnetgrp.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-RDS.svg',
}
cst_rds_subnetgrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Description', 'data.db_subnet_group_description'),
        EnumDyField.data_source('Status', 'data.subnet_group_status', default_state={
            'safe': ['Complete']
        }),
        TextDyField.data_source('VPC', 'data.vpc_id'),
        TextDyField.data_source('ARN', 'data.db_subnet_group_arn', options={
            'is_optional': True
        }),
        ListDyField.data_source('Subnet IDs', 'data.subnets', options={
            'sub_key': 'subnet_identifier',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Availability Zones', 'data.subnets', options={
            'sub_key': 'subnet_availability_zone.name',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.db_subnet_group_arn'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Subnet ID', key='data.subnets.subnet_identifier'),
        SearchField.set(name='Availability Zone', key='data.subnets.subnet_availability_zone'),
        SearchField.set(name='AWS Account ID', key='account'),
    ]
)

'''
Parameter Group
'''
cst_rds_paramgrp = CloudServiceTypeResource()
cst_rds_paramgrp.name = 'ParameterGroup'
cst_rds_paramgrp.provider = 'aws'
cst_rds_paramgrp.group = 'RDS'
cst_rds_paramgrp.labels = ['Database']
cst_rds_paramgrp.service_code = 'AmazonRDS'
cst_rds_paramgrp.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-RDS.svg',
}
cst_rds_paramgrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Family', 'data.db_parameter_group_family'),
        TextDyField.data_source('Description', 'data.description'),
        TextDyField.data_source('ARN', 'data.db_parameter_group_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Type', 'data.db_parameter_group_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.db_parameter_group_arn'),
        SearchField.set(name='Family', key='data.db_parameter_group_family'),
        SearchField.set(name='AWS Account ID', key='account'),
    ]
)

'''
OptionGroup
'''
cst_rds_optgrp = CloudServiceTypeResource()
cst_rds_optgrp.name = 'OptionGroup'
cst_rds_optgrp.provider = 'aws'
cst_rds_optgrp.group = 'RDS'
cst_rds_optgrp.labels = ['Database']
cst_rds_optgrp.service_code = 'AmazonRDS'
cst_rds_optgrp.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-RDS.svg',
}
cst_rds_optgrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Description', 'data.option_group_description'),
        TextDyField.data_source('Engine', 'data.engine_name'),
        TextDyField.data_source('Engine version', 'data.major_engine_version'),
        TextDyField.data_source('ARN', 'data.option_group_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allows VPC and Non VPC Instance Memberships',
                                'data.allows_vpc_and_non_vpc_instance_memberships',
                                options={'is_optional': True}),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.option_group_arn'),
        SearchField.set(name='Engine', key='data.engine_name'),
        SearchField.set(name='Major Engine Version', key='data.major_engine_version'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='AWS Account ID', key='account'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_rds_database}),
    CloudServiceTypeResponse({'resource': cst_rds_instance}),
    CloudServiceTypeResponse({'resource': cst_rds_snapshot}),
    CloudServiceTypeResponse({'resource': cst_rds_subnetgrp}),
    CloudServiceTypeResponse({'resource': cst_rds_paramgrp}),
    CloudServiceTypeResponse({'resource': cst_rds_optgrp}),
]
