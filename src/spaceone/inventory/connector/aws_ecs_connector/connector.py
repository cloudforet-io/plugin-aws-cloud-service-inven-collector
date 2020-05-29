import logging
from typing import List

from spaceone.inventory.connector.aws_ecs_connector.schema.data import Cluster, Service, Task, ContainerInstance
from spaceone.inventory.connector.aws_ecs_connector.schema.resource import ClusterResource, ClusterResponse
from spaceone.inventory.connector.aws_ecs_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel


_LOGGER = logging.getLogger(__name__)


class ECSConnector(SchematicAWSConnector):
    response_schema = ClusterResponse
    service_name = 'ecs'

    def get_resources(self) -> List[ClusterResource]:
        print("** ECS START **")
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': ClusterResource({'data': data,
                                                  'reference': ReferenceModel(data.reference)})})

    def request_data(self, region_name) -> List[Cluster]:
        cluster_arns = self.list_clusters()
        response = self.client.describe_clusters(clusters=list(cluster_arns))

        for raw in response.get('clusters', []):
            raw.update({
                'services': self.set_services(raw['clusterArn']),
                'tasks': self.set_tasks(raw['clusterArn']),
                'container_instances': self.set_container_instances(raw['clusterArn']),
                'region_name': region_name,
                'account_id': self.account_id
            })
            res = Cluster(raw, strict=False)
            yield res

    def list_clusters(self):
        paginator = self.client.get_paginator('list_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('clusterArns', []):
                yield raw

    def set_services(self, cluster_arn):
        service_arns = self.list_services(cluster_arn)

        if len(service_arns) > 0:
            response = self.client.describe_services(cluster=cluster_arn, services=service_arns)
            return list(map(lambda _service: Service(_service, strict=False), response.get('services', [])))

        return []

    def set_tasks(self, cluster_arn):
        tasks = []
        task_arns = self.list_tasks(cluster_arn)

        if len(task_arns) > 0:
            response = self.client.describe_tasks(cluster=cluster_arn, tasks=task_arns)

            for task in response.get('tasks', []):
                if task_name := self._get_task_name(task.get('taskArn', '')):
                    task['task'] = task_name

                if task_definition := self._get_task_definition_name(task.get('taskDefinitionArn', '')):
                    task['task_definition'] = task_definition

                tasks.append(Task(task, strict=False))

        return tasks

    def set_container_instances(self, cluster_arn):
        container_instance_arns = self.list_container_instances(cluster_arn)

        if len(container_instance_arns) > 0:
            response = self.client.describe_container_instances(cluster=cluster_arn,
                                                                containerInstances=container_instance_arns)

            return list(map(lambda _instance: ContainerInstance(_instance, strict=False),
                            response.get('containerInstances', [])))

        return []

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
            service_arns = service_arns + data.get('serviceArns', [])

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
            task_arns = task_arns + data.get('taskArns', [])

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
            instance_arns = instance_arns + data.get('containerInstanceArns', [])

        return instance_arns

    @staticmethod
    def _get_task_name(task_arn):
        _task = task_arn.split('/')
        return _task[1] if len(_task) > 1 else None

    @staticmethod
    def _get_task_definition_name(task_definition_arn):
        _task_definition = task_definition_arn.split('/')
        return _task_definition[1] if len(_task_definition) > 1 else None
