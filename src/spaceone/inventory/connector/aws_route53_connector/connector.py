import time
import logging
from typing import List

from spaceone.inventory.connector.aws_route53_connector.schema.data import HostedZone, RecordSet
from spaceone.inventory.connector.aws_route53_connector.schema.resource import HostedZoneResource, HostedZoneResponse
from spaceone.inventory.connector.aws_route53_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel, CloudWatchModel

_LOGGER = logging.getLogger(__name__)


class Route53Connector(SchematicAWSConnector):
    response_schema = HostedZoneResponse
    service_name = 'route53'
    cloud_service_group = 'Route53'
    cloud_service_type = 'HostedZone'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[HostedZoneResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Route53")
        resources = []
        start_time = time.time()

        try:
            resources.extend(self.set_service_code_in_cloud_service_type())

            # merge data
            for data in self.request_data():
                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:
                    if getattr(data, 'set_cloudwatch', None):
                        data.cloudwatch = CloudWatchModel(data.set_cloudwatch())

                    resources.append(self.response_schema(
                        {'resource': HostedZoneResource({
                            'name': data.name,
                            'data': data,
                            'instance_type': data.type,
                            'account': self.account_id,
                            'reference': ReferenceModel(data.reference()),
                            'region_code': 'global'
                        })}))

        except Exception as e:
            resource_id = ''
            resources.append(self.generate_error('global', resource_id, e))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Route53 ({time.time() - start_time} sec)')
        return resources

    def request_data(self) -> List[HostedZone]:
        cloudtrail_resource_type = 'AWS::Route53::HostedZone'
        paginator = self.client.get_paginator('list_hosted_zones')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('HostedZones', []):
                try:
                    raw.update({
                        'type': self.set_hosted_zone_type(raw['Config']['PrivateZone']),
                        'hosted_zone_id': self.get_hosted_zone_id(raw['Id']),
                        'record_sets': list(self.describe_record_sets(raw['Id'])),
                        'arn': self.generate_arn(service=self.service_name, region="", account_id="",
                                                 resource_type="hostedzone", resource_id=raw['Id'])
                    })

                    raw.update({'cloudtrail': self.set_cloudtrail('us-east-1', cloudtrail_resource_type, raw['hosted_zone_id'])})

                    yield HostedZone(raw, strict=False)
                except Exception as e:
                    resource_id = raw.get('Id', '')
                    error_resource_response = self.generate_error('global', resource_id, e)
                    yield error_resource_response

    def describe_record_sets(self, host_zone_id):
        paginator = self.client.get_paginator('list_resource_record_sets')
        response_iterator = paginator.paginate(
            HostedZoneId=host_zone_id,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('ResourceRecordSets', []):
                display_values = []
                if raw.get('Type') == 'A':
                    _alias = raw.get('AliasTarget', {})
                    if dns_name := _alias.get('DNSName'):
                        display_values.append(dns_name)
                else:
                    _records = raw.get('ResourceRecords', [])
                    for _r in _records:
                        display_values.append(_r.get('Value'))

                if len(display_values) > 0:
                    raw.update({'display_values': display_values})

                res = RecordSet(raw, strict=False)
                yield res

    @staticmethod
    def get_hosted_zone_id(id):
        return id.split('/')[2]

    @staticmethod
    def set_hosted_zone_type(private_zone):
        if private_zone is True:
            return "Private"
        else:
            return "Public"
