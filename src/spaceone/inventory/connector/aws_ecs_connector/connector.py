import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ecs_connector.schema.data import Cluster, Service, Task, ContainerInstance
from spaceone.inventory.connector.aws_ecs_connector.schema.resource import ClusterResource, ClusterResponse
from spaceone.inventory.connector.aws_ecs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)

MAX_CLUSTERS = 100
MAX_SERVICES = 10
MAX_TASKS = 100
MAX_CONTAINER_INSTANCES = 100


class ECSConnector(SchematicAWSConnector):
    service_name = 'ecs'
    cloud_service_group = 'ECS'
    cloud_service_type = 'Cluster'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[ClusterResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: ECS")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        collect_resource = {
            'request_method': self.request_data,
            'resource': ClusterResource,
            'response_schema': ClusterResponse
        }

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: ECS ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Cluster]:
        cloudtrail_resource_type = 'AWS::ECS::Cluster'
        cluster_arns = self.list_clusters()

        for _arns in self.divide_to_chunks(cluster_arns, MAX_CLUSTERS):
            response = self.client.describe_clusters(clusters=_arns)

            for raw in response.get('clusters', []):
                try:
                    raw.update({
                        'services': self.set_services(raw['clusterArn']),
                        'tasks': self.set_tasks(raw['clusterArn']),
                        'container_instances': self.set_container_instances(raw['clusterArn']),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['clusterName'])
                    })

                    cluster_vo = Cluster(raw, strict=False)
                    yield {
                        'data': cluster_vo,
                        'name': cluster_vo.cluster_name,
                        'account': self.account_id,
                        'tags': self.convert_tags_to_dict_type(raw.get('tags', []))
                    }

                except Exception as e:
                    resource_id = raw.get('clusterArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def list_clusters(self):
        clusters = []

        paginator = self.client.get_paginator('list_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            clusters.extend(data.get('clusterArns', []))

        return clusters

    def set_services(self, cluster_arn):
        services = []
        service_arns = self.list_services(cluster_arn)

        if service_arns:
            for _arns in self.divide_to_chunks(service_arns, MAX_SERVICES):
                response = self.client.describe_services(cluster=cluster_arn, services=_arns)
                services.extend(list(map(lambda _service: Service(_service, strict=False),
                                         response.get('services', []))))

        return services

    def set_tasks(self, cluster_arn):
        tasks = []
        task_arns = self.list_tasks(cluster_arn)

        if task_arns:
            for _arns in self.divide_to_chunks(task_arns, MAX_TASKS):
                response = self.client.describe_tasks(cluster=cluster_arn, tasks=_arns)

                for task in response.get('tasks', []):
                    if task_name := self._get_task_name(task.get('taskArn', '')):
                        task['task'] = task_name

                    if task_definition := self._get_task_definition_name(task.get('taskDefinitionArn', '')):
                        task['task_definition'] = task_definition

                    tasks.append(Task(task, strict=False))

        return tasks

    def set_container_instances(self, cluster_arn):
        container_instances = []
        container_instance_arns = self.list_container_instances(cluster_arn)

        if container_instance_arns:
            for _arns in self.divide_to_chunks(container_instance_arns, MAX_CONTAINER_INSTANCES):
                response = self.client.describe_container_instances(cluster=cluster_arn, containerInstances=_arns)
                container_instances.extend(list(map(lambda _instance: ContainerInstance(_instance, strict=False),
                                                    response.get('containerInstances', []))))

        return container_instances

    def list_services(self, cluster_arn):
        service_arns = []
        paginator = self.client.get_paginator('list_services')
        response_iterator = paginator.paginate(
            cluster=cluster_arn,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            service_arns.extend(data.get('serviceArns', []))

        return service_arns

    def list_tasks(self, cluster_arn):
        task_arns = []
        paginator = self.client.get_paginator('list_tasks')
        response_iterator = paginator.paginate(
            cluster=cluster_arn,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            task_arns.extend(data.get('taskArns', []))

        return task_arns

    def list_container_instances(self, cluster_arn):
        instance_arns = []
        paginator = self.client.get_paginator('list_container_instances')
        response_iterator = paginator.paginate(
            cluster=cluster_arn,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            instance_arns.extend(data.get('containerInstanceArns', []))

        return instance_arns

    @staticmethod
    def _get_task_name(task_arn):
        _task = task_arn.split('/')
        return _task[1] if len(_task) > 1 else None

    @staticmethod
    def _get_task_definition_name(task_definition_arn):
        _task_definition = task_definition_arn.split('/')
        return _task_definition[1] if len(_task_definition) > 1 else None
