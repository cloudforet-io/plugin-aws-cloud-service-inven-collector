from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_acm_connector.schema.data import Certificate
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Certificate
'''
# TAB - Status
acm_meta_status = ItemDynamicLayout.set_fields('Status', fields=[
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['ISSUED'],
        'warning': ['PENDING_VALIDATION', 'INACTIVE', 'VALIDATION_TIMED_OUT', 'REVOKED'],
        'alert': ['EXPIRED', 'FAILED']
    }),
    DateTimeDyField.data_source('Issue Date', 'data.issued_at'),
])

acm_meta_domain_validation_table = \
    TableDynamicLayout.set_fields('Domain Validation Status','data.domain_validation_options',
                                  fields=[
                                      TextDyField.data_source('Domain', 'domain_name'),
                                      EnumDyField.data_source('Validation status', 'validation_status',
                                                              default_state={
                                                                  'safe': ['SUCCESS'],
                                                                  'warning': ['PENDING_VALIDATION'],
                                                                  'alert': ['FAILED']}),
                                  ])

certificate_status = ListDynamicLayout.set_layouts('Status', layouts=[acm_meta_status, acm_meta_domain_validation_table])


# TAB - Detail
acm_meta_detail = ItemDynamicLayout.set_fields('Details', fields=[
    TextDyField.data_source('Type', 'data.type'),
    TextDyField.data_source('In use?', 'data.in_use_display'),
    TextDyField.data_source('Domain Name', 'data.domain_name'),
    ListDyField.data_source('Additional names', 'data.additional_names_display', options={
        'delimiter': '<br>'
    }),
    TextDyField.data_source('Identifier', 'data.identifier'),
    TextDyField.data_source('Serial Number', 'data.serial'),
    ListDyField.data_source('Associated Resource', 'data.in_use_by', options={
        'delimiter': '<br>'
    }),
    DateTimeDyField.data_source('Requested At', 'data.created_at'),
    DateTimeDyField.data_source('Issued At', 'data.issued_at'),
    DateTimeDyField.data_source('Not Before', 'data.not_before'),
    DateTimeDyField.data_source('Not After', 'data.not_after'),
    TextDyField.data_source('Public Key Info', 'data.key_algorithm'),
    TextDyField.data_source('Signature Algorithm', 'data.signature_algorithm'),
    TextDyField.data_source('ARN', 'data.certificate_arn')
])

acm_meta = CloudServiceMeta.set_layouts([certificate_status, acm_meta_detail])


class ACMResource(CloudServiceResource):
    cloud_service_group = StringType(default='CertificateManager')


class CertificateResource(ACMResource):
    cloud_service_type = StringType(default='Certificate')
    data = ModelType(Certificate)
    _metadata = ModelType(CloudServiceMeta, default=acm_meta, serialized_name='metadata')


class ACMResponse(CloudServiceResponse):
    resource = PolyModelType(CertificateResource)
