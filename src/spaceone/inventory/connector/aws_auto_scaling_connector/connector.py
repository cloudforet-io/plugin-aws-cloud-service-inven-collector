import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.data import AutoScalingGroup, LaunchConfiguration, \
    AutoScalingPolicy, LifecycleHook, NotificationConfiguration, ScheduledAction, LaunchTemplateDetail, Tags, \
    AutoScalingGroupTags
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.resource import AutoScalingGroupResource, \
    LaunchConfigurationResource, LaunchTemplateResource, AutoScalingGroupResponse, LaunchConfigurationResponse, \
    LaunchTemplateResponse
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class AutoScalingConnector(SchematicAWSConnector):
    _launch_configurations = None
    _launch_templates = None

    service_name = 'autoscaling'
    cloud_service_group = 'EC2'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Auto Scaling")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        collect_resources = [
            {
                'request_method': self.request_launch_configuration_data,
                'resource': LaunchConfigurationResource,
                'response_schema': LaunchConfigurationResponse
            },
            {
                'request_method': self.request_launch_template_data,
                'resource': LaunchTemplateResource,
                'response_schema': LaunchTemplateResponse
            },
            {
                'request_method': self.request_auto_scaling_group_data,
                'resource': AutoScalingGroupResource,
                'response_schema': AutoScalingGroupResponse
            }
        ]

        for region_name in self.region_names:
            self._launch_configurations = []
            self._launch_templates = []
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Auto Scaling ({time.time() - start_time} sec)')
        return resources

    def request_auto_scaling_group_data(self, region_name) -> List[AutoScalingGroup]:
        self.cloud_service_type = 'AutoScalingGroup'

        paginator = self.client.get_paginator('describe_auto_scaling_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        policies = None
        notification_configurations = None

        for data in response_iterator:
            for raw in data.get('AutoScalingGroups', []):
                try:
                    if policies is None:
                        policies = self._describe_policies()

                    if notification_configurations is None:
                        notification_configurations = self._describe_notification_configurations()

                    match_lc = self._match_launch_configuration(raw.get('LaunchConfigurationName', ''))
                    match_lt = self._match_launch_template(raw)

                    match_policies = self._match_policies(policies, raw.get('AutoScalingGroupName'))
                    match_noti_confs = self._match_notification_configuration(notification_configurations,
                                                                              raw.get('AutoScalingGroupName'))
                    match_lb_arns = self.get_load_balancer_arns(raw.get('TargetGroupARNs', []))
                    match_lbs = self.get_load_balancer_info(match_lb_arns)

                    raw.update({
                        'launch_configuration': LaunchConfiguration(match_lc, strict=False),
                        'policies': list(map(lambda policy: AutoScalingPolicy(policy, strict=False), match_policies)),
                        'notification_configurations': list(map(lambda noti_conf: NotificationConfiguration(noti_conf,
                                                                                                            strict=False),
                                                                match_noti_confs)),
                        'scheduled_actions': list(map(lambda scheduled_action: ScheduledAction(scheduled_action,
                                                                                               strict=False),
                                                      self._describe_scheduled_actions(raw['AutoScalingGroupName']))),
                        'lifecycle_hooks': list(map(lambda lifecycle_hook: LifecycleHook(lifecycle_hook, strict=False),
                                                    self._describe_lifecycle_hooks(raw['AutoScalingGroupName']))),
                        'autoscaling_tags': list(map(lambda tag: AutoScalingGroupTags(tag, strict=False),
                                                     raw.get('Tags', []))),
                        'instances': self.get_asg_instances(raw.get('Instances', [])),
                        'tags': list(map(lambda tag: Tags(tag, strict=False),
                                         self.get_general_tags(raw.get('Tags', [])))),
                        'account_id': self.account_id
                    })

                    if raw.get('LaunchConfigurationName'):
                        raw.update({
                            'display_launch_configuration_template': raw.get('LaunchConfigurationName')
                        })
                    elif raw.get('MixedInstancesPolicy', {}).get('LaunchTemplate', {}).get('LaunchTemplateSpecification'):
                        _lt_info = raw.get('MixedInstancesPolicy', {}).get('LaunchTemplate', {}).get('LaunchTemplateSpecification')
                        raw.update({
                            'display_launch_configuration_template': _lt_info.get('LaunchTemplateName'),
                            'launch_template': match_lt
                        })
                    elif raw.get('LaunchTemplate'):
                        raw.update({
                            'display_launch_configuration_template': raw.get('LaunchTemplate').get('LaunchTemplateName'),
                            'launch_template': match_lt
                        })

                    else:
                        for instance in raw.get('Instances', []):
                            if instance.get('LaunchTemplate'):
                                raw.update({
                                    'launch_template': match_lt,
                                    'display_launch_configuration_template': instance.get('LaunchTemplate').get(
                                        'LaunchTemplateName')
                                })
                            elif instance.get('LaunchConfigurationName'):
                                raw.update({
                                    'LaunchConfigurationName': instance.get('LaunchConfigurationName'),
                                    'display_launch_configuration_template': instance.get('LaunchConfigurationName')
                                })

                    if raw.get('TargetGroupARNs'):
                        raw.update({
                            'load_balancers': match_lbs,
                            'load_balancer_arns': match_lb_arns
                        })

                    auto_scaling_group_vo = AutoScalingGroup(raw, strict=False)
                    yield {
                        'data': auto_scaling_group_vo,
                        'name': auto_scaling_group_vo.auto_scaling_group_name,
                        'account': self.account_id,
                        'launched_at': self.datetime_to_iso8601(auto_scaling_group_vo.created_time)
                    }

                except Exception as e:
                    resource_id = raw.get('AutoScalingGroupARN', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_launch_configuration_data(self, region_name) -> List[LaunchConfiguration]:
        self.cloud_service_type = 'LaunchConfiguration'

        paginator = self.client.get_paginator('describe_launch_configurations')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('LaunchConfigurations', []):
                try:
                    raw.update({
                        'account_id': self.account_id
                    })
                    launch_configuration_vo = LaunchConfiguration(raw, strict=False)
                    self._launch_configurations.append(launch_configuration_vo)

                    yield {
                        'data': launch_configuration_vo,
                        'name': launch_configuration_vo.launch_configuration_name,
                        'account': self.account_id,
                        'launched_at': self.datetime_to_iso8601(launch_configuration_vo.created_time)
                    }

                except Exception as e:
                    resource_id = raw.get('LaunchConfigurationARN', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_launch_template_data(self, region_name) -> List[LaunchTemplateDetail]:
        self.cloud_service_type = 'LaunchTemplate'

        ec2_client = self.session.client('ec2')
        paginator = ec2_client.get_paginator('describe_launch_templates')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('LaunchTemplates', []):
               try:
                    match_lt_version = self._match_launch_template_version(raw.get('LaunchTemplateId'))
                    match_lt_data = self._match_launch_template_data(match_lt_version)

                    raw.update({
                        'version': match_lt_version.get('VersionNumber'),
                        'version_description': match_lt_version.get('VersionDescription'),
                        'default_version': match_lt_version.get('DefaultVersion'),
                        'account_id': self.account_id,
                        'launch_template_data': match_lt_data,
                        'arn': self.generate_arn(service="ec2", region="", account_id="",
                                                 resource_type="launch_template",
                                                 resource_id=raw['LaunchTemplateId'] + '/v' + str(
                                                     match_lt_version.get('VersionNumber')))
                    })

                    launch_template_vo = LaunchTemplateDetail(raw, strict=False)
                    self._launch_templates.append(launch_template_vo)

                    yield {
                        'data': launch_template_vo,
                        'name': launch_template_vo.launch_template_name,
                        'account': self.account_id,
                        'launched_at': self.datetime_to_iso8601(launch_template_vo.create_time)
                    }

               except Exception as e:
                    resource_id = raw.get('LaunchTemplateId', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def get_asg_instances(self, instances):
        ec2_client = self.session.client('ec2')
        max_count = 20
        instances_from_ec2 = []
        split_instances = [instances[i:i + max_count] for i in range(0, len(instances), max_count)]

        for instances in split_instances:
            try:
                instance_ids = [_instance.get('InstanceId') for _instance in instances if _instance.get('InstanceId')]
                response = ec2_client.describe_instances(InstanceIds=instance_ids)

                for reservation in response.get('Reservations', []):
                    instances_from_ec2.extend(reservation.get('Instances', []))
            except Exception as e:
                _LOGGER.debug(f"[autoscaling] instance not found: {instance_ids}")

        for instance in instances:
            for instance_from_ec2 in instances_from_ec2:
                if instance_from_ec2.get('InstanceId') == instance.get('InstanceId'):
                    instance.update({
                        'lifecycle': instance_from_ec2.get('InstanceLifecycle', 'scheduled')
                    })
                    break

        return instances

    def get_load_balancer_arns(self, target_group_arns):
        elb_client = self.session.client('elbv2')
        lb_arns = []
        max_count = 20

        split_tgs_arns = [target_group_arns[i:i + max_count] for i in range(0, len(target_group_arns), max_count)]

        for tg_arns in split_tgs_arns:
            try:
                response = elb_client.describe_target_groups(TargetGroupArns=tg_arns)

                for target_group in response.get('TargetGroups', []):
                    lb_arns.extend(target_group.get('LoadBalancerArns', []))
            except Exception as e:
                _LOGGER.debug(f"[autoscaling] target group not found: {tg_arns}")

        return lb_arns

    def get_load_balancer_info(self, lb_arns):
        elb_client = self.session.client('elbv2')
        max_count = 20

        split_lb_arns = [lb_arns[i:i + max_count] for i in range(0, len(lb_arns), max_count)]

        load_balancer_data_list = []

        for lb_arns in split_lb_arns:
            try:
                lbs = elb_client.describe_load_balancers(LoadBalancerArns=lb_arns).get('LoadBalancers', [])

                for lb in lbs:
                    lb_arn = lb.get('LoadBalancerArn', '')
                    listeners = elb_client.describe_listeners(LoadBalancerArn=lb_arn).get('Listeners', [])
                    lb.update({
                        'listeners': listeners
                    })
                    load_balancer_data_list.append(self.get_load_balancer_data(lb))

                    # avoid to API Rate limitation.
                    time.sleep(0.5)

            except Exception as e:
                _LOGGER.debug(f"[autoscaling] ELB not found: {lb_arns}")

        return load_balancer_data_list

    @staticmethod
    def get_load_balancer_data(match_load_balancer):
        return {
            'endpoint': match_load_balancer.get('DNSName', ''),
            'type': match_load_balancer.get('Type'),
            'scheme': match_load_balancer.get('Scheme'),
            'name': match_load_balancer.get('LoadBalancerName', ''),
            'protocol': [listener.get('Protocol') for listener in match_load_balancer.get('listeners', []) if
                         listener.get('Protocol')],
            'port': [listener.get('Port') for listener in match_load_balancer.get('listeners', []) if
                     listener.get('Port')],
            'tags': {
                'arn': match_load_balancer.get('LoadBalancerArn', '')
            }
        }

    def _match_launch_template_version(self, lt):
        ec2_client = self.session.client('ec2')
        lt_versions = ec2_client.describe_launch_template_versions(LaunchTemplateId=lt)
        res = lt_versions.get('LaunchTemplateVersions', [])[0]
        return res

    def _match_launch_configuration(self, lc):
        return next((launch_configuration for launch_configuration in self._launch_configurations
                     if launch_configuration.launch_configuration_name == lc), '')

    def _match_launch_template(self, raw):
        lt_dict = {}

        if raw.get('LaunchTemplate'):
            lt_dict = raw.get('LaunchTemplate')
        elif raw.get('MixedInstancesPolicy', {}).get('LaunchTemplate', {}).get('LaunchTemplateSpecification'):
            lt_dict = raw.get('MixedInstancesPolicy', {}).get('LaunchTemplate', {}).get('LaunchTemplateSpecification')
        else:
            for instance in raw.get('Instances', []):
                if instance.get('LaunchTemplate'):
                    lt_dict = instance.get('LaunchTemplate')

        return next((launch_template for launch_template in self._launch_templates
                     if launch_template.launch_template_id == lt_dict.get('LaunchTemplateId')), None)

    @staticmethod
    def _match_launch_template_data(lt_ver):
        res = lt_ver.get('LaunchTemplateData', [])
        return res

    @staticmethod
    def _match_policies(policies, asg_name):
        match_policies = []

        for _policy in policies:
            if _policy['AutoScalingGroupName'] == asg_name:
                match_policies.append(_policy)

        return match_policies

    @staticmethod
    def _match_notification_configuration(notification_configurations, asg_name):
        match_noti_confs = []

        for _noti_conf in notification_configurations:
            if _noti_conf['AutoScalingGroupName'] == asg_name:
                match_noti_confs.append(_noti_conf)

        return match_noti_confs

    @staticmethod
    def _match_lifecycle_hook(lifecycle_hooks, asg_name):
        match_lifecycle_kooks = []

        for _lifecycle_hook in lifecycle_hooks:
            if _lifecycle_hook['AutoScalingGroupName'] == asg_name:
                match_lifecycle_kooks.append(_lifecycle_hook)

        return match_lifecycle_kooks

    def _describe_launch_configuration(self):
        res = self.client.describe_launch_configurations()
        return res.get('LaunchConfigurations', [])

    def _describe_policies(self):
        res = self.client.describe_policies()
        return res.get('ScalingPolicies', [])

    def _describe_lifecycle_hooks(self, auto_scaling_group_name):
        res = self.client.describe_lifecycle_hooks(AutoScalingGroupName=auto_scaling_group_name)
        return res.get('LifecycleHooks', [])

    def _describe_notification_configurations(self):
        res = self.client.describe_notification_configurations()
        return res.get('NotificationConfigurations', [])

    def _describe_scheduled_actions(self, auto_scaling_group_name):
        res = self.client.describe_scheduled_actions(AutoScalingGroupName=auto_scaling_group_name)
        return res.get('ScheduledUpdateGroupActions', [])

    @staticmethod
    def get_general_tags(tags):
        return [{'key': tag.get('Key', ''), 'value': tag.get('Value', '')} for tag in tags]
