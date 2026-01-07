import logging

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_elb_connector.schema.data import (
    LoadBalancer,
    TargetGroup,
    LoadBalancerAttributes,
    TargetGroupAttributes,
    Listener,
    Instance,
    ListenerRule,
)
from spaceone.inventory.connector.aws_elb_connector.schema.resource import (
    LoadBalancerResource,
    TargetGroupResource,
    LoadBalancerResponse,
    TargetGroupResponse,
)
from spaceone.inventory.connector.aws_elb_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import CloudWatchModel
from spaceone.inventory.conf.cloud_service_conf import *


_LOGGER = logging.getLogger(__name__)
MAX_TAG_RESOURCES = 20


class ELBConnector(SchematicAWSConnector):
    classic_service_name = "elb"
    elbv2_service_name = "elbv2"
    cloud_service_group = "ELB"
    cloud_service_types = CLOUD_SERVICE_TYPES

    elbv2_client = None
    classic_client = None

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: ELB")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        collect_resources = [
            {
                "request_method": self.request_target_group_data,
                "resource": TargetGroupResource,
                "response_schema": TargetGroupResponse,
            },
            {
                "request_method": self.request_load_balancer_data,
                "resource": LoadBalancerResource,
                "response_schema": LoadBalancerResponse,
            },
        ]

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)
                self.target_groups = []
                self.load_balancers = []

                # Initialize clients once per region
                self.elbv2_client = self.set_client(self.elbv2_service_name)
                self.classic_client = self.set_client(self.classic_service_name)

                for collect_resource in collect_resources:
                    resources.extend(
                        self.collect_data_by_region(
                            self.service_name, region_name, collect_resource
                        )
                    )
            except Exception as e:
                error_resource_response = self.generate_error(region_name, "", e)
                resources.append(error_resource_response)

        _LOGGER.debug(
            f"[get_resources][account_id: {self.account_id}] FINISHED: ELB ({time.time() - start_time} sec)"
        )
        return resources

    def request_target_group_data(self, region_name):
        self.cloud_service_type = "TargetGroup"
        cloudtrail_resource_type = "AWS::ElasticLoadBalancingV2::TargetGroup"

        raw_tgs = self.request_target_group(region_name)
        tg_arns = [
            raw_tg.get("TargetGroupArn")
            for raw_tg in raw_tgs
            if raw_tg.get("TargetGroupArn")
        ]
        all_tags = []

        if tg_arns:
            all_tags = self.request_tags(tg_arns)

        for raw_tg in raw_tgs:
            try:
                match_tags = self.search_tags(all_tags, raw_tg.get("TargetGroupArn"))
                raw_tg.update(
                    {
                        "region_name": region_name,
                        "cloudtrail": self.set_cloudtrail(
                            region_name,
                            cloudtrail_resource_type,
                            raw_tg["TargetGroupArn"],
                        ),
                        "targets_health": self.get_targets_health(
                            raw_tg["TargetGroupArn"]
                        ),
                    }
                )

                target_group_vo = TargetGroup(raw_tg, strict=False)
                self.target_groups.append(target_group_vo)

                yield {
                    "data": target_group_vo,
                    "instance_type": target_group_vo.target_type,
                    "name": target_group_vo.target_group_name,
                    "account": self.account_id,
                    "tags": self.convert_tags_to_dict_type(match_tags),
                }

            except Exception as e:
                resource_id = raw_tg.get("TargetGroupArn", "")
                error_resource_response = self.generate_error(
                    region_name, resource_id, e
                )
                yield {"data": error_resource_response}

    def get_targets_health(self, tg_arn: str):
        return self.request_target_health(tg_arn)

    def request_load_balancer_data(self, region_name):
        self.cloud_service_type = "LoadBalancer"
        cloudtrail_resource_type = "AWS::ElasticLoadBalancingV2::LoadBalancer"

        all_tags = []
        raw_lbs = self.request_loadbalancer(region_name)

        # Get EC2 Instances
        instances = self.request_instances(region_name)

        lb_arns = [
            raw_lb.get("LoadBalancerArn")
            for raw_lb in raw_lbs
            if raw_lb.get("LoadBalancerArn")
        ]

        if lb_arns:
            all_tags = self.request_tags(lb_arns)

        for raw_lb in raw_lbs:
            try:
                match_instances = []

                match_target_groups = self.match_target_group_from_lb(
                    raw_lb.get("LoadBalancerArn")
                )
                match_tags = self.search_tags(all_tags, raw_lb.get("LoadBalancerArn"))
                raw_listeners = self.request_listeners(raw_lb.get("LoadBalancerArn"))
                listener_rules = self.get_listener_rules(raw_listeners)

                for match_tg in match_target_groups:
                    match_instances.extend(self.match_elb_instance(match_tg, instances))

                # Generate custom stats data
                stats = {"instances_size": len(match_instances)}

                raw_lb.update(
                    {
                        "region_name": region_name,
                        "listeners": list(
                            map(
                                lambda _listener: Listener(_listener, strict=False),
                                raw_listeners,
                            )
                        ),
                        "listener_rules": list(
                            map(
                                lambda _listener_rule: ListenerRule(
                                    _listener_rule, strict=False
                                ),
                                listener_rules,
                            )
                        ),
                        "cloudwatch": self.elb_cloudwatch(raw_lb, region_name),
                        "cloudtrail": self.set_cloudtrail(
                            region_name,
                            cloudtrail_resource_type,
                            raw_lb["LoadBalancerArn"],
                        ),
                        "target_groups": match_target_groups,
                        "instances": match_instances,
                        "stats": stats,
                    }
                )

                load_balancer_vo = LoadBalancer(raw_lb, strict=False)
                self.load_balancers.append(load_balancer_vo)

                yield {
                    "name": load_balancer_vo.load_balancer_name,
                    "data": load_balancer_vo,
                    "instance_type": load_balancer_vo.type,
                    "launched_at": self.datetime_to_iso8601(
                        load_balancer_vo.created_time
                    ),
                    "account": self.account_id,
                    "tags": self.convert_tags_to_dict_type(match_tags),
                }

                # for avoid to API Rate limitation.
                time.sleep(0.5)

            except Exception as e:
                resource_id = raw_lb.get("LoadBalancerArn", "")
                error_resource_response = self.generate_error(
                    region_name, resource_id, e
                )
                yield {"data": error_resource_response}


        # Classic Load Balancer
        cloudtrail_resource_type_classic = "AWS::ElasticLoadBalancing::LoadBalancer"
        raw_classic_lbs = self.request_classic_loadbalancer()

        # Get tags for all classic load balancers
        classic_lb_names = [
            lb.get("LoadBalancerName")
            for lb in raw_classic_lbs
            if lb.get("LoadBalancerName")
        ]
        all_classic_tags = []
        if classic_lb_names:
            all_classic_tags = self.request_classic_tags(classic_lb_names)

        for raw_classic_lb in raw_classic_lbs:
            try:
                lb_name = raw_classic_lb.get("LoadBalancerName")

                # Get load balancer attributes
                classic_attributes = self.request_classic_lb_attributes(lb_name)

                # Get instance health
                instance_health = self.request_classic_instance_health(lb_name)

                # Find matching tags
                match_tags = self.search_classic_tags(all_classic_tags, lb_name)

                # Generate ARN
                arn = self.generate_classic_elb_arn(lb_name, region_name)

                # Convert to LoadBalancer format
                converted_lb = self.convert_classic_to_lb_format(
                    raw_classic_lb,
                    arn,
                    region_name,
                    classic_attributes,
                    instance_health,
                    instances,
                )

                converted_lb.update(
                    {
                        "cloudwatch": self.classic_elb_cloudwatch(
                            raw_classic_lb, region_name
                        ),
                        "cloudtrail": self.set_cloudtrail(
                            region_name,
                            cloudtrail_resource_type_classic,
                            lb_name,
                        ),
                    }
                )

                load_balancer_vo = LoadBalancer(converted_lb, strict=False)

                yield {
                    "name": load_balancer_vo.load_balancer_name,
                    "data": load_balancer_vo,
                    "instance_type": "classic",
                    "launched_at": self.datetime_to_iso8601(
                        load_balancer_vo.created_time
                    ),
                    "account": self.account_id,
                    "tags": self.convert_tags_to_dict_type(match_tags),
                }

                # Avoid API rate limitation
                time.sleep(0.3)

            except Exception as e:
                resource_id = raw_classic_lb.get("LoadBalancerName", "")
                error_resource_response = self.generate_error(
                    region_name, resource_id, e
                )
                yield {"data": error_resource_response}

    def match_elb_instance(self, target_group, instances):
        match_instances = []

        for target_health in self.request_target_health(target_group.target_group_arn):
            target_id = target_health.get("Target", {}).get("Id")

            for instance in instances:
                if target_group.target_type == "instance":
                    if instance["InstanceId"] == target_id:
                        instance.update(
                            {
                                "instance_name": self.get_instance_name_from_tag(
                                    instance
                                ),
                                "target_group_arn": target_group.target_group_arn,
                                "target_group_name": target_group.target_group_name,
                            }
                        )

                        match_instances.append(Instance(instance, strict=False))
                elif target_group.target_type == "ip":
                    for network_interface in instance.get("NetworkInterfaces", []):
                        for private_ip_addr_info in network_interface.get(
                            "PrivateIpAddresses", []
                        ):
                            if (
                                private_ip_addr_info.get("PrivateIpAddress")
                                == target_id
                            ):
                                instance.update(
                                    {
                                        "instance_name": self.get_instance_name_from_tag(
                                            instance
                                        ),
                                        "target_group_arn": target_group.target_group_arn,
                                        "target_group_name": target_group.target_group_name,
                                    }
                                )

                                match_instances.append(Instance(instance, strict=False))
                                break

        return match_instances

    def get_listener_rules(self, raw_listeners: list) -> list:
        listener_rules = []

        for raw_listener in raw_listeners:
            try:
                raw_listener_rules = self.request_rules_by_listener(raw_listener)

                for raw_listener_rule in raw_listener_rules:
                    is_default = raw_listener_rule.get("IsDefault", False)
                    conditions = self.get_formatted_conditions(
                        raw_listener_rule["Conditions"], is_default
                    )
                    actions = self.get_formatted_actions(raw_listener_rule["Actions"])
                    rule_info = {
                        "Protocol": raw_listener.get("Protocol"),
                        "Port": raw_listener.get("Port"),
                        "RuleArn": raw_listener_rule.get("RuleArn"),
                        "Priority": raw_listener_rule.get("Priority"),
                        "Conditions": conditions,
                        "Actions": actions,
                        "IsDefault": is_default,
                    }

                    listener_rules.append(rule_info)
            except Exception as e:
                resource_id = raw_listener.get("ListenerArn", "")
                error_resource_response = self.generate_error(None, resource_id, e)
                _LOGGER.error(error_resource_response)

        return listener_rules

    @staticmethod
    def get_formatted_conditions(raw_conditions: list, is_default: bool) -> list:
        str_conditions = []

        if is_default:
            return ["If no other rule applies"]

        for condition in raw_conditions:
            field = condition.get("Field")

            if field == "http-header":
                if config := condition.get("HttpHeaderConfig", {}):
                    header_name = config.get("HttpHeaderName")
                    header_values: list = config.get("Values")

                    if header_name and header_values:
                        str_value = ','.join(header_values)
                        str_conditions.append("HTTP Header :")
                        str_conditions.append(f" - {header_name} : {str_value}")

            elif field == "http-request-method":
                if values := condition.get("HttpRequestMethodConfig", {}).get("Values"):
                    str_value = ','.join(values)
                    str_conditions.append(f"HTTP Request Method : {str_value}")

            elif field == "host-header":
                if values := condition.get("HostHeaderConfig", {}).get("Values"):
                    str_value = ','.join(values)
                    str_conditions.append(f"Host Header : {str_value}")

            elif field == "path-pattern":
                if values := condition.get("PathPatternConfig", {}).get("Values"):
                    str_value = ','.join(values)
                    str_conditions.append(f"Path Pattern : {str_value}")

            elif field == "query-string":
                if values := condition.get("QueryStringConfig", {}).get("Values"):
                    str_conditions.append("QueryString :")

                    for config in values:
                        key = config.get("Key")
                        value = config.get("Value")

                        if key:
                            str_conditions.append(f" - key={key} : value={value}")
                        else:
                            str_conditions.append(f" - value={value}")

            elif field == "source-ip":
                if values := condition.get("SourceIpConfig", {}).get("Values"):
                    str_value = ','.join(values)
                    str_conditions.append(f"Source IP : {str_value}")

        return str_conditions

    @staticmethod
    def get_formatted_actions(actions: list) -> list:
        str_actions = []

        for action in actions:
            action_type = action.get("Type")

            if action_type == "forward":
                config = action.get("ForwardConfig")
                target_groups = config.get("TargetGroups")
                stickiness = (
                    "on"
                    if config.get("TargetGroupStickinessConfig", {}).get(
                        "Enabled", False
                    )
                    == True
                    else "off"
                )

                str_actions.append("Forward to target group")

                for target_group in target_groups:
                    target = target_group.get("TargetGroupArn")
                    weight = target_group.get("Weight")

                    target_info = f" - {target}"
                    if weight:
                        target_info = f" - {target}: {weight}"

                    str_actions.append(target_info)

                str_actions.append(f" - Target group stickiness: {stickiness}")

            elif action_type == "authenticate-oidc":
                config = action.get("AuthenticateOidcConfig")

                str_actions.extend(
                    [
                        "Authenticate OIDC",
                        f" - Issuer: {config.get('Issuer')}",
                        f" - Client ID: {config.get('ClientId')}",
                        f" - Scope: {config.get('Scope')}",
                        f" - On Unauthenticated Request: {config.get('OnUnauthenticatedRequest')}",
                    ]
                )

            elif action_type == "authenticate-cognito":
                config = action.get("AuthenticateCognitoConfig")

                str_actions.extend(
                    [
                        "Authenticate Cognito",
                        f" - User Pool Arn: {config.get('UserPoolArn')}",
                        f" - User Pool Client ID: {config.get('UserPoolClientId')}",
                        f" - User Pool Domain: {config.get('UserPoolDomain')}",
                        f" - Scope: {config.get('Scope')}",
                        f" - On Unauthenticated Request: {config.get('OnUnauthenticatedRequest')}",
                    ]
                )

            elif action_type == "redirect":
                config = action.get("RedirectConfig")
                protocol = config.get("Protocol")
                port = config.get("Port")
                host = config.get("Host")
                path = config.get("Path")
                query = config.get("Query")
                status_code = config.get("StatusCode")

                str_action = f"Redirect to {protocol}://#{host}:{port}{path}?{query}"
                str_actions.append(str_action)
                str_actions.append(f" - Status code: {status_code}")

            elif action_type == "fixed-response":
                config = action.get("FixedResponseConfig")
                response_code = config.get("StatusCode")
                content_type = config.get("ContentType")

                str_actions.extend(
                    [
                        "Return fixed response",
                        f" - Response code: {response_code}",
                        " - Response body",
                        f" - Response content type: {content_type}",
                    ]
                )

        return str_actions

    def request_loadbalancer(self, region_name):
        load_balancers = []

        paginator = self.elbv2_client.get_paginator("describe_load_balancers")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )

        for data in response_iterator:
            for raw in data.get("LoadBalancers", []):
                raw["attributes"] = self.request_lb_attributes(
                    raw.get("LoadBalancerArn")
                )
                load_balancers.append(raw)

        return load_balancers

    def request_target_health(self, target_group_arn):
        response = self.elbv2_client.describe_target_health(TargetGroupArn=target_group_arn)
        return response.get("TargetHealthDescriptions", [])

    def request_target_group(self, region_name):
        target_groups = []

        paginator = self.elbv2_client.get_paginator("describe_target_groups")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )
        for data in response_iterator:
            for raw in data.get("TargetGroups", []):
                raw["attributes"] = self.request_target_group_attributes(
                    raw.get("TargetGroupArn")
                )
                target_groups.append(raw)

        return target_groups

    def request_listeners(self, lb_arn):
        response = self.elbv2_client.describe_listeners(LoadBalancerArn=lb_arn)
        return response.get("Listeners", [])

    def request_rules_by_listener(self, listener: dict) -> list:
        listener_arn = listener.get("ListenerArn")
        response = self.elbv2_client.describe_rules(ListenerArn=listener_arn)

        return response.get("Rules", [])

    def request_tags(self, resource_arns):
        all_tags = []

        for _arns in self.divide_to_chunks(resource_arns, MAX_TAG_RESOURCES):
            response = self.elbv2_client.describe_tags(ResourceArns=_arns)
            all_tags.extend(response.get("TagDescriptions", []))

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
        ec2_client = self.session.client(
            "ec2", region_name=region_name, verify=BOTO3_HTTPS_VERIFIED
        )

        instances = []
        paginator = ec2_client.get_paginator("describe_instances")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            },
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": [
                        "pending",
                        "running",
                        "shutting-down",
                        "stopping",
                        "stopped",
                    ],
                }
            ],
        )

        for data in response_iterator:
            for _reservation in data.get("Reservations", []):
                instances.extend(_reservation.get("Instances", []))

        return instances

    def request_lb_attributes(self, lb_arn):
        attribute_info = {}

        response = self.elbv2_client.describe_load_balancer_attributes(LoadBalancerArn=lb_arn)
        attrs = response.get("Attributes", [])

        for attr in attrs:
            if attr.get("Key") == "access_logs.s3.enabled":
                if attr.get("Value") == "true":
                    attribute_info["access_logs_s3_enabled"] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info["access_logs_s3_enabled"] = "Disabled"
            elif attr.get("Key") == "access_logs.s3.prefix":
                attribute_info["access_logs_s3_prefix"] = attr.get("Value", "")
            elif attr.get("Key") == "access_logs.s3.bucket":
                attribute_info["access_logs_s3_bucket"] = attr.get("Value", "")
            elif attr.get("Key") == "idle_timeout.timeout_seconds":
                attribute_info["idle_timeout_seconds"] = attr.get("Value", "")
            elif attr.get("Key") == "load_balancing.cross_zone.enabled":
                if attr.get("Value") == "true":
                    attribute_info["load_balancing_cross_zone_enabled"] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info["load_balancing_cross_zone_enabled"] = "Disabled"
            elif attr.get("Key") == "deletion_protection.enabled":
                if attr.get("Value") == "true":
                    attribute_info["deletion_protection_enabled"] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info["deletion_protection_enabled"] = "Disabled"
            elif attr.get("Key") == "routing.http2.enabled":
                if attr.get("Value") == "true":
                    attribute_info["routing_http2_enabled"] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info["routing_http2_enabled"] = "Disabled"
            elif attr.get("Key") == "routing.http.drop_invalid_header_fields.enabled":
                if attr.get("Value") == "true":
                    attribute_info[
                        "routing_http_drop_invalid_header_fields_enabled"
                    ] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info[
                        "routing_http_drop_invalid_header_fields_enabled"
                    ] = "Disabled"
            elif attr.get("Key") == "routing.http.desync_mitigation_mode":
                attribute_info["routing_http_desync_mitigation_mode"] = attr.get(
                    "Value", ""
                )
            elif attr.get("Key") == "waf.fail_open.enabled":
                if attr.get("Value") == "true":
                    attribute_info["waf_fail_open_enabled"] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info["waf_fail_open_enabled"] = "Disabled"

        return LoadBalancerAttributes(attribute_info, strict=False)

    def request_target_group_attributes(self, tg_arn):
        attribute_info = {}

        response = self.elbv2_client.describe_target_group_attributes(TargetGroupArn=tg_arn)
        attrs = response.get("Attributes")

        for attr in attrs:
            if attr.get("Key") == "stickiness.enabled":
                if attr.get("Value") == "true":
                    attribute_info["stickiness_enabled"] = "Enabled"
                elif attr.get("Value") == "false":
                    attribute_info["stickiness_enabled"] = "Disabled"

            elif attr.get("Key") == "deregistration_delay.timeout_seconds":
                attribute_info["deregistration_delay_timeout_seconds"] = attr.get(
                    "Value", ""
                )

            elif attr.get("Key") == "stickiness.type":
                attribute_info["stickiness_type"] = attr.get("Value", "")

            elif attr.get("Key") == "stickiness.lb_cookie.duration_seconds":
                attribute_info["stickiness_lb_cookie.duration_seconds"] = attr.get(
                    "Value", ""
                )

            elif attr.get("Key") == "slow_start.duration_seconds":
                attribute_info["slow_start_duration_seconds"] = attr.get("Value", "")

            elif attr.get("Key") == "load_balancing.algorithm.type":
                attribute_info["load_balancing_algorithm_type"] = attr.get("Value", "")

        return TargetGroupAttributes(attribute_info, strict=False)

    def request_classic_loadbalancer(self):
        classic_load_balancers = []

        paginator = self.classic_client.get_paginator("describe_load_balancers")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 400,
            }
        )

        for data in response_iterator:
            for raw in data.get("LoadBalancerDescriptions", []):
                classic_load_balancers.append(raw)

        return classic_load_balancers

    def request_classic_lb_attributes(self, lb_name):
        attribute_info = {}

        try:
            response = self.classic_client.describe_load_balancer_attributes(
                LoadBalancerName=lb_name
            )
            attrs = response.get("LoadBalancerAttributes", {})

            # CrossZoneLoadBalancing
            cross_zone = attrs.get("CrossZoneLoadBalancing", {})
            if cross_zone.get("Enabled"):
                attribute_info["load_balancing_cross_zone_enabled"] = "Enabled"
            else:
                attribute_info["load_balancing_cross_zone_enabled"] = "Disabled"

            # AccessLog
            access_log = attrs.get("AccessLog", {})
            if access_log.get("Enabled"):
                attribute_info["access_logs_s3_enabled"] = "Enabled"
                attribute_info["access_logs_s3_bucket"] = access_log.get(
                    "S3BucketName", ""
                )
                attribute_info["access_logs_s3_prefix"] = access_log.get(
                    "S3BucketPrefix", ""
                )
            else:
                attribute_info["access_logs_s3_enabled"] = "Disabled"

            # ConnectionSettings (IdleTimeout)
            connection_settings = attrs.get("ConnectionSettings", {})
            if connection_settings.get("IdleTimeout"):
                attribute_info["idle_timeout_seconds"] = str(
                    connection_settings.get("IdleTimeout")
                )

            # Note: Classic ELB does not have deletion_protection concept
            # ConnectionDraining is a different feature (graceful deregistration)

        except Exception as e:
            _LOGGER.debug(f"[request_classic_lb_attributes] Error: {e}")

        return LoadBalancerAttributes(attribute_info, strict=False)

    def request_classic_instance_health(self, lb_name):
        try:
            response = self.classic_client.describe_instance_health(
                LoadBalancerName=lb_name
            )
            return response.get("InstanceStates", [])
        except Exception as e:
            _LOGGER.debug(f"[request_classic_instance_health] Error: {e}")
            return []

    def request_classic_tags(self, lb_names):
        all_tags = []

        for _names in self.divide_to_chunks(lb_names, MAX_TAG_RESOURCES):
            try:
                response = self.classic_client.describe_tags(LoadBalancerNames=_names)
                all_tags.extend(response.get("TagDescriptions", []))
            except Exception as e:
                _LOGGER.debug(f"[request_classic_tags] Error: {e}")

        return all_tags

    def generate_classic_elb_arn(self, lb_name, region_name):
        return f"arn:aws:elasticloadbalancing:{region_name}:{self.account_id}:loadbalancer/{lb_name}"

    def classic_elb_cloudwatch(self, raw_lb, region_name):
        return self.set_cloudwatch(
            "AWS/ELB", "LoadBalancerName", raw_lb["LoadBalancerName"], region_name
        )

    @staticmethod
    def search_classic_tags(all_tags, lb_name):
        for tag_desc in all_tags:
            if tag_desc.get("LoadBalancerName") == lb_name:
                return tag_desc.get("Tags", [])
        return []

    def convert_classic_to_lb_format(
        self, raw_classic_lb, arn, region_name, attributes, instance_health, ec2_instances
    ):
        """Convert Classic ELB data to LoadBalancer model format"""
        lb_name = raw_classic_lb.get("LoadBalancerName")

        # Convert AvailabilityZones (string list) to LoadBalancerAvailabilityZones format
        availability_zones = []
        classic_azs = raw_classic_lb.get("AvailabilityZones", [])
        classic_subnets = raw_classic_lb.get("Subnets", [])

        for idx, az in enumerate(classic_azs):
            az_info = {"ZoneName": az}
            if idx < len(classic_subnets):
                az_info["SubnetId"] = classic_subnets[idx]
            availability_zones.append(az_info)

        # Convert ListenerDescriptions to Listener format
        listeners = []
        for listener_desc in raw_classic_lb.get("ListenerDescriptions", []):
            listener = listener_desc.get("Listener", {})
            listeners.append(
                Listener(
                    {
                        "Port": listener.get("LoadBalancerPort"),
                        "Protocol": listener.get("Protocol"),
                    },
                    strict=False,
                )
            )

        # Match instances with EC2 instance data
        match_instances = []
        classic_instances = raw_classic_lb.get("Instances", [])
        instance_health_map = {
            ih.get("InstanceId"): ih for ih in instance_health
        }

        for classic_instance in classic_instances:
            instance_id = classic_instance.get("InstanceId")
            health_info = instance_health_map.get(instance_id, {})

            # Find matching EC2 instance
            for ec2_instance in ec2_instances:
                if ec2_instance.get("InstanceId") == instance_id:
                    # Map health state to instance state
                    health_state = health_info.get("State", "Unknown")
                    state_name = "running" if health_state == "InService" else "stopped"

                    ec2_instance.update(
                        {
                            "instance_name": self.get_instance_name_from_tag(ec2_instance),
                        }
                    )
                    match_instances.append(Instance(ec2_instance, strict=False))
                    break

        # Build converted LoadBalancer data
        converted_lb = {
            "LoadBalancerArn": arn,
            "LoadBalancerName": lb_name,
            "DNSName": raw_classic_lb.get("DNSName"),
            "CanonicalHostedZoneId": raw_classic_lb.get("CanonicalHostedZoneNameID"),
            "CreatedTime": raw_classic_lb.get("CreatedTime"),
            "Scheme": raw_classic_lb.get("Scheme"),
            "VpcId": raw_classic_lb.get("VPCId"),
            "State": None,
            "Type": "classic",
            "AvailabilityZones": availability_zones,
            "SecurityGroups": raw_classic_lb.get("SecurityGroups", []),
            "IpAddressType": None,
            "region_name": region_name,
            "listeners": listeners,
            "listener_rules": None,
            "target_groups": None,
            "attributes": attributes,
            "instances": match_instances,
            "stats": {"instances_size": len(match_instances)},
        }

        return converted_lb

    def elb_cloudwatch(self, raw_lb, region_name):
        cloudwatch_elb = self.set_cloudwatch(
            "AWS/ELB", "LoadBalancerName", raw_lb["LoadBalancerName"], region_name
        )

        cloudwatch_elb_type = None
        if raw_lb.get("Type") == "application":
            elb_id = self.get_elb_id_from_arn(raw_lb["LoadBalancerArn"])
            if elb_id:
                cloudwatch_elb_type = self.set_cloudwatch(
                    "AWS/ApplicationELB", "LoadBalancer", elb_id, region_name
                )
        elif raw_lb.get("Type") == "network":
            elb_id = self.get_elb_id_from_arn(raw_lb["LoadBalancerArn"])
            if elb_id:
                cloudwatch_elb_type = self.set_cloudwatch(
                    "AWS/NetworkELB", "LoadBalancer", elb_id, region_name
                )

        metrics_info = cloudwatch_elb.metrics_info
        if cloudwatch_elb_type:
            metrics_info = metrics_info + cloudwatch_elb_type.metrics_info

        cloudwatch_vo = CloudWatchModel(
            {"region_name": region_name, "metrics_info": metrics_info}, strict=False
        )

        return cloudwatch_vo

    @staticmethod
    def search_tags(all_tags, resource_arn):
        for tag in all_tags:
            if tag.get("ResourceArn") == resource_arn:
                return tag.get("Tags", [])

        return []

    @staticmethod
    def get_instance_name_from_tag(instance):
        for tag in instance.get("Tags", []):
            if tag.get("Key") == "Name":
                return tag.get("Value")

        return None

    @staticmethod
    def get_elb_id_from_arn(arn):
        try:
            split_id = arn.split("/")[1:]
            return "/".join(split_id)
        except Exception as e:
            return None
