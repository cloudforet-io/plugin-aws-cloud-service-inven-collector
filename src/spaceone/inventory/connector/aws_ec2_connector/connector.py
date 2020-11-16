import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ec2_connector.schema.data import SecurityGroup, SecurityGroupIpPermission, \
    Image, LaunchPermission
from spaceone.inventory.connector.aws_ec2_connector.schema.resource import SecurityGroupResource, SecurityGroupResponse, \
    ImageResource, ImageResponse
from spaceone.inventory.connector.aws_ec2_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EC2Connector(SchematicAWSConnector):
    service_name = 'ec2'

    include_vpc_default = False

    def get_resources(self) -> List[SecurityGroupResource]:
        print("** EC2 Manager START **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_security_group_data,
                'resource': SecurityGroupResource,
                'response_schema': SecurityGroupResponse
            },
            {
                'request_method': self.request_ami_data,
                'resource': ImageResource,
                'response_schema': ImageResponse
            },
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' EC2 Finished {time.time() - start_time} Seconds')
        return resources

    def request_ami_data(self, region_name) -> List[Image]:
        results = self.client.describe_images(Owners=['self'])

        for image in results.get('Images', []):
            try:
                permission_info = self.client.describe_image_attribute(Attribute='launchPermission', ImageId=image['ImageId'])
            except Exception as e:
                permission_info = {}

            if permission_info:
                image.update({
                    'launch_permissions': [LaunchPermission(_permission, strict=False) for _permission in permission_info.get('LaunchPermissions', [])]
                })

            yield Image(image, strict=False)

    def request_security_group_data(self, region_name) -> List[SecurityGroup]:
        # Get default VPC
        default_vpcs = self._get_default_vpc()

        # Get Security Group
        paginator = self.client.get_paginator('describe_security_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('SecurityGroups', []):
                if self.include_vpc_default is False and raw.get('VpcId') in default_vpcs:
                    continue

                # Inbound Rules
                inbound_rules = []
                for in_rule in raw.get('IpPermissions', []):
                    for _ip_range in in_rule.get('IpRanges', []):
                        inbound_rules.append(
                            SecurityGroupIpPermission(self.custom_security_group_rule_info(in_rule, _ip_range,
                                                                                           'ip_ranges'),
                                                      strict=False))

                    for _user_group_pairs in in_rule.get('UserIdGroupPairs', []):
                        inbound_rules.append(
                            SecurityGroupIpPermission(self.custom_security_group_rule_info(in_rule, _user_group_pairs,
                                                                                           'user_id_group_pairs'),
                                                      strict=False))

                    for _ip_v6_range in in_rule.get('Ipv6Ranges', []):
                        inbound_rules.append(
                            SecurityGroupIpPermission(self.custom_security_group_rule_info(in_rule, _ip_v6_range,
                                                                                           'ipv6_ranges'),
                                                      strict=False))

                # Outbound Rules
                outbound_rules = []
                for out_rule in raw.get('IpPermissionsEgress', []):
                    for _ip_range in out_rule.get('IpRanges', []):
                        outbound_rules.append(
                            SecurityGroupIpPermission(self.custom_security_group_rule_info(out_rule, _ip_range,
                                                                                           'ip_ranges'),
                                                      strict=False))

                    for _user_group_pairs in out_rule.get('UserIdGroupPairs', []):
                        outbound_rules.append(
                            SecurityGroupIpPermission(self.custom_security_group_rule_info(out_rule, _user_group_pairs,
                                                                                           'user_id_group_pairs'),
                                                      strict=False))

                    for _ip_v6_range in out_rule.get('Ipv6Ranges', []):
                        outbound_rules.append(
                            SecurityGroupIpPermission(self.custom_security_group_rule_info(out_rule, _ip_v6_range,
                                                                                           'ipv6_ranges'),
                                                      strict=False))

                raw.update({
                    'account_id': self.account_id,
                    'ip_permissions': inbound_rules,
                    'ip_permissions_egress': outbound_rules
                })

                result = SecurityGroup(raw, strict=False)
                yield result

    def custom_security_group_rule_info(self, raw_rule, remote, remote_type):
        raw_rule.update({
            'protocol_display': self._get_protocol_display(raw_rule.get('IpProtocol')),
            'port_display': self._get_port_display(raw_rule),
            'source_display': self._get_source_display(remote),
            'description_display': self._get_description_display(remote),
            remote_type: remote
        })

        return raw_rule

    @staticmethod
    def _get_protocol_display(raw_protocol):
        if raw_protocol == '-1':
            return 'ALL'
        elif raw_protocol == 'tcp':
            return 'TCP'
        elif raw_protocol == 'udp':
            return 'UDP'
        elif raw_protocol == 'icmp':
            return 'ICMP'
        else:
            return raw_protocol

    @staticmethod
    def _get_port_display(raw_rule):
        _protocol = raw_rule.get('IpProtocol')

        if _protocol == '-1':
            return 'ALL'
        elif _protocol in ['tcp', 'udp']:
            from_port = raw_rule.get('FromPort')
            to_port = raw_rule.get('ToPort')

            if from_port == 0 and to_port == 65535:
                return 'ALL'

            if from_port == to_port:
                return f'{from_port}'

            if from_port is not None and to_port is not None:
                return f'{from_port} - {to_port}'

            return ''
        elif _protocol == 'icmp':
            return 'ALL'
        else:
            return ''

    @staticmethod
    def _get_source_display(remote):
        if cidr := remote.get('CidrIp'):
            return cidr
        elif group_id := remote.get('GroupId'):
            return group_id
        elif cidrv6 := remote.get('CidrIpv6'):
            return cidrv6

        return ''

    @staticmethod
    def _get_description_display(remote):
        if description := remote.get('Description'):
            return description

        return ''

    def _get_default_vpc(self):
        default_vpcs = []
        vpc_response = self.client.describe_vpcs()
        for _vpc in vpc_response['Vpcs']:
            if _vpc.get('IsDefault', False):
                default_vpcs.append(_vpc['VpcId'])

        return default_vpcs
