from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_cluster = CloudServiceTypeResource()
cst_cluster.name = 'Cluster'
cst_cluster.provider = 'aws'
cst_cluster.group = 'DocumentDB'
cst_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
    'spaceone:is_major': 'true',
}
cst_cluster._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


cst_subnet_group = CloudServiceTypeResource()
cst_subnet_group.name = 'SubnetGroup'
cst_subnet_group.provider = 'aws'
cst_subnet_group.group = 'DocumentDB'
cst_subnet_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
    'spaceone:is_major': 'false',
}
cst_subnet_group._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.db_subnet_group_name'),
    EnumDyField.data_source('Status', 'data.subnet_group_status', default_state={
        'safe': ['Complete']
    }),
    TextDyField.data_source('Description', 'data.db_subnet_group_description'),
    TextDyField.data_source('VPC', 'data.vpc_id'),
])


cst_parameter_group = CloudServiceTypeResource()
cst_parameter_group.name = 'ParameterGroup'
cst_parameter_group.provider = 'aws'
cst_parameter_group.group = 'DocumentDB'
cst_parameter_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-DocumentDB.svg',
    'spaceone:is_major': 'false',
}
cst_parameter_group._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.db_cluster_parameter_group_name'),
    BadgeDyField.data_source('Family', 'data.db_parameter_group_family'),
    TextDyField.data_source('Description', 'data.description'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cluster}),
    CloudServiceTypeResponse({'resource': cst_subnet_group}),
    CloudServiceTypeResponse({'resource': cst_parameter_group}),
]