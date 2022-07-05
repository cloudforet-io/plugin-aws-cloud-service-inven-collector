from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_ecs_connector.schema.data import Cluster
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

base = ItemDynamicLayout.set_fields('Clusters', fields=[
    TextDyField.data_source('Name', 'data.cluster_name'),
    TextDyField.data_source('ARN', 'data.cluster_arn'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['PROVISIONING', 'DEPROVISIONING'],
        'disable': ['INACTIVE'],
        'alert': ['FAILED']
    }),
    TextDyField.data_source('Active Service', 'data.active_services_count'),
    TextDyField.data_source('Running Tasks', 'data.running_tasks_count'),
    TextDyField.data_source('Pending Tasks', 'data.pending_tasks_count'),
    TextDyField.data_source('Registered Instances', 'data.registered_container_instances_count'),
])

services = TableDynamicLayout.set_fields('Services', 'data.services', fields=[
    TextDyField.data_source('Name', 'service_name'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['ACTIVE'],
        'disable': ['INACTIVE'],
        'warning': ['DRAINING']
    }),
    EnumDyField.data_source('Service Type', 'scheduling_strategy', default_outline_badge=['REPLICA', 'DAEMON']),
    TextDyField.data_source('Task Definition', 'task_definition'),
    TextDyField.data_source('Desired tasks', 'desired_count'),
    TextDyField.data_source('Running tasks', 'running_count'),
    EnumDyField.data_source('Launch type', 'launch_type', default_outline_badge=['EC2', 'FARGATE']),
    TextDyField.data_source('Platform version', 'platform_version'),
])

tasks = TableDynamicLayout.set_fields('Tasks', 'data.tasks', fields=[
    TextDyField.data_source('Task', 'task'),
    TextDyField.data_source('Task Definition', 'task_definition'),
    EnumDyField.data_source('Last status', 'last_status', default_state={
        'safe': ['RUNNING']
    }),
    EnumDyField.data_source('Desired status', 'desired_status', default_state={
        'safe': ['RUNNING']
    }),
    TextDyField.data_source('Started By', 'started_by'),
    TextDyField.data_source('Group', 'group'),
    TextDyField.data_source('Container instance', 'container_instance_arn'),
    EnumDyField.data_source('Launch Type', 'launch_type', default_outline_badge=['EC2', 'FARGATE']),
    TextDyField.data_source('Platform version', 'platform_version'),
])

container_instances = TableDynamicLayout.set_fields('Container Instances', 'data.container_instances', fields=[
    TextDyField.data_source('Container instance', 'container_instance_arn'),
    TextDyField.data_source('EC2 Instance', 'ec2_instance_id'),
    EnumDyField.data_source('Agent Connected', 'agent_connected', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Running tasks count', 'running_tasks_count'),
    TextDyField.data_source('Agent Version', 'version_info.agent_version'),
    TextDyField.data_source('Docker Version', 'version_info.docker_version'),
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[base, services, tasks, container_instances, tags])


class ECSResource(CloudServiceResource):
    cloud_service_group = StringType(default='ECS')


class ClusterResource(ECSResource):
    cloud_service_type = StringType(default='Cluster')
    data = ModelType(Cluster)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class ClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterResource)
