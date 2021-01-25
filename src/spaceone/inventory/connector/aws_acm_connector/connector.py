import time
import logging
from typing import List

from spaceone.inventory.connector.aws_acm_connector.schema.data import Certificate, Tags
from spaceone.inventory.connector.aws_acm_connector.schema.resource import ACMResource, CertificateResource, ACMResponse
from spaceone.inventory.connector.aws_acm_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class ACMConnector(SchematicAWSConnector):
    service_name = 'acm'

    def get_resources(self):
        print("** Certificate Manager Start **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_data,
                'resource': CertificateResource,
                'response_schema': ACMResponse
            }
        ]

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' Certificate Manager Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[Certificate]:
        paginator = self.client.get_paginator('list_certificates')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        
        for data in response_iterator:
            for raw in data.get('CertificateSummaryList', []):
                certificate_response = self.client.describe_certificate(CertificateArn=raw.get('CertificateArn'))
                certificate_info = certificate_response.get('Certificate', {})

                certificate_info.update({
                    'identifier': self.get_identifier(certificate_info.get('CertificateArn')),
                    'additional_names_display': self.get_additional_names_display(certificate_info.get('SubjectAlternativeNames')),
                    'in_use_display': self.get_in_use_display(certificate_info.get('InUseBy')),
                    'tags': self.get_tags(certificate_info.get('CertificateArn')),
                    'account_id': self.account_id
                })

                res = Certificate(certificate_info, strict=False)
                yield res

    def get_tags(self, arn):
        tag_response = self.client.list_tags_for_certificate(CertificateArn=arn)
        return tag_response.get('Tags', [])

    @staticmethod
    def get_identifier(certificate_arn):
        return certificate_arn.split('/')[-1]

    @staticmethod
    def get_additional_names_display(subject_alternative_names):
        return subject_alternative_names[1:]

    @staticmethod
    def get_in_use_display(in_use_by):
        if in_use_by:
            return 'Yes'
        else:
            return 'No'
