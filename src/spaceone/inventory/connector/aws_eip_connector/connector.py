import time
import logging
from typing import List

from spaceone.inventory.connector.aws_eip_connector.schema.data import ElasticIPAddress
from spaceone.inventory.connector.aws_eip_connector.schema.resource import EIPResource, EIPResponse
from spaceone.inventory.connector.aws_eip_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EIPConnector(SchematicAWSConnector):
    service_name = 'ec2'
    cloud_service_group = 'EC2'
    cloud_service_type = 'EIP'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[EIPResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: EIP")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        collect_resource = {
            'request_method': self.request_data,
            'resource': EIPResource,
            'response_schema': EIPResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: EIP ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[ElasticIPAddress]:
        nat_gateways = None
        network_interfaces = None
        cloudtrail_resource_type = 'AWS::EC2::EIP'

        response = self.client.describe_addresses()
        eips = response.get('Addresses', [])

        if len(eips) > 0:
            nat_gateways = self._describe_nat_gateways()
            network_interfaces = self._describe_network_interfaces([eip.get('NetworkInterfaceId') for eip in eips
                                                                    if eip.get('NetworkInterfaceId')])

        for _ip in eips:
            try:
                public_ip = _ip.get('PublicIp')

                if public_ip is not None:
                    if nat_gw_id := self._match_nat_gw(public_ip, nat_gateways):
                        _ip['nat_gateway_id'] = nat_gw_id

                    if public_dns := self._match_network_interface_public_dns(public_ip, network_interfaces):
                        _ip['public_dns'] = public_dns

                _ip.update({
                    'allocation_status': 'In-use' if _ip.get('AllocationId') else 'Unused',
                    'name': self._get_name_from_tags(_ip.get('Tags', [])),
                    'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, _ip['AllocationId']),
                })

                eip_vo = ElasticIPAddress(_ip, strict=False)

                yield {
                    'data': eip_vo,
                    'name': eip_vo.name,
                    'account': self.account_id,
                    'tags': self.convert_tags_to_dict_type(_ip.get('Tags', []))
                }

            except Exception as e:
                resource_id = _ip.get('PublicIp', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def _describe_nat_gateways(self):
        response = self.client.describe_nat_gateways()
        return response.get('NatGateways', [])

    def _describe_network_interfaces(self, nif_ids):
        response = self.client.describe_network_interfaces(NetworkInterfaceIds=nif_ids)

        return response.get('NetworkInterfaces', [])

    @staticmethod
    def _match_network_interface_public_dns(ip, network_interfaces):
        for nif in network_interfaces:
            if association := nif.get('Association'):
                if ip == association.get('PublicIp'):
                    return association.get('PublicDnsName', None)

        return None

    @staticmethod
    def _match_nat_gw(ip, nat_gateways):
        for nat_gw in nat_gateways:
            nat_gw_address = nat_gw.get('NatGatewayAddresses', [{}])[0]
            if ip == nat_gw_address.get('PublicIp'):
                return nat_gw.get('NatGatewayId')

        return None

    @staticmethod
    def _get_name_from_tags(tags):
        for tag in tags:
            if 'Name' in tag.get('Key'):
                return tag.get('Value')

        return ""
