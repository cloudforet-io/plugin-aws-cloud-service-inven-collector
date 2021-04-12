import logging
import time
from typing import List

from spaceone.inventory.connector.aws_eks_connector.schema.data import Cluster, NodeGroup, Update, Tags
from spaceone.inventory.connector.aws_eks_connector.schema.resource import ClusterResource, ClusterResponse, \
    NodeGroupResource, NodeGroupResponse
from spaceone.inventory.connector.aws_eks_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class EKSConnector(SchematicAWSConnector):
    service_name = 'eks'

    def get_resources(self):
        print("** EKS START **")
        resources = []
        self.node_groups = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': ClusterResource,
            'response_schema': ClusterResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

            # For Node Group
            for node_group_vo in self.node_groups:
                resources.append(NodeGroupResponse(
                    {'resource': NodeGroupResource(
                        {'data': node_group_vo,
                         'tags': [{'key': tag.key, 'value': tag.value} for tag in node_group_vo.tags],
                         'region_code': region_name,
                         'reference': ReferenceModel(node_group_vo.reference(region_name))})}
                ))

            self.node_groups = []
            self.reset_region(region_name)

        print(f' EKS Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[Cluster]:
        paginator = self.client.get_paginator('list_clusters')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for _cluster_name in data.get('clusters', []):
                raw = self.client.describe_cluster(name=_cluster_name)

                if cluster := raw.get('cluster'):
                    cluster.update({
                        'updates': list(self.list_updates(_cluster_name)),
                        'account_id': self.account_id,
                        'tags': list(map(lambda tag: Tags(tag, strict=False),
                                         self.convert_tags(cluster.get('tags', {}))))
                    })

                    node_groups = list(self.list_node_groups(_cluster_name, cluster.get('arn')))

                    cluster.update({
                        'node_groups': node_groups
                    })

                    self.node_groups.extend(node_groups)

                    yield Cluster(cluster, strict=False)

    def list_node_groups(self, cluster_name, cluster_arn):
        asgs = self.get_auto_scaling_groups()
        paginator = self.client.get_paginator('list_nodegroups')
        response_iterator = paginator.paginate(
            clusterName=cluster_name,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for node_group in data.get('nodegroups', []):
                node_group_response = self.client.describe_nodegroup(clusterName=cluster_name, nodegroupName=node_group)
                node_group = node_group_response.get('nodegroup', {})
                node_group.update({
                    'cluster_arn': cluster_arn,
                    'account_id': self.account_id,
                    'tags': list(map(lambda tag: Tags(tag, strict=False),
                                     self.convert_tags(node_group.get('tags', {}))))
                })
                asg_names = [asg.get("name", "") for asg in
                             node_group.get("resources", "").get("autoScalingGroups", [])]
                if len(asg_names) > 0:
                    node_group["resources"]["autoScalingGroups"] = self.get_matched_auto_scaling_groups(asgs, asg_names)
                yield NodeGroup(node_group, strict=False)

    def list_updates(self, cluster_name):
        paginator = self.client.get_paginator('list_updates')
        response_iterator = paginator.paginate(
            name=cluster_name,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for update_id in data.get('updateIds', []):
                response = self.client.describe_update(name=cluster_name, updateId=update_id)
                yield Update(response.get('update', {}), strict=False)

    @staticmethod
    def _convert_tag_format(tags):
        list_tags = []

        for _key in tags:
            list_tags.append({'key': _key, 'value': tags[_key]})

        return list_tags

    def get_auto_scaling_groups(self):
        auto_scaling_client = self.session.client('autoscaling')
        paginator = auto_scaling_client.get_paginator('describe_auto_scaling_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        asgs = []
        for data in response_iterator:
            for asg in data.get('AutoScalingGroups', []):
                asgs.append({
                    "name": asg.get("AutoScalingGroupName", ""),
                    "arn": asg.get("AutoScalingGroupARN", "")
                })
        return asgs

    def get_matched_auto_scaling_groups(self, asgs, asg_names):
        matched_asgs = []
        for asg in asgs:
            if asg.get("name", "") in asg_names:
                matched_asgs.append(asg)
        return matched_asgs
