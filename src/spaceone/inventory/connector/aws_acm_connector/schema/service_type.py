import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')

cst_certi = CloudServiceTypeResource()
cst_certi.name = 'Certificate'
cst_certi.provider = 'aws'
cst_certi.group = 'CertificateManager'
cst_certi.labels = ['Security']
cst_certi.is_primary = True
cst_certi.service_code = 'AWSCertificateManager'
cst_certi.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Certificate-Manager.svg',
}

cst_certi._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        ListDyField.data_source('Additional Names', 'data.additional_names_display', options={
            "delimiter": "<br>"
        }),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['ISSUED'],
            'warning': ['PENDING_VALIDATION', 'INACTIVE', 'VALIDATION_TIMED_OUT', 'REVOKED'],
            'alert': ['EXPIRED', 'FAILED']
        }),
        TextDyField.data_source('Type', 'instance_type'),
        TextDyField.data_source('In use?', 'data.in_use_display'),
        TextDyField.data_source('Renewal Eligibility', 'data.renewal_eligibility_display'),
        # For Dynamic Table
        TextDyField.data_source('Identifier', 'data.identifier', options={
            'is_optional': True
        }),
        TextDyField.data_source('Issuer', 'data.issuer', options={
            'is_optional': True
        }),
        TextDyField.data_source('Certificate ARN', 'data.certificate_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Subject', 'data.subject', options={
            'is_optional': True
        }),
        TextDyField.data_source('Serial', 'data.serial', options={
            'is_optional': True
        }),
        TextDyField.data_source('Signature Algorithm', 'data.signature_algorithm', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Algorithm', 'data.key_algorithm', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.certificate_arn'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='In use?', key='data.in_use_display'),
        SearchField.set(name='Renewal Eligibility', key='data.renewal_eligibility'),
        SearchField.set(name='Associated Resources', key='data.in_use_by'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_certi}),
]
