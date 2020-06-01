from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    BadgeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_rds_database = CloudServiceTypeResource()
cst_rds_database.name = 'Database'
cst_rds_database.provider = 'aws'
cst_rds_database.group = 'RDS'
cst_rds_database.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'true',
}

cst_rds_database._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('DB Identifier', 'data.db_identifier'),
    EnumDyField.data_source('Role', 'data.role', default_badge={
        'indigo.500': ['cluster'], 'coral.600': ['instance']
    }),
    EnumDyField.data_source('Engine', 'data.engine',
                            default_outline_badge=['aurora', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                   'oracle-se1', 'oracle-se2','sqlserver-ex', 'sqlserver-web',
                                                   'sqlserver-se', 'sqlserver-ee']),
    TextDyField.data_source('Size', 'data.size'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['available'],
        'warning': ['creating', 'deleting', 'maintenance', 'modifying', 'rebooting',
                    'renaming', 'starting', 'stopping', 'upgrading'],
        'alert': ['failed', 'inaccessible-encryption-credentials', 'restore-error', 'stopped', 'storage-full']
    }),
    TextDyField.data_source('VPC', 'data.vpc_id'),
    TextDyField.data_source('Region & AZ', 'data.availability_zone'),
    EnumDyField.data_source('Multi-AZ', 'data.multi_az', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Maintenance', 'data.maintenance'),
])

cst_rds_snapshot = CloudServiceTypeResource()
cst_rds_snapshot.name = 'Snapshot'
cst_rds_snapshot.provider = 'aws'
cst_rds_snapshot.group = 'RDS'
cst_rds_snapshot.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_snapshot._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Snapshot', 'data.db_snapshot_identifier'),
    TextDyField.data_source('DB Instance', 'data.db_instance_identifier'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['available'],
    }),
    TextDyField.data_source('Progress (%)', 'data.percent_progress'),
    EnumDyField.data_source('Type', 'data.snapshot_type', default_outline_badge=['manual', 'automated']),
    EnumDyField.data_source('Engine', 'data.engine',
                            default_outline_badge=['aurora', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                   'oracle-se1', 'oracle-se2', 'sqlserver-ex', 'sqlserver-web',
                                                   'sqlserver-se', 'sqlserver-ee']),
    TextDyField.data_source('AZ', 'data.availability_zone'),
    EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Snapshot Creation Time', 'data.snapshot_create_time'),
])

cst_rds_subnetgrp = CloudServiceTypeResource()
cst_rds_subnetgrp.name = 'SubnetGroup'
cst_rds_subnetgrp.provider = 'aws'
cst_rds_subnetgrp.group = 'RDS'
cst_rds_subnetgrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_subnetgrp._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.db_subnet_group_name'),
    TextDyField.data_source('Description', 'data.db_subnet_group_description'),
    EnumDyField.data_source('Status', 'data.subnet_group_status', default_state={
        'safe': ['Complete']
    }),
    TextDyField.data_source('VPC', 'data.vpc_id'),
])

cst_rds_paramgrp = CloudServiceTypeResource()
cst_rds_paramgrp.name = 'ParameterGroup'
cst_rds_paramgrp.provider = 'aws'
cst_rds_paramgrp.group = 'RDS'
cst_rds_paramgrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_paramgrp._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.db_parameter_group_name'),
    BadgeDyField.data_source('Family', 'data.db_parameter_group_family'),
    TextDyField.data_source('Description', 'data.description'),
])

cst_rds_optgrp = CloudServiceTypeResource()
cst_rds_optgrp.name = 'OptionGroup'
cst_rds_optgrp.provider = 'aws'
cst_rds_optgrp.group = 'RDS'
cst_rds_optgrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_optgrp._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.db_parameter_group_name'),
    TextDyField.data_source('Description', 'data.description'),
    EnumDyField.data_source('Engine', 'data.engine_name',
                            default_outline_badge=['aurora', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                   'oracle-se1', 'oracle-se2', 'sqlserver-ex', 'sqlserver-web',
                                                   'sqlserver-se', 'sqlserver-ee']),
    TextDyField.data_source('Engine version', 'data.major_engine_version'),
])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_rds_database}),
    CloudServiceTypeResponse({'resource': cst_rds_snapshot}),
    CloudServiceTypeResponse({'resource': cst_rds_subnetgrp}),
    CloudServiceTypeResponse({'resource': cst_rds_paramgrp}),
    CloudServiceTypeResponse({'resource': cst_rds_optgrp}),
]
