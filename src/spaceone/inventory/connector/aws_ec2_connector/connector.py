import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ec2_connector.schema.data import (
    SecurityGroup,
    SecurityGroupIpPermission,
    Image,
    LaunchPermission,
    Instance,
)
from spaceone.inventory.connector.aws_ec2_connector.schema.resource import (
    SecurityGroupResource,
    SecurityGroupResponse,
    ImageResource,
    ImageResponse,
)
from spaceone.inventory.connector.aws_ec2_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EC2Connector(SchematicAWSConnector):
    service_name = "ec2"
    cloud_service_group = "EC2"
    cloud_service_types = CLOUD_SERVICE_TYPES

    include_vpc_default = False

    def get_resources(self) -> List[SecurityGroupResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: EC2")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        collect_resources = [
            {
                "request_method": self.request_security_group_data,
                "resource": SecurityGroupResource,
                "response_schema": SecurityGroupResponse,
            },
            {
                "request_method": self.request_ami_data,
                "resource": ImageResource,
                "response_schema": ImageResponse,
            },
        ]

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)

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
            f"[get_resources][account_id: {self.account_id}] FINISHED: EC2 ({time.time() - start_time} sec)"
        )
        return resources

    def request_ami_data(self, region_name) -> List[Image]:
        self.cloud_service_type = "AMI"
        cloudtrail_resource_type = "AWS::EC2::Ami"

        results = self.client.describe_images(Owners=["self"])

        for image in results.get("Images", []):
            try:
                try:
                    permission_info = self.client.describe_image_attribute(
                        Attribute="launchPermission", ImageId=image["ImageId"]
                    )

                    if permission_info:
                        image.update(
                            {
                                "launch_permissions": [
                                    LaunchPermission(_permission, strict=False)
                                    for _permission in permission_info.get(
                                        "LaunchPermissions", []
                                    )
                                ]
                            }
                        )

                except Exception as e:
                    _LOGGER.debug(f"[ami][request_ami_data] SKIP: {e}")

                image.update(
                    {
                        "cloudtrail": self.set_cloudtrail(
                            region_name, cloudtrail_resource_type, image["ImageId"]
                        )
                    }
                )

                image_vo = Image(image, strict=False)
                yield {
                    "data": image_vo,
                    "name": image_vo.name,
                    "instance_type": image_vo.image_type,
                    "account": self.account_id,
                    "tags": self.convert_tags_to_dict_type(image.get("Tags", [])),
                }

            except Exception as e:
                resource_id = image.get("ImageId", "")
                error_resource_response = self.generate_error(
                    region_name, resource_id, e
                )
                yield {"data": error_resource_response}

    def request_security_group_data(self, region_name) -> List[SecurityGroup]:
        self.cloud_service_type = "SecurityGroup"
        cloudtrail_resource_type = "AWS::EC2::SecurityGroup"

        # Get default VPC
        default_vpcs = self._get_default_vpc()

        # Get EC2 Instances
        instances = self.list_instances()

        # Get Security Group
        paginator = self.client.get_paginator("describe_security_groups")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )

        for data in response_iterator:
            for raw in data.get("SecurityGroups", []):
                try:
                    if (
                        self.include_vpc_default is False
                        and raw.get("VpcId") in default_vpcs
                    ):
                        continue

                    # Inbound Rules
                    inbound_rules = []
                    for in_rule in raw.get("IpPermissions", []):
                        for _ip_range in in_rule.get("IpRanges", []):
                            inbound_rules.append(
                                SecurityGroupIpPermission(
                                    self.custom_security_group_rule_info(
                                        in_rule, _ip_range, "ip_ranges"
                                    ),
                                    strict=False,
                                )
                            )

                        for _user_group_pairs in in_rule.get("UserIdGroupPairs", []):
                            inbound_rules.append(
                                SecurityGroupIpPermission(
                                    self.custom_security_group_rule_info(
                                        in_rule,
                                        _user_group_pairs,
                                        "user_id_group_pairs",
                                    ),
                                    strict=False,
                                )
                            )

                        for _ip_v6_range in in_rule.get("Ipv6Ranges", []):
                            inbound_rules.append(
                                SecurityGroupIpPermission(
                                    self.custom_security_group_rule_info(
                                        in_rule, _ip_v6_range, "ipv6_ranges"
                                    ),
                                    strict=False,
                                )
                            )

                    # Outbound Rules
                    outbound_rules = []
                    for out_rule in raw.get("IpPermissionsEgress", []):
                        for _ip_range in out_rule.get("IpRanges", []):
                            outbound_rules.append(
                                SecurityGroupIpPermission(
                                    self.custom_security_group_rule_info(
                                        out_rule, _ip_range, "ip_ranges"
                                    ),
                                    strict=False,
                                )
                            )

                        for _user_group_pairs in out_rule.get("UserIdGroupPairs", []):
                            outbound_rules.append(
                                SecurityGroupIpPermission(
                                    self.custom_security_group_rule_info(
                                        out_rule,
                                        _user_group_pairs,
                                        "user_id_group_pairs",
                                    ),
                                    strict=False,
                                )
                            )

                        for _ip_v6_range in out_rule.get("Ipv6Ranges", []):
                            outbound_rules.append(
                                SecurityGroupIpPermission(
                                    self.custom_security_group_rule_info(
                                        out_rule, _ip_v6_range, "ipv6_ranges"
                                    ),
                                    strict=False,
                                )
                            )

                    raw.update(
                        {
                            "ip_permissions": inbound_rules,
                            "ip_permissions_egress": outbound_rules,
                            "instances": self.get_security_group_map_instances(
                                raw, instances
                            ),
                            "cloudtrail": self.set_cloudtrail(
                                region_name, cloudtrail_resource_type, raw["GroupId"]
                            ),
                        }
                    )
                    sg_vo = SecurityGroup(raw, strict=False)
                    yield {
                        "data": sg_vo,
                        "name": sg_vo.group_name,
                        "account": self.account_id,
                        "tags": self.convert_tags_to_dict_type(raw.get("Tags", [])),
                    }

                except Exception as e:
                    resource_id = raw.get("GroupId", "")
                    error_resource_response = self.generate_error(
                        region_name, resource_id, e
                    )
                    yield {"data": error_resource_response}

    def custom_security_group_rule_info(self, raw_rule, remote, remote_type):
        raw_rule.update(
            {
                "protocol_display": self._get_protocol_display(
                    raw_rule.get("IpProtocol")
                ),
                "port_display": self._get_port_display(raw_rule),
                "source_display": self._get_source_display(remote),
                "description_display": self._get_description_display(remote),
                remote_type: remote,
            }
        )

        return raw_rule

    def list_instances(self):
        instances = []
        paginator = self.client.get_paginator("describe_instances")
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

    def _get_default_vpc(self):
        default_vpcs = []
        vpc_response = self.client.describe_vpcs()
        for _vpc in vpc_response["Vpcs"]:
            if _vpc.get("IsDefault", False):
                default_vpcs.append(_vpc["VpcId"])

        return default_vpcs

    def get_security_group_map_instances(self, security_group, instances):
        sg_map_instances = []

        for instance in instances:
            for instance_sg in instance.get("SecurityGroups", []):
                if security_group.get("GroupId") == instance_sg.get("GroupId"):
                    instance["instance_name"] = self.get_instance_name_from_tags(
                        instance
                    )
                    sg_map_instances.append(instance)

        return [
            Instance(sg_map_instance, strict=False)
            for sg_map_instance in sg_map_instances
        ]

    @staticmethod
    def _get_protocol_display(raw_protocol):
        if raw_protocol == "-1":
            return "ALL"
        elif raw_protocol == "tcp":
            return "TCP"
        elif raw_protocol == "udp":
            return "UDP"
        elif raw_protocol == "icmp":
            return "ICMP"
        else:
            return raw_protocol

    @staticmethod
    def _get_port_display(raw_rule):
        _protocol = raw_rule.get("IpProtocol")

        if _protocol == "-1":
            return "ALL"
        elif _protocol in ["tcp", "udp"]:
            from_port = raw_rule.get("FromPort")
            to_port = raw_rule.get("ToPort")

            if from_port == 0 and to_port == 65535:
                return "ALL"

            if from_port == to_port:
                return f"{from_port}"

            if from_port is not None and to_port is not None:
                return f"{from_port} - {to_port}"

            return ""
        elif _protocol == "icmp":
            return "ALL"
        else:
            return ""

    @staticmethod
    def _get_source_display(remote):
        if cidr := remote.get("CidrIp"):
            return cidr
        elif group_id := remote.get("GroupId"):
            return group_id
        elif cidrv6 := remote.get("CidrIpv6"):
            return cidrv6

        return ""

    @staticmethod
    def _get_description_display(remote):
        if description := remote.get("Description"):
            return description

        return ""

    @staticmethod
    def get_instance_name_from_tags(instance):
        for _tag in instance.get("Tags", []):
            if _tag.get("Key") == "Name":
                return _tag.get("Value")

        return ""
