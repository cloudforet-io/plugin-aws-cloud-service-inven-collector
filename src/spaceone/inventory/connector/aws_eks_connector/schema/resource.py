from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_eks_connector.schema.data import Cluster, NodeGroup
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

cluster_base = ItemDynamicLayout.set_fields('Cluster', fields=[
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

cluster_node_groups = TableDynamicLayout.set_fields('Node Groups', 'data.node_groups', fields=[
    TextDyField.data_source('Group Name', 'nodegroup_name'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'UPDATING', 'DELETING'],
        'alert': ['CREATE_FAILED', 'DELETE_FAILED', 'DEGRADED'],
    }),
    ListDyField.data_source('Instance Types', 'instance_types', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Subnets', 'subnets', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Disk Size', 'disk_size'),
    ListDyField.data_source('Health Issue', 'instance_types', options={
        'delimiter': '<br>'
    }),
])

cluster_logging = TableDynamicLayout.set_fields('Cluster Logging', 'data.logging.cluster_logging', fields=[
    ListDyField.data_source('Types', 'types', options={
        'delimiter': '<br>'
    }),
    EnumDyField.data_source('Enabled', 'enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

cluster_update = TableDynamicLayout.set_fields('Updates', 'data.updates', fields=[
    TextDyField.data_source('Update ID', 'id'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['Successful'],
        'warning': ['InProgress'],
        'alert': ['Failed'],
        'disable': ['Cancelled']
    }),
    TextDyField.data_source('Type', 'type'),
    DateTimeDyField.data_source('Submission Time', 'created_at'),
    ListDyField.data_source('Error', 'errors.error_code', options={
        'delimiter': '<br>'
    })
])

cluster_metadata = CloudServiceMeta.set_layouts(
    layouts=[cluster_base, cluster_node_groups, cluster_logging])

node_group_base = ItemDynamicLayout.set_fields('Node Group', fields=[
    TextDyField.data_source('Node Group Name', 'data.nodegroup_name'),
    TextDyField.data_source('Node Group ARN', 'data.nodegroup_arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'UPDATING', 'DELETING'],
        'alert': ['CREATE_FAILED', 'DELETE_FAILED', 'DEGRADED'],
    }),
    TextDyField.data_source('EKS Cluster Name', 'data.cluster_name'),
    TextDyField.data_source('EKS Cluster ARN', 'data.cluster_arn'),
    TextDyField.data_source('Version', 'data.version'),
    TextDyField.data_source('Release Version', 'data.release_version'),
    ListDyField.data_source('Instance Types', 'data.instance_types', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Subnets', 'data.subnets', options={
        'delimiter': '<br>'
    }),
    ListDyField.data_source('Source Security Group', 'data.remote_access.source_security_groups', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('AMI Type', 'data.ami_type'),
    TextDyField.data_source('Node Role', 'data.node_role'),
    TextDyField.data_source('Labels', 'data.labels.string'),
    TextDyField.data_source('Disk Size', 'data.disk_size'),
    DateTimeDyField.data_source('Creation Time', 'data.created_at'),
    DateTimeDyField.data_source('Modification Time', 'data.modified_at')
])

node_group_scaling_config = ItemDynamicLayout.set_fields('Scaling Config', fields=[
    TextDyField.data_source('Min Size', 'data.scaling_config.min_size'),
    TextDyField.data_source('Max Size', 'data.scaling_config.max_size'),
    TextDyField.data_source('Desired Size', 'data.scaling_config.desired_size'),
])

node_group_resource = ItemDynamicLayout.set_fields('Resources', fields=[
    ListDyField.data_source('Auto Scaling Group Name', 'data.resources.auto_scaling_groups', options={
        'delimiter': '<br>',
        'sub_key': 'name'
    }),
    ListDyField.data_source('Auto Scaling Group ARN', 'data.resources.auto_scaling_groups', options={
        'delimiter': '<br>',
        'sub_key': 'arn'
    }),
    TextDyField.data_source('Remote Access Security Group', 'data.resources.remote_access_security_group'),
])

node_group_health = TableDynamicLayout.set_fields('Health', 'data.health.issues', fields=[
    TextDyField.data_source('Code', 'code'),
    TextDyField.data_source('Message', 'message'),
    ListDyField.data_source('Resource IDs', 'resource_ids', options={
        'delimiter': '<br>',
    }),
])

node_group_metadata = CloudServiceMeta.set_layouts(layouts=[node_group_base, node_group_scaling_config,
                                                            node_group_resource, node_group_health])


class EKSResource(CloudServiceResource):
    cloud_service_group = StringType(default='EKS')


class ClusterResource(EKSResource):
    cloud_service_type = StringType(default='Cluster')
    data = ModelType(Cluster)
    _metadata = ModelType(CloudServiceMeta, default=cluster_metadata, serialized_name='metadata')


class ClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterResource)


class NodeGroupResource(EKSResource):
    cloud_service_type = StringType(default='NodeGroup')
    data = ModelType(NodeGroup)
    _metadata = ModelType(CloudServiceMeta, default=node_group_metadata, serialized_name='metadata')


class NodeGroupResponse(CloudServiceResponse):
    resource = PolyModelType(NodeGroupResource)
