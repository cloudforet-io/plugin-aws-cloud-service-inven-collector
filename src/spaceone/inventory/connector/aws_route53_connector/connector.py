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

    def get_resources(self) -> List[HostedZoneResource]:
        print("** Route53 START **")
        resources = []
        start_time = time.time()

        try:
            # init cloud service type
            for cst in CLOUD_SERVICE_TYPES:
                resources.append(cst)

            # merge data
            for data in self.request_data():
                if getattr(data, 'set_cloudwatch', None):
                    data.cloudwatch = CloudWatchModel(data.set_cloudwatch())

                resources.append(self.response_schema(
                    {'resource': HostedZoneResource({'data': data,
                                                     'reference': ReferenceModel(data.reference()),
                                                     'region_code': 'global'
                                                     })}))
        except Exception as e:
            print(f'[ERROR {self.service_name}] {e}')

        print(f' Route53 Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self) -> List[HostedZone]:
        paginator = self.client.get_paginator('list_hosted_zones')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('HostedZones', []):
                raw.update({
                    'type': self.set_hosted_zone_type(raw['Config']['PrivateZone']),
                    'hosted_zone_id': self.get_hosted_zone_id(raw['Id']),
                    'record_sets': list(self.describe_record_sets(raw['Id'])),
                    'account_id': self.account_id,
                    'arn': self.generate_arn(service=self.service_name, region="", account_id="",
                                             resource_type="hostedzone", resource_id=raw['Id'])
                })

                res = HostedZone(raw, strict=False)
                yield res

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
