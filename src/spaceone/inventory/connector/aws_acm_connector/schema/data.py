import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, FloatType, DateTimeType, serializable, ListType, \
    BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from='Key')
    value = StringType(deserialize_from='Value')


class ResourceRecord(Model):
    name = StringType(deserialize_from="Name")
    type = StringType(deserialize_from="Type")
    value = StringType(deserialize_from="Value")


class DomainValidationOptions(Model):
    domain_name = StringType(deserialize_from="DomainName")
    validation_emails = ListType(StringType, deserialize_from="ValidationEmails")
    validation_domain = StringType(deserialize_from="ValidationDomain")
    validation_status = StringType(deserialize_from="ValidationStatus",
                                   choices=('PENDING_VALIDATION','SUCCESS','FAILED'))
    resource_record = ModelType(ResourceRecord, deserialize_from="ResourceRecord")
    validation_method = StringType(deserialize_from="ValidationMethod", choices=('EMAIL', 'DNS'))


class RenewalSummary(Model):
    renewal_status = StringType(deserialize_from="RenewalStatus",
                                choices=('PENDING_AUTO_RENEWAL','PENDING_VALIDATION','SUCCESS','FAILED'))
    domain_validation_options = ListType(ModelType(DomainValidationOptions), deserialize_from="DomainValidationOptions")
    renewal_status_reason = StringType(deserialize_from="RenewalStatusReason",
                                       choices=('NO_AVAILABLE_CONTACTS', 'ADDITIONAL_VERIFICATION_REQUIRED',
                                                'DOMAIN_NOT_ALLOWED', 'INVALID_PUBLIC_DOMAIN', 'DOMAIN_VALIDATION_DENIED',
                                                'CAA_ERROR', 'PCA_LIMIT_EXCEEDED', 'PCA_INVALID_ARN', 'PCA_INVALID_STATE',
                                                'PCA_REQUEST_FAILED', 'PCA_NAME_CONSTRAINTS_VALIDATION',
                                                'PCA_RESOURCE_NOT_FOUND', 'PCA_INVALID_ARGS', 'PCA_INVALID_DURATION',
                                                'PCA_ACCESS_DENIED', 'SLR_NOT_FOUND', 'OTHER'))
    updated_at = DateTimeType(deserialize_from="UpdatedAt")


class ExtendedKeyUsagesName(Model):
    name = StringType(deserialize_from="Name",
                      choices=('TLS_WEB_SERVER_AUTHENTICATION', 'TLS_WEB_CLIENT_AUTHENTICATION', 'CODE_SIGNING',
                               'EMAIL_PROTECTION', 'TIME_STAMPING', 'OCSP_SIGNING', 'IPSEC_END_SYSTEM',
                               'IPSEC_TUNNEL', 'IPSEC_USER', 'ANY', 'NONE', 'CUSTOM'))
    oid = StringType(deserialize_from="OID")


class KeyUsagesName(Model):
    name = StringType(deserialize_from="Name",
                      choices=('DIGITAL_SIGNATURE', 'NON_REPUDIATION', 'KEY_ENCIPHERMENT', 'DATA_ENCIPHERMENT',
                                'KEY_AGREEMENT', 'CERTIFICATE_SIGNING', 'CRL_SIGNING', 'ENCIPHER_ONLY',
                               'DECIPHER_ONLY', 'ANY', 'CUSTOM'))


class Options(Model):
    certificate_transparency_logging_preference = StringType(deserialize_from="CertificateTransparencyLoggingPreference",
                                                             choices=('ENABLED', 'DISABLED'))


class Certificate(Model):
    certificate_arn = StringType(deserialize_from="CertificateArn")
    identifier = StringType()
    domain_name = StringType(deserialize_from="DomainName")
    subject_alternative_names = ListType(StringType, deserialize_from="SubjectAlternativeNames")
    additional_names_display = ListType(StringType)
    domain_validation_options = ListType(ModelType(DomainValidationOptions), deserialize_from="DomainValidationOptions")
    serial = StringType(deserialize_from="Serial")
    subject = StringType(deserialize_from="Subject")
    issuer = StringType(deserialize_from="Issuer")
    created_at = DateTimeType(deserialize_from="CreatedAt")
    issued_at = DateTimeType(deserialize_from="IssuedAt")
    imported_at = DateTimeType(deserialize_from="ImportedAt")
    status = StringType(deserialize_from="Status",
                        choices=('PENDING_VALIDATION', 'ISSUED', 'INACTIVE', 'EXPIRED', 'VALIDATION_TIMED_OUT',
                                 'REVOKED', 'FAILED'))
    revoked_at = DateTimeType(deserialize_from="RevokedAt")
    revocation_reason = StringType(deserialize_from="RevocationReason",
                                   choices=('UNSPECIFIED', 'KEY_COMPROMISE', 'CA_COMPROMISE', 'AFFILIATION_CHANGED',
                                            'SUPERCEDED', 'CESSATION_OF_OPERATION', 'CERTIFICATE_HOLD',
                                            'REMOVE_FROM_CRL', 'PRIVILEGE_WITHDRAWN', 'A_A_COMPROMISE'))
    not_before = DateTimeType(deserialize_from="NotBefore")
    not_after = DateTimeType(deserialize_from="NotAfter")
    key_algorithm = StringType(deserialize_from="KeyAlgorithm",
                               choices=('RSA_2048', 'RSA_1024', 'RSA_4096', 'EC_prime256v1', 'EC_secp384r1',
                                        'EC_secp521r1'))
    signature_algorithm = StringType(deserialize_from="SignatureAlgorithm")
    in_use_by = ListType(StringType, deserialize_from="InUseBy")
    in_use_display = StringType(choices=('Yes', 'No'))
    failure_reason = StringType(deserialize_from="FailureReason",
                                choices=('NO_AVAILABLE_CONTACTS', 'ADDITIONAL_VERIFICATION_REQUIRED',
                                         'DOMAIN_NOT_ALLOWED', 'INVALID_PUBLIC_DOMAIN', 'DOMAIN_VALIDATION_DENIED',
                                         'CAA_ERROR', 'PCA_LIMIT_EXCEEDED', 'PCA_INVALID_ARN', 'PCA_INVALID_STATE',
                                         'PCA_REQUEST_FAILED', 'PCA_NAME_CONSTRAINTS_VALIDATION',
                                         'PCA_RESOURCE_NOT_FOUND', 'PCA_INVALID_ARGS', 'PCA_INVALID_DURATION',
                                         'PCA_ACCESS_DENIED', 'SLR_NOT_FOUND', 'OTHER'))
    type = StringType(deserialize_from="Type", choices=('IMPORTED', 'AMAZON_ISSUED', 'PRIVATE'))
    renewal_summary = ModelType(RenewalSummary, deserialize_from="RenewalSummary")
    key_usages = ListType(ModelType(KeyUsagesName), deserialize_from="KeyUsages")
    extended_key_usages = ListType(ModelType(ExtendedKeyUsagesName), deserialize_from="ExtendedKeyUsages")
    certificate_authority_arn = StringType(deserialize_from="CertificateAuthorityArn")
    renewal_eligibility = StringType(deserialize_from="RenewalEligibility", choices=("ELIGIBLE", "INELIGIBLE"))
    options = ModelType(Options, deserialize_from="Options")
    tags = ListType(ModelType(Tags), default=[])
    account_id = StringType(default='')


    def reference(self, region_code):
        return {
            "resource_id": self.certificate_arn,
            "external_link": f"https://console.aws.amazon.com/acm/home?region={region_code}#/?id={self.identifier}"
        }
