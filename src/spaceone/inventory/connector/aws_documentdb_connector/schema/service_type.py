from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField, SearchField, \
    DateTimeDyField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_cluster = CloudServiceTypeResource()
cst_cluster.name = 'Cluster'
cst_cluster.provider = 'aws'
cst_cluster.group = 'DocumentDB'
cst_cluster.labels = ['Database']
cst_cluster.is_primary = True
cst_cluster.is_major = True
cst_cluster.service_code = 'AmazonDocDB'
cst_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
}
cst_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Cluster', 'data.db_cluster_identifier'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['available'],
            'warning': ['maintenance', 'backing-up', 'creating', 'migrating', 'modifying', 'renaming',
                        'resetting-master-credentials', 'upgrading'],
            'alert': ['deleting', 'failing-over', 'inaccessible-encryption-credentials', 'migration-failed']
        }),
        TextDyField.data_source('Engine', 'data.engine'),
        TextDyField.data_source('Version', 'data.engine_version'),
        TextDyField.data_source('Instances', 'data.instance_count'),
        # For Dynamic Table
        TextDyField.data_source('DB Cluster ARN', 'data.db_cluster_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('DB Cluster Resource ID', 'data.db_cluster_resource_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Endpoint', 'data.endpoint', options={
            'is_optional': True
        }),
        TextDyField.data_source('Reader Endpoint', 'data.reader_endpoint', options={
            'is_optional': True
        }),
        TextDyField.data_source('Port', 'data.port', options={
            'is_optional': True
        }),
        TextDyField.data_source('Multi AZ', 'data.multi_az', options={
            'is_optional': True
        }),
        ListDyField.data_source('Availability Zones', 'data.availability_zones', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Instances ARN', 'data.instances', options={
            'delimiter': '<br>',
            'sub_key': 'db_instance_arn',
            'is_optional': True
        }),
        ListDyField.data_source('Instances Identifier', 'data.instances', options={
            'delimiter': '<br>',
            'sub_key': 'db_instance_identifier',
            'is_optional': True
        }),
        ListDyField.data_source('Instances Availability Zone', 'data.instances', options={
            'delimiter': '<br>',
            'sub_key': 'availability_zone',
            'is_optional': True
        }),
        ListDyField.data_source('Instances Type', 'data.instances', options={
            'delimiter': '<br>',
            'sub_key': 'db_instance_class',
            'is_optional': True
        }),
        TextDyField.data_source('DB Cluster Parameter Group', 'data.parameter_group', options={
            'is_optional': True
        }),
        TextDyField.data_source('Parameter Group', 'data.db_cluster_parameter_group', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subnet Group', 'data.subnet_group', options={
            'is_optional': True
        }),
        TextDyField.data_source('DB Subnet Group', 'data.db_subnet_group', options={
            'is_optional': True
        }),
        TextDyField.data_source('Master Username', 'data.master_username', options={
            'is_optional': True
        }),
        TextDyField.data_source('Storage Encrypted', 'data.storage_encrypted', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Deletion Protection', 'data.deletion_protection', options={
            'is_optional': True
        }),
        TextDyField.data_source('Preferred Maintenance Window', 'data.preferred_maintenance_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('Preferred Backup Window', 'data.preferred_backup_window', options={
            'is_optional': True
        }),
        TextDyField.data_source('Backup Retention Period', 'data.backup_retention_period', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Latest Restorable Time', 'data.latest_restorable_time', options={
            'is_optional': True
        }),
        TextDyField.data_source('Hosted Zone ID', 'data.hosted_zone_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Security Groups', 'data.vpc_security_groups', options={
            'delimiter': '<br>',
            'sub_key': 'vpc_security_group_id',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Cluster', key='data.db_cluster_identifier'),
        SearchField.set(name='ARN', key='data.db_cluster_arn'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Engine', key='data.engine'),
        SearchField.set(name='Version', key='data.engine_version'),
        SearchField.set(name='Cluster Endpoint', key='data.endpoint'),
        SearchField.set(name='Cluster Read Endpoint', key='data.reader_endpoint'),
        SearchField.set(name='Port', key='data.port', data_type='integer'),
        SearchField.set(name='Cluster Parameter Group', key='data.db_cluster_parameter_group'),
        SearchField.set(name='Deletion Protection', key='data.deletion_protection', data_type='boolean'),
        SearchField.set(name='Avaiilability Zone', key='data.availability_zones'),
        SearchField.set(name='Security Group ID', key='data.vpc_security_groups.vpc_security_group_id'),
        SearchField.set(name='Instance', key='data.instances.db_instance_identifier'),
        SearchField.set(name='Instance Type', key='data.instances.db_instance_class'),
        SearchField.set(name='VPC ID', key='data.instances.db_subnet_group.vpc_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
        SearchField.set(name='Creation Time', key='data.cluster_create_time', data_type='datetime'),
    ]
)


cst_subnet_group = CloudServiceTypeResource()
cst_subnet_group.name = 'SubnetGroup'
cst_subnet_group.provider = 'aws'
cst_subnet_group.group = 'DocumentDB'
cst_subnet_group.labels = ['Database']
cst_subnet_group.service_code = 'AmazonDocDB'
cst_subnet_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
}
cst_subnet_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_subnet_group_name'),
        EnumDyField.data_source('Status', 'data.subnet_group_status', default_state={
            'safe': ['Complete']
        }),
        TextDyField.data_source('Description', 'data.db_subnet_group_description'),
        TextDyField.data_source('VPC', 'data.vpc_id'),
        TextDyField.data_source('Subnet Group ARN', 'data.db_subnet_group_arn', options={
            'is_optional': True
        }),
        ListDyField.data_source('Subnet Identifier', 'data.subnets', options={
            'delimeter': '<br>',
            'sub_key': 'subnet_identifier',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Name', key='data.db_subnet_group_name'),
        SearchField.set(name='ARN', key='data.db_subnet_group_arn'),
        SearchField.set(name='Status', key='data.subnet_group_status'),
        SearchField.set(name='Subnet ID', key='data.subnets.subnet_identifier'),
        SearchField.set(name='Availability Zone', key='data.subnets.subnet_availability_zone'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_parameter_group = CloudServiceTypeResource()
cst_parameter_group.name = 'ParameterGroup'
cst_parameter_group.provider = 'aws'
cst_parameter_group.group = 'DocumentDB'
cst_parameter_group.labels = ['Database']
cst_parameter_group.service_code = 'AmazonDocDB'
cst_parameter_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
}
cst_parameter_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_cluster_parameter_group_name'),
        TextDyField.data_source('Family', 'data.db_parameter_group_family'),
        TextDyField.data_source('Description', 'data.description'),
        TextDyField.data_source('Parameter Group ARN', 'data.db_cluster_parameter_group_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Name', key='data.db_cluster_parameter_group_name'),
        SearchField.set(name='ARN', key='data.db_cluster_parameter_group_arn'),
        SearchField.set(name='Family', key='data.db_parameter_group_family'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cluster}),
    CloudServiceTypeResponse({'resource': cst_subnet_group}),
    CloudServiceTypeResponse({'resource': cst_parameter_group}),
]