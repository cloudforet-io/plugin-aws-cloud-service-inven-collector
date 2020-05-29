import logging
from typing import List

import boto3

from spaceone.inventory.connector.aws_eip_connector.schema.data import ElasticIPAddress, ElasticIPAddressTags
from spaceone.inventory.connector.aws_eip_connector.schema.resource import EIPResource, EIPResponse
from spaceone.inventory.connector.aws_eip_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class EIPConnector(SchematicAWSConnector):
    response_schema = EIPResponse
    service_name = 'ec2'

    def get_resources(self) -> List[EIPResource]:
        print("** EIP START **")
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': EIPResource({'data': data,
                                              'reference': ReferenceModel(data.reference)})})

    def request_data(self, region_name) -> List[ElasticIPAddress]:
        nat_gateways = None
        network_interfaces = None
        response = self.client.describe_addresses()
        eips = response.get('Addresses', [])

        if len(eips) > 0:
            nat_gateways = self._describe_nat_gateways()
            network_interfaces = self._describe_network_interfaces([eip.get('NetworkInterfaceId') for eip in eips if eip.get('NetworkInterfaceId')])

        for _ip in eips:
            if nat_gw_id := self._match_nat_gw(_ip, nat_gateways):
                _ip['nat_gateway_id'] = nat_gw_id

            if public_dns := self._match_network_interface_public_dns(_ip, network_interfaces):
                _ip['public_dns'] = public_dns

            _ip.update({
                'region_name': region_name,
                'account_id': self.account_id,
                'name': self._get_name_from_tags(_ip.get('Tags', []))
            })
            result = ElasticIPAddress(_ip, strict=False)
            yield result

    def _describe_nat_gateways(self):
        response = self.client.describe_nat_gateways()
        return response.get('NatGateways', [])

    def _describe_network_interfaces(self, nif_ids):
        response = self.client.describe_network_interfaces(NetworkInterfaceIds=nif_ids)

        return response.get('NetworkInterfaces', [])

    @staticmethod
    def _match_network_interface_public_dns(ip, network_interfaces):
        for nif in network_interfaces:
            if ip == nif['Association']['PublicIp']:
                return nif['Association']['PublicDnsName']

        return None

    @staticmethod
    def _match_nat_gw(ip, nat_gateways):
        for nat_gw in nat_gateways:
            nat_gw_address = nat_gw['NatGatewayAddresses'][0]
            if ip == nat_gw_address['PublicIp']:
                return nat_gw['NatGatewayId']

        return None

    @staticmethod
    def _get_name_from_tags(tags):
        for tag in tags:
            if 'Name' in tag.get('Key'):
                return tag.get('Value')

        return ""
