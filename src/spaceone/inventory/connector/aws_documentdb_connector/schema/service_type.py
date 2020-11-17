from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_cluster = CloudServiceTypeResource()
cst_cluster.name = 'Cluster'
cst_cluster.provider = 'aws'
cst_cluster.group = 'DocumentDB'
cst_cluster.labels = ['Database']
cst_cluster.is_primary = True
cst_cluster.is_major = True
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
        EnumDyField.data_source('Engine', 'data.engine', default_outline_badge=['docdb']),
        TextDyField.data_source('Version', 'data.engine_version'),
        TextDyField.data_source('Instances', 'data.instance_count'),
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
cst_parameter_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
}
cst_parameter_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.db_cluster_parameter_group_name'),
        BadgeDyField.data_source('Family', 'data.db_parameter_group_family'),
        TextDyField.data_source('Description', 'data.description'),
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