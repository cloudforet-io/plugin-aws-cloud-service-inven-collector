from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_ecs_cluster = CloudServiceTypeResource()
cst_ecs_cluster.name = 'Cluster'
cst_ecs_cluster.provider = 'aws'
cst_ecs_cluster.group = 'ECS'
cst_ecs_cluster.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Container-Service.svg',
    'spaceone:is_major': 'true',
}

cst_ecs_cluster._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ecs_cluster}),
]
