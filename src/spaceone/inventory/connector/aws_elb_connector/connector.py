import time
import logging
import traceback

from typing import List

from spaceone.inventory.connector.aws_elb_connector.schema.data import LoadBalancer, TargetGroup, Tags, \
    LoadBalancerAttributes, TargetGroupAttributes, Listener, Instance
from spaceone.inventory.connector.aws_elb_connector.schema.resource import LoadBalancerResource, TargetGroupResource, \
    LoadBalancerResponse, TargetGroupResponse
from spaceone.inventory.connector.aws_elb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class ELBConnector(SchematicAWSConnector):
    lb_response_schema = LoadBalancerResponse
    tg_response_schema = TargetGroupResponse

    service_name = 'elbv2'

    def get_resources(self):
        print("** ELB START **")
        resources = []
        start_time = time.time()

        collect_resources = [{
            'request_method': self.request_target_group_data,
            'resource': TargetGroupResource,
            'response_schema': TargetGroupResponse
        }, {
            'request_method': self.request_load_balancer_data,
            'resource': LoadBalancerResource,
            'response_schema': LoadBalancerResponse
        }]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)
            self.target_groups = []
            self.load_balancers = []

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' ELB Finished {time.time() - start_time} Seconds')
        return resources

    def request_target_group_data(self, region_name):
        raw_tgs = self.request_target_group(region_name)
        tg_arns = [raw_tg.get('TargetGroupArn') for raw_tg in raw_tgs if raw_tg.get('TargetGroupArn')]

        if len(tg_arns) > 0:
            all_tags = self.request_tags(tg_arns)

        for raw_tg in raw_tgs:
            match_tags = self.search_tags(all_tags, raw_tg.get('TargetGroupArn'))
            raw_tg.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'tags': list(map(lambda match_tag: Tags(match_tag, strict=False), match_tags))
            })

            target_group = TargetGroup(raw_tg, strict=False)
            self.target_groups.append(target_group)
            yield target_group, target_group.target_group_name

    def request_load_balancer_data(self, region_name):
        all_tags = []
        raw_lbs = self.request_loadbalancer(region_name)

        # Get EC2 Instances
        instances = self.request_instances(region_name)

        lb_arns = [raw_lb.get('LoadBalancerArn') for raw_lb in raw_lbs if raw_lb.get('LoadBalancerArn')]

        if len(lb_arns) > 0:
            all_tags = self.request_tags(lb_arns)

        for raw_lb in raw_lbs:
            match_target_groups = []
            match_instances = []

            match_tags = self.search_tags(all_tags, raw_lb.get('LoadBalancerArn'))
            raw_listeners = self.request_listeners(raw_lb.get('LoadBalancerArn'))

            for _listener in raw_listeners:
                for default_action in _listener.get('DefaultActions', []):
                    if match_tg := self.match_target_group(default_action.get('TargetGroupArn')):
                        match_target_groups.append(match_tg)

            for match_tg in match_target_groups:
                match_instances.extend(self.match_elb_instance(match_tg, instances))

            raw_lb.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'listeners': list(map(lambda _listener: Listener(_listener, strict=False), raw_listeners)),
                'tags': list(map(lambda match_tag: Tags(match_tag, strict=False), match_tags)),
                'target_groups': match_target_groups,
                'instances': match_instances
            })

            load_balancer = LoadBalancer(raw_lb, strict=False)
            self.load_balancers.append(load_balancer)
            yield load_balancer, load_balancer.load_balancer_name

            # for avoid to API Rate limitation.
            time.sleep(0.5)

    def match_elb_instance(self, target_group, instances):
        match_instances = []

        target_healths = self.request_target_health(target_group.target_group_arn)

        for target_health in target_healths:
            target_id = target_health.get('Target', {}).get('Id')

            for instance in instances:
                if target_group.target_type == 'instance':
                    if instance['InstanceId'] == target_id:
                        match_instances.append(Instance(instance, strict=False))
                elif target_group.target_type == 'ip':
                    for network_interface in instance.get('NetworkInterfaces', []):
                        if network_interface.get('PrivateIpAddress') == target_id:
                            match_instances.append(Instance(instance, strict=False))
                            break

        return match_instances


    def request_loadbalancer(self, region_name):
        load_balancers = []
        paginator = self.client.get_paginator('describe_load_balancers')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('LoadBalancers', []):
                raw['attributes'] = self.request_lb_attributes(raw.get('LoadBalancerArn'))
                load_balancers.append(raw)

        return load_balancers

    def request_target_health(self, target_group_arn):
        response = self.client.describe_target_health(TargetGroupArn=target_group_arn)
        return response.get('TargetHealthDescriptions', [])

    def request_target_group(self, region_name):
        target_groups = []
        paginator = self.client.get_paginator('describe_target_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('TargetGroups', []):
                raw['attributes'] = self.request_target_group_attributes(raw.get('TargetGroupArn'))
                target_groups.append(raw)

        return target_groups

    def request_lb_attributes(self, lb_arn):
        attribute_info = {}

        response = self.client.describe_load_balancer_attributes(LoadBalancerArn=lb_arn)
        attrs = response.get('Attributes', [])

        for attr in attrs:
            if attr.get('Key') == 'access_logs.s3.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['access_logs_s3_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['access_logs_s3_enabled'] = 'Disabled'
            elif attr.get('Key') == 'access_logs.s3.prefix':
                attribute_info['access_logs_s3_prefix'] = attr.get('Value', '')
            elif attr.get('Key') == 'access_logs.s3.bucket':
                attribute_info['access_logs_s3_bucket'] = attr.get('Value', '')
            elif attr.get('Key') == 'idle_timeout.timeout_seconds':
                attribute_info['idle_timeout_seconds'] = attr.get('Value', '')
            elif attr.get('Key') == 'load_balancing.cross_zone.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['load_balancing_cross_zone_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['load_balancing_cross_zone_enabled'] = 'Disabled'
            elif attr.get('Key') == 'deletion_protection.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['deletion_protection_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['deletion_protection_enabled'] = 'Disabled'
            elif attr.get('Key') == 'routing.http2.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['routing_http2_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['routing_http2_enabled'] = 'Disabled'
            elif attr.get('Key') == 'routing.http.drop_invalid_header_fields.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['routing_http_drop_invalid_header_fields_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['routing_http_drop_invalid_header_fields_enabled'] = 'Disabled'
            elif attr.get('Key') == 'routing.http.desync_mitigation_mode':
                attribute_info['routing_http_desync_mitigation_mode'] = attr.get('Value', '')
            elif attr.get('Key') == 'waf.fail_open.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['waf_fail_open_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['waf_fail_open_enabled'] = 'Disabled'

        return LoadBalancerAttributes(attribute_info, strict=False)

    def request_target_group_attributes(self, tg_arn):
        attribute_info = {}

        response = self.client.describe_target_group_attributes(TargetGroupArn=tg_arn)
        attrs = response.get('Attributes')

        for attr in attrs:
            if attr.get('Key') == 'stickiness.enabled':
                if attr.get('Value') == 'true':
                    attribute_info['stickiness_enabled'] = 'Enabled'
                elif attr.get('Value') == 'false':
                    attribute_info['stickiness_enabled'] = 'Disabled'

            elif attr.get('Key') == 'deregistration_delay.timeout_seconds':
                attribute_info['deregistration_delay_timeout_seconds'] = attr.get('Value', '')

            elif attr.get('Key') == 'stickiness.type':
                attribute_info['stickiness_type'] = attr.get('Value', '')

            elif attr.get('Key') == 'stickiness.lb_cookie.duration_seconds':
                attribute_info['stickiness_lb_cookie.duration_seconds'] = attr.get('Value', '')

            elif attr.get('Key') == 'slow_start.duration_seconds':
                attribute_info['slow_start_duration_seconds'] = attr.get('Value', '')

            elif attr.get('Key') == 'load_balancing.algorithm.type':
                attribute_info['load_balancing_algorithm_type'] = attr.get('Value', '')

        return TargetGroupAttributes(attribute_info, strict=False)

    def request_listeners(self, lb_arn):
        response = self.client.describe_listeners(LoadBalancerArn=lb_arn)
        return response.get('Listeners', [])

    def request_tags(self, resource_arns):
        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        all_tags = []
        for _arns in list(chunks(resource_arns, 20)):
            response = self.client.describe_tags(ResourceArns=_arns)
            all_tags = all_tags + response.get('TagDescriptions', [])

        return all_tags

    def match_target_group(self, taget_group_arn):
        for _tg in self.target_groups:
            if _tg.target_group_arn == taget_group_arn:
                return _tg

        return None

    def request_instances(self, region_name):
        ec2_client = self.session.client('ec2', region_name=region_name)

        instances = []
        paginator = ec2_client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            },
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['pending', 'running', 'shutting-down', 'stopping', 'stopped']}]
        )

        for data in response_iterator:
            for _reservation in data.get('Reservations', []):
                instances.extend(_reservation.get('Instances', []))

        return instances

    @staticmethod
    def search_tags(all_tags, resource_arn):
        for tag in all_tags:
            if tag.get('ResourceArn') == resource_arn:
                return tag.get('Tags', [])

        return []
