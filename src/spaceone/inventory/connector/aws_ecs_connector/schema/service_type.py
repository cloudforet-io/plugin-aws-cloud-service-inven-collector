from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_ecs_cluster = CloudServiceTypeResource()
cst_ecs_cluster.name = 'Cluster'
cst_ecs_cluster.provider = 'aws'
cst_ecs_cluster.group = 'ECS'
cst_ecs_cluster.labels = ['Container']
cst_ecs_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Container-Service.svg',
    'spaceone:is_major': 'true',
}

cst_ecs_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.cluster_name'),
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
    ],
    search=[
        SearchField.set(name='Cluster Name', key='data.cluster_name'),
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
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecs_cluster}),
]
