import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
active_service_total_count_conf = os.path.join(current_dir, 'widget/active_service_total_count.yaml')
running_task_total_count_conf = os.path.join(current_dir, 'widget/running_task_total_count.yaml')
cluster_count_by_region_conf = os.path.join(current_dir, 'widget/cluster_count_by_region.yaml')
cluster_count_by_account_conf = os.path.join(current_dir, 'widget/cluster_count_by_account.yaml')
active_service_count_by_cluster_conf = os.path.join(current_dir, 'widget/active_service_count_by_cluster.yaml')
running_task_count_by_cluster_conf = os.path.join(current_dir, 'widget/running_task_count_by_cluster.yaml')

cst_ecs_cluster = CloudServiceTypeResource()
cst_ecs_cluster.name = 'Cluster'
cst_ecs_cluster.provider = 'aws'
cst_ecs_cluster.group = 'ECS'
cst_ecs_cluster.labels = ['Container', 'Compute']
cst_ecs_cluster.is_primary = True
cst_ecs_cluster.is_major = True
cst_ecs_cluster.service_code = 'AmazonECS'
cst_ecs_cluster.tags = {
    'spaceone:icon': f'{ASSET_URL}/Amazon-Elastic-Container-Service.svg',
}

cst_ecs_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['ACTIVE'],
            'warning': ['PROVISIONING', 'DEPROVISIONING'],
            'disable': ['INACTIVE'],
            'alert': ['FAILED']
        }),
        TextDyField.data_source('Active Services', 'data.active_services_count'),
        TextDyField.data_source('Running Tasks', 'data.running_tasks_count'),
        TextDyField.data_source('Pending Tasks', 'data.pending_tasks_count'),
        TextDyField.data_source('Registered Instances', 'data.registered_container_instances_count'),
        TextDyField.data_source('Cluster ARN', 'data.cluster_arn', options={
            'is_optional': True
        }),
        ListDyField.data_source('Services ARN', 'data.services', options={
            'sub_key': 'service_arn',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Services name', 'data.services', options={
            'sub_key': 'service_name',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Services Launch Type', 'data.services', options={
            'sub_key': 'launch_type',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Services Role ARN', 'data.services', options={
            'sub_key': 'role_arn',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Services Scheduling Strategy', 'data.services', options={
            'sub_key': 'scheduling_strategy',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Tasks ARN', 'data.tasks', options={
            'sub_key': 'task_arn',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Tasks name', 'data.tasks', options={
            'sub_key': 'task',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Tasks Availability Zone', 'data.tasks', options={
            'sub_key': 'availability_zone',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Tasks Health Status', 'data.tasks', options={
            'sub_key': 'health_status',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Tasks CPU', 'data.tasks', options={
            'sub_key': 'cpu',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Tasks CPU', 'data.tasks', options={
            'sub_key': 'memory',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.cluster_arn'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Active Services Count', key='data.active_services_count', data_type='integer'),
        SearchField.set(name='Running Tasks Count', key='data.running_tasks_count', data_type='integer'),
        SearchField.set(name='Pending Tasks Count', key='data.pending_tasks_count', data_type='integer'),
        SearchField.set(name='Service Name', key='data.services.service_name'),
        SearchField.set(name='Service ARN', key='data.services.service_arn'),
        SearchField.set(name='Service Type', key='data.services.scheduling_strategy',
                        enums={
                            'REPLICA': {'label': 'REPLICA'},
                            'DAEMON': {'label': 'DAEMON'},
                        }),
        SearchField.set(name='Task Name', key='data.tasks.task'),
        SearchField.set(name='Task Definition', key='data.tasks.task_definition'),
        SearchField.set(name='Task Definition ARN', key='data.tasks.task_definition_arn'),
        SearchField.set(name='Container Instance ID', key='data.container_instances.ec2_instance_id'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(active_service_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(running_task_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(cluster_count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(cluster_count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(active_service_count_by_cluster_conf)),
        ChartWidget.set(**get_data_from_yaml(running_task_count_by_cluster_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecs_cluster}),
]
