from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, \
    BadgeDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_rds_database = CloudServiceTypeResource()
cst_rds_database.name = 'Database'
cst_rds_database.provider = 'aws'
cst_rds_database.group = 'RDS'
cst_rds_database.labels = ['Database']
cst_rds_database.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'true',
}

cst_rds_database._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
    ],
    search=[
        SearchField.set(name='DB Identifier', key='data.db_identifier'),
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
        SearchField.set(name='Size', key='data.size'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='Multi AZ', key='data.multi_az', data_type='boolean'),
        SearchField.set(name='Cluster Endpoint', key='data.cluster.endpoint'),
        SearchField.set(name='Cluster Reader Endpoint', key='data.cluster.reader_endpoint'),
        SearchField.set(name='Cluster Custom Endpoint', key='data.cluster.custom_endpoints'),
        SearchField.set(name='Cluster Port', key='data.cluster.port', data_type='integer'),
        SearchField.set(name='Instance Endpoint', key='data.instance.endpoint'),
        SearchField.set(name='Instance Port', key='data.instance.db_instance_port', data_type='integer'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_rds_snapshot = CloudServiceTypeResource()
cst_rds_snapshot.name = 'Snapshot'
cst_rds_snapshot.provider = 'aws'
cst_rds_snapshot.group = 'RDS'
cst_rds_snapshot.labels = ['Database']
cst_rds_snapshot.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_snapshot._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
    ],
    search=[
        SearchField.set(name='Snapshot Identifier', key='data.db_snapshot_identifier'),
        SearchField.set(name='ARN', key='data.db_snapshot_arn'),
        SearchField.set(name='DB Instance Identifier', key='data.db_instance_identifier'),
        SearchField.set(name='Engine', key='data.engine'),
        SearchField.set(name='Allocated Storage', key='data.allocated_storage', data_type='integer'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Created Time', key='data.snapshot_create_time', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_rds_subnetgrp = CloudServiceTypeResource()
cst_rds_subnetgrp.name = 'SubnetGroup'
cst_rds_subnetgrp.provider = 'aws'
cst_rds_subnetgrp.group = 'RDS'
cst_rds_subnetgrp.labels = ['Database']
cst_rds_subnetgrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_subnetgrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_subnet_group_name'),
        TextDyField.data_source('Description', 'data.db_subnet_group_description'),
        EnumDyField.data_source('Status', 'data.subnet_group_status', default_state={
            'safe': ['Complete']
        }),
        TextDyField.data_source('VPC', 'data.vpc_id'),
    ],
    search=[
        SearchField.set(name='Name', key='data.db_subnet_group_name'),
        SearchField.set(name='ARN', key='data.db_subnet_group_arn'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Subnet ID', key='data.subnets.subnet_identifier'),
        SearchField.set(name='Availability Zone', key='data.subnets.subnet_availability_zone'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_rds_paramgrp = CloudServiceTypeResource()
cst_rds_paramgrp.name = 'ParameterGroup'
cst_rds_paramgrp.provider = 'aws'
cst_rds_paramgrp.group = 'RDS'
cst_rds_paramgrp.labels = ['Database']
cst_rds_paramgrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_paramgrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_parameter_group_name'),
        BadgeDyField.data_source('Family', 'data.db_parameter_group_family'),
        TextDyField.data_source('Description', 'data.description'),
    ],
    search=[
        SearchField.set(name='Name', key='data.db_parameter_group_name'),
        SearchField.set(name='ARN', key='data.db_parameter_group_arn'),
        SearchField.set(name='Family', key='data.db_parameter_group_family'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_rds_optgrp = CloudServiceTypeResource()
cst_rds_optgrp.name = 'OptionGroup'
cst_rds_optgrp.provider = 'aws'
cst_rds_optgrp.group = 'RDS'
cst_rds_optgrp.labels = ['Database']
cst_rds_optgrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-RDS.svg',
    'spaceone:is_major': 'false',
}
cst_rds_optgrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_parameter_group_name'),
        TextDyField.data_source('Description', 'data.description'),
        EnumDyField.data_source('Engine', 'data.engine_name',
                                default_outline_badge=['aurora', 'mysql', 'mariadb', 'postgres', 'oracle-ee', 'oracle-se',
                                                       'oracle-se1', 'oracle-se2', 'sqlserver-ex', 'sqlserver-web',
                                                       'sqlserver-se', 'sqlserver-ee']),
        TextDyField.data_source('Engine version', 'data.major_engine_version'),
    ],
    search=[
        SearchField.set(name='Name', key='data.option_group_name'),
        SearchField.set(name='ARN', key='data.option_group_arn'),
        SearchField.set(name='Engine', key='data.engine_name'),
        SearchField.set(name='Major Engine Version', key='data.major_engine_version'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_rds_database}),
    CloudServiceTypeResponse({'resource': cst_rds_snapshot}),
    CloudServiceTypeResponse({'resource': cst_rds_subnetgrp}),
    CloudServiceTypeResponse({'resource': cst_rds_paramgrp}),
    CloudServiceTypeResponse({'resource': cst_rds_optgrp}),
]
