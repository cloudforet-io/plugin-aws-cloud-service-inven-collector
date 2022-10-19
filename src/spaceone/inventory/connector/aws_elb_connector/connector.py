import logging
from spaceone.core.utils import *
from spaceone.inventory.connector.aws_elb_connector.schema.data import LoadBalancer, TargetGroup, LoadBalancerAttributes, \
    TargetGroupAttributes, Listener, Instance
from spaceone.inventory.connector.aws_elb_connector.schema.resource import LoadBalancerResource, TargetGroupResource, \
    LoadBalancerResponse, TargetGroupResponse
from spaceone.inventory.connector.aws_elb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import CloudWatchModel


_LOGGER = logging.getLogger(__name__)
MAX_TAG_RESOURCES = 20


class ELBConnector(SchematicAWSConnector):
    service_name = 'elbv2'
    cloud_service_group = 'ELB'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: ELB")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        collect_resources = [{
            'request_method': self.request_target_group_data,
            'resource': TargetGroupResource,
            'response_schema': TargetGroupResponse
        }, {
            'request_method': self.request_load_balancer_data,
            'resource': LoadBalancerResource,
            'response_schema': LoadBalancerResponse
        }]

        for region_name in self.region_names:
            self.reset_region(region_name)
            self.target_groups = []
            self.load_balancers = []

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: ELB ({time.time() - start_time} sec)')
        return resources

    def request_target_group_data(self, region_name):
        self.cloud_service_type = 'TargetGroup'
        cloudtrail_resource_type = 'AWS::ElasticLoadBalancingV2::TargetGroup'

        raw_tgs = self.request_target_group(region_name)
        tg_arns = [raw_tg.get('TargetGroupArn') for raw_tg in raw_tgs if raw_tg.get('TargetGroupArn')]
        all_tags = []

        if tg_arns:
            all_tags = self.request_tags(tg_arns)

        for raw_tg in raw_tgs:
            try:
                match_tags = self.search_tags(all_tags, raw_tg.get('TargetGroupArn'))
                raw_tg.update({
                    'region_name': region_name,
                    'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw_tg['TargetGroupArn'])
                })

                target_group_vo = TargetGroup(raw_tg, strict=False)
                self.target_groups.append(target_group_vo)

                yield {
                    'data': target_group_vo,
                    'instance_type': target_group_vo.target_type,
                    'name': target_group_vo.target_group_name,
                    'account': self.account_id,
                    'tags': self.convert_tags_to_dict_type(match_tags)
                }

            except Exception as e:
                resource_id = raw_tg.get('TargetGroupArn', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def request_load_balancer_data(self, region_name):
        self.cloud_service_type = 'LoadBalancer'
        cloudtrail_resource_type = 'AWS::ElasticLoadBalancingV2::LoadBalancer'

        all_tags = []
        raw_lbs = self.request_loadbalancer(region_name)

        # Get EC2 Instances
        instances = self.request_instances(region_name)

        lb_arns = [raw_lb.get('LoadBalancerArn') for raw_lb in raw_lbs if raw_lb.get('LoadBalancerArn')]

        if lb_arns:
            all_tags = self.request_tags(lb_arns)

        for raw_lb in raw_lbs:
            try:
                match_instances = []

                match_target_groups = self.match_target_group_from_lb(raw_lb.get('LoadBalancerArn'))
                match_tags = self.search_tags(all_tags, raw_lb.get('LoadBalancerArn'))
                raw_listeners = self.request_listeners(raw_lb.get('LoadBalancerArn'))

                for match_tg in match_target_groups:
                    match_instances.extend(self.match_elb_instance(match_tg, instances))

                raw_lb.update({
                    'region_name': region_name,
                    'listeners': list(map(lambda _listener: Listener(_listener, strict=False), raw_listeners)),
                    'cloudwatch': self.elb_cloudwatch(raw_lb, region_name),
                    'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw_lb['LoadBalancerArn']),
                    'target_groups': match_target_groups,
                    'instances': match_instances
                })

                load_balancer_vo = LoadBalancer(raw_lb, strict=False)
                self.load_balancers.append(load_balancer_vo)

                yield {
                    'name': load_balancer_vo.load_balancer_name,
                    'data': load_balancer_vo,
                    'instance_type': load_balancer_vo.type,
                    'launched_at': self.datetime_to_iso8601(load_balancer_vo.created_time),
                    'account': self.account_id,
                    'tags': self.convert_tags_to_dict_type(match_tags)
                }

                # for avoid to API Rate limitation.
                time.sleep(0.5)

            except Exception as e:
                resource_id = raw_lb.get('LoadBalancerArn', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def match_elb_instance(self, target_group, instances):
        match_instances = []

        for target_health in self.request_target_health(target_group.target_group_arn):
            target_id = target_health.get('Target', {}).get('Id')

            for instance in instances:
                if target_group.target_type == 'instance':
                    if instance['InstanceId'] == target_id:
                        instance.update({
                            'instance_name': self.get_instance_name_from_tag(instance),
                            'target_group_arn': target_group.target_group_arn,
                            'target_group_name': target_group.target_group_name,
                        })

                        match_instances.append(Instance(instance, strict=False))
                elif target_group.target_type == 'ip':
                    for network_interface in instance.get('NetworkInterfaces', []):
                        for private_ip_addr_info in network_interface.get('PrivateIpAddresses', []):
                            if private_ip_addr_info.get('PrivateIpAddress') == target_id:
                                instance.update({
                                    'instance_name': self.get_instance_name_from_tag(instance),
                                    'target_group_arn': target_group.target_group_arn,
                                    'target_group_name': target_group.target_group_name,
                                })

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

    def request_listeners(self, lb_arn):
        response = self.client.describe_listeners(LoadBalancerArn=lb_arn)
        return response.get('Listeners', [])

    def request_tags(self, resource_arns):
        all_tags = []

        for _arns in self.divide_to_chunks(resource_arns, MAX_TAG_RESOURCES):
            response = self.client.describe_tags(ResourceArns=_arns)
            all_tags.extend(response.get('TagDescriptions', []))

        return all_tags

    def match_target_group_from_lb(self, load_balancer_arn):
        match_target_groups = []

        for _tg in self.target_groups:
            if _tg.load_balancer_arns:
                for _tg_lb_arn in _tg.load_balancer_arns:
                    if _tg_lb_arn == load_balancer_arn:
                        match_target_groups.append(_tg)

        return match_target_groups

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

    def elb_cloudwatch(self, raw_lb, region_name):
        cloudwatch_elb = self.set_cloudwatch('AWS/ELB', 'LoadBalancerName', raw_lb['LoadBalancerName'], region_name)

        cloudwatch_elb_type = None
        if raw_lb.get('Type') == 'application':
            elb_id = self.get_elb_id_from_arn(raw_lb['LoadBalancerArn'])
            if elb_id:
                cloudwatch_elb_type = self.set_cloudwatch('AWS/ApplicationELB', 'LoadBalancer', elb_id, region_name)
        elif raw_lb.get('Type') == 'network':
            elb_id = self.get_elb_id_from_arn(raw_lb['LoadBalancerArn'])
            if elb_id:
                cloudwatch_elb_type = self.set_cloudwatch('AWS/NetworkELB', 'LoadBalancer', elb_id, region_name)

        metrics_info = cloudwatch_elb.metrics_info
        if cloudwatch_elb_type:
            metrics_info = metrics_info + cloudwatch_elb_type.metrics_info

        cloudwatch_vo = CloudWatchModel({
            'region_name': region_name,
            'metrics_info': metrics_info
        }, strict=False)

        return cloudwatch_vo

    @staticmethod
    def search_tags(all_tags, resource_arn):
        for tag in all_tags:
            if tag.get('ResourceArn') == resource_arn:
                return tag.get('Tags', [])

        return []

    @staticmethod
    def get_instance_name_from_tag(instance):
        for tag in instance.get('Tags', []):
            if tag.get('Key') == 'Name':
                return tag.get('Value')

        return None

    @staticmethod
    def get_elb_id_from_arn(arn):
        try:
            split_id = arn.split('/')[1:]
            return '/'.join(split_id)
        except Exception as e:
            return None