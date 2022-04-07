import time
import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_acm_connector.schema.data import Certificate, Tags
from spaceone.inventory.connector.aws_acm_connector.schema.resource import ACMResource, CertificateResource, ACMResponse
from spaceone.inventory.connector.aws_acm_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)


class ACMConnector(SchematicAWSConnector):
    service_name = 'acm'
    cloud_service_group = 'CertificateManager'
    cloud_service_type = 'Certificate'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: Certificate Manager")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        collect_resources = [
            {
                'request_method': self.request_data,
                'resource': CertificateResource,
                'response_schema': ACMResponse
            }
        ]

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: Certificate Manager ({time.time() - start_time} sec)')
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
                try:
                    certificate_response = self.client.describe_certificate(CertificateArn=raw.get('CertificateArn'))
                    certificate_info = certificate_response.get('Certificate', {})
    
                    certificate_info.update({
                        'type_display': self.get_string_title(certificate_info.get('Type')),
                        'renewal_eligibility_display': self.get_string_title(certificate_info.get('RenewalEligibility')),
                        'identifier': self.get_identifier(certificate_info.get('CertificateArn')),
                        'additional_names_display': self.get_additional_names_display(certificate_info.get('SubjectAlternativeNames')),
                        'in_use_display': self.get_in_use_display(certificate_info.get('InUseBy')),
                        'tags': self.get_tags(certificate_info.get('CertificateArn')),
                        'account_id': self.account_id
                    })
    
                    certificate_vo = Certificate(certificate_info, strict=False)
                    yield {
                        'data': certificate_vo,
                        'name': certificate_vo.domain_name,
                        'instance_type': certificate_vo.type_display,
                        'account': self.account_id,
                        'launched_at': self.datetime_to_iso8601(certificate_vo.created_at)
                    }
                    
                except Exception as e:
                    resource_id = raw.get('CertificateArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}
                    
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

    @staticmethod
    def get_string_title(str):
        try:
            display_title = str.replace('_', ' ').title()
        except Exception as e:
            display_title = str

        return display_title
