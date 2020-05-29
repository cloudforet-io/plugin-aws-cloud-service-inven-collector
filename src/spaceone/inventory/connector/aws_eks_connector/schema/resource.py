from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_eks_connector.schema.data import Cluster
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout

base = ItemDynamicLayout.set_fields('Clusters', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('ARN', 'data.arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'DELETING', 'UPDATING'],
        'alert': ['FAILED']
    }),
    TextDyField.data_source('Version', 'data.version'),
    TextDyField.data_source('Endpoint', 'data.endpoint'),
    TextDyField.data_source('Role ARN', 'data.role_arn'),
    TextDyField.data_source('Certificate Authority', 'data.certificate_authority.data'),
])

node_groups = TableDynamicLayout.set_fields('Node Groups', 'data.node_groups', fields=[
    TextDyField.data_source('Group Name', 'container_instance_arn'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'UPDATING', 'DELETING'],
        'alert': ['CREATE_FAILED', 'DELETE_FAILED', 'DEGRADED'],
    }),
    ListDyField.data_source('Instance Types', 'instance_types', default_badge={'type': 'outline'}),
    ListDyField.data_source('Subnets', 'subnets', default_badge={'type': 'outline'}),
    TextDyField.data_source('Disk Size', 'data_size'),
    ListDyField.data_source('Health Issue', 'instance_types', default_badge={'type': 'outline'}),
])

logging = TableDynamicLayout.set_fields('Cluster Logging', 'data.logging.cluster_logging', fields=[
    ListDyField.data_source('Types', 'types', default_badge={'type': 'outline'}),
    EnumDyField.data_source('Enabled', 'enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

update = TableDynamicLayout.set_fields('Updates', 'data.updates', fields=[
    TextDyField.data_source('Update ID', 'id'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['Successful'],
        'warning': ['InProgress'],
        'alert': ['Failed'],
        'disable': ['Cancelled']
    }),
    EnumDyField.data_source('Type', 'type', default_outline_badge=['VersionUpdate', 'EndpointAccessUpdate',
                                                                   'LoggingUpdate', 'ConfigUpdate']),
    DateTimeDyField.data_source('Submission Time', 'created_at'),
    ListDyField.data_source('Error', 'errors.error_code', default_badge={'type': 'outline'})
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[base, node_groups, logging, tags])


class EKSResource(CloudServiceResource):
    cloud_service_group = StringType(default='EKS')


class ClusterResource(EKSResource):
    cloud_service_type = StringType(default='Cluster')
    data = ModelType(Cluster)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class ClusterResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(ClusterResource)
