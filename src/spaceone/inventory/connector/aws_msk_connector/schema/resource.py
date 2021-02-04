from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_msk_connector.schema.data import Configuration, Cluster
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout, \
    SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
CLUSTERS
'''
# Base
cluster_base = ItemDynamicLayout.set_fields('Base', fields=[
    TextDyField.data_source('ARN', 'data.cluster_arn'),
    TextDyField.data_source('Name', 'data.cluster_name'),
    DateTimeDyField.data_source('Created Time', 'data.creation_time'),
    TextDyField.data_source('Current Version', 'data.current_version'),
    TextDyField.data_source('Enhanced Monitoring', 'data.enhanced_monitoring'),
    TextDyField.data_source('Number of Broker Nodes', 'data.number_of_broker_nodes'),
    TextDyField.data_source('Zookeeper Connect String', 'data.zookeeper_connect_string'),
])

# Broker  Summary Info
cluster_broker_node_summary = ItemDynamicLayout.set_fields('Broker Summary Info',
                                                           root_path='data.broker_node_group_info',
                                                           fields=[
                                                               TextDyField.data_source('Broker AZ Distribution',
                                                                                       'broker_az_distribution'),
                                                               ListDyField.data_source('Client Subnet',
                                                                                       'client_subnets',
                                                                                       options={
                                                                                           'delimiter': '<br>'
                                                                                       }),
                                                               ListDyField.data_source('Security Group',
                                                                                       'security_group',
                                                                                       options={
                                                                                           'delimiter': '<br>'
                                                                                       }),
                                                               TextDyField.data_source('EBS storage volume per broker',
                                                                                       'storage_info.ebs_storage_info.volume_size'),
                                                           ])

# Broker  Info
cluster_broker_node_info = TableDynamicLayout.set_fields('Broker Node Info', root_path='data.node_info_list', fields=[
    TextDyField.data_source('Instance Type', 'instance_type'),
    TextDyField.data_source('Node Type', 'node_type'),
    TextDyField.data_source('Node ARN', 'node_arn'),
    TextDyField.data_source('Added To Cluster Time', 'added_to_cluster_time'),
    TextDyField.data_source('Broker ID', 'broker_node_info.broker_id'),
    ListDyField.data_source('Endpoints', 'broker_node_info.endpoints',
                            options={
                                'delimiter': '<br>'
                            }),
    TextDyField.data_source('Client Subnet', 'broker_node_info.client_subnet'),
    TextDyField.data_source('Client VPC IP', 'broker_node_info.client_vpc_ip_address'),
])

broker_info = ListDynamicLayout.set_layouts('Broker', layouts=[cluster_broker_node_summary, cluster_broker_node_info])

# Encryption Info
cluster_encryption_info = ItemDynamicLayout.set_fields('Encryption Info', root_path='data.encryption_info', fields=[
    EnumDyField.data_source('Within the cluster', 'encryption_at_rest.in_cluster',
                            default_badge={'indigo.500': ['true'],
                                           'coral.600': ['false'],
                                           }),
    TextDyField.data_source('Between Client & Broker',
                            'encryption_in_transit.data_volume_kms_key_id'),
])
'''
# Broker Node Info
cluster_broker_node_info = TableDynamicLayout.set_fields('Broker Node Info', root_path='data.node_info_list', fields=[
                                        TextDyField.data_source('Broker ID', 'broker_node_info.broker_id'),
                                        ListDyField.data_source('Endpoints', 'broker_node_info.endpoints',
                                                                default_badge={'type': 'outline',
                                                                               'delimiter': '<br>'}),
                                        TextDyField.data_source('Client Subnet', 'broker_node_info.client_subnet'),
                                        TextDyField.data_source('Client VPC IP','broker_node_info.client_vpc_ip_address'),
                                        TextDyField.data_source('')
])
'''

cluster_client_authentication = \
    ItemDynamicLayout.set_fields('Client Authentication',
                                 root_path='data.client_authentication', fields=[
            EnumDyField.data_source('Sasl scram', 'sasl.scram',
                                    default_badge={
                                        'indigo.500': ['true'],
                                        'coral.600': ['false'],
                                    }),
            ListDyField.data_source(
                'Tls CertificateAuthorityArnList',
                'tls.certificate_authority_arn_list',
                options={
                    'delimiter': '<br>'
                }),
        ])

cluster_broker_cloudwatchlogs = \
    ItemDynamicLayout.set_fields('CloudWatch Logs',
                                 root_path='data.logging_info.broker_logs.cloud_watch_logs',
                                 fields=[
                                     EnumDyField.data_source('Enabled', 'enabled',
                                                             default_badge={
                                                                 'indigo.500': ['true'],
                                                                 'coral.600': ['false'],
                                                             }),
                                     TextDyField.data_source('Log Group', 'log_group')
                                 ])

cluster_broker_firehose = \
    ItemDynamicLayout.set_fields('Firehose',
                                 root_path='data.logging_info.firehose',
                                 fields=[
                                     EnumDyField.data_source('Enabled', 'enabled',
                                                             default_badge={
                                                                 'indigo.500': ['true'],
                                                                 'coral.600': ['false'],
                                                             }),
                                     TextDyField.data_source('Delivery Stream', 'delivery_stream'),
                                 ])

cluster_broker_s3 = \
    ItemDynamicLayout.set_fields('S3',
                                 root_path='data.logging_info.s3',
                                 fields=[
                                     EnumDyField.data_source('Enabled', 'enabled',
                                                             default_badge={
                                                                 'indigo.500': ['true'],
                                                                 'coral.600': ['false'],
                                                             }),
                                     TextDyField.data_source('Bucket', 'bucket'),
                                     TextDyField.data_source('Prefix', 'prefix'),
                                 ])
cluster_logging_meta = CloudServiceMeta.set_layouts([cluster_broker_cloudwatchlogs,
                                                     cluster_broker_firehose, cluster_broker_s3])

cluster_tag = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

cluster_operations = \
    TableDynamicLayout.set_fields('Operations', root_path='data.cluster_operation_info', fields=[
        TextDyField.data_source('Operation ARN', 'operation_arn'),
        TextDyField.data_source('Cluster ARN', 'cluster_arn'),
        TextDyField.data_source('Operation Type', 'operation_type'),
        TextDyField.data_source('Error Code', 'error_info.error_code'),
        TextDyField.data_source('Error', 'error_info.error_string'),
        DateTimeDyField.data_source('Creation Time', 'Creation Time'),
        DateTimeDyField.data_source('End Time', 'end_time'),
    ])

cluster_operations_meta = CloudServiceMeta.set_layouts([cluster_operations])

cluster_metadata = CloudServiceMeta.set_layouts([cluster_base, broker_info, cluster_encryption_info,
                                                 cluster_client_authentication, cluster_logging_meta,
                                                 cluster_operations_meta, cluster_tag])

'''
CONFIGURATION
'''
configuration_base = ItemDynamicLayout.set_fields('General', fields=[
    TextDyField.data_source('Configuration ARN', 'arn'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Description', 'description'),
])

configuration_revision = \
    TableDynamicLayout.set_fields('Revisions',
                                  root_path='data.revisions_configurations',
                                  fields=[
                                      TextDyField.data_source('Configuration ARN', 'arn'),
                                      TextDyField.data_source('Revision number', 'revision'),
                                      ListDyField.data_source('Server Properties', 'server_properties'),
                                      TextDyField.data_source('Description', 'description'),
                                      TextDyField.data_source('Creation Time', 'creation_time'),
                                  ])

configuration_metadata = CloudServiceMeta.set_layouts([configuration_base, configuration_revision])


class MSKResource(CloudServiceResource):
    cloud_service_group = StringType(default='MSK')


# Cluster
class ClusterResource(MSKResource):
    class_service_type = StringType(default='Clusters')
    data = ModelType(Cluster)
    _metadata = ModelType(CloudServiceMeta, default=cluster_metadata, serialized_name='metadata')


class ClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterResource)


# Cluster Configuration
class ConfigurationResource(MSKResource):
    class_service_type = StringType(default='Cluster Configurations')
    data = ModelType(Configuration)
    _metadata = ModelType(CloudServiceMeta, default=configuration_metadata, serialized_name='metadata')


class ConfigurationResponse(CloudServiceResponse):
    resource = PolyModelType(ConfigurationResource)
