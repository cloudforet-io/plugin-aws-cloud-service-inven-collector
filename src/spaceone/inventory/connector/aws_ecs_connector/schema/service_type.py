from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_ecs_cluster = CloudServiceTypeResource()
cst_ecs_cluster.name = 'Cluster'
cst_ecs_cluster.provider = 'aws'
cst_ecs_cluster.group = 'ECS'
cst_ecs_cluster.labels = ['Container', 'Compute']
cst_ecs_cluster.is_primary = True
cst_ecs_cluster.is_major = True
cst_ecs_cluster.service_code = 'AmazonECS'
cst_ecs_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Container-Service.svg',
}

cst_ecs_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
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
        })
    ],
    search=[
        SearchField.set(name='Cluster Name', key='name'),
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
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecs_cluster}),
]
