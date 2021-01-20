import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel


_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class KeyPairIds(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class ActiveTrustedKeyGroupItems(Model):
    key_group_id = StringType(deserialize_from="KeyGroupId")
    key_pair_ids = ModelType(KeyPairIds, deserialize_from="KeyPairIds")


class ActiveTrustedSignersItems(Model):
    aws_account_number = StringType(deserialize_from="AwsAccountNumber")
    key_pair_ids = ModelType(KeyPairIds, deserialize_from="KeyPairIds")


class ActiveTrustedSigners(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(ActiveTrustedSignersItems), deserialize_from="Items")


class ActiveTrustedKeyGroups(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(ActiveTrustedKeyGroupItems), deserialize_from="Items")


class Aliases(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class CustomHeadersItems(Model):
    header_name = StringType(deserialize_from="HeaderName")
    header_value = StringType(deserialize_from="HeaderValue")


class CustomHeaders(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(CustomHeadersItems), deserialize_from="Items")


class S3OriginConfig(Model):
    origin_access_identity = StringType(deserialize_from="OriginAccessIdentity")


class OriginSslProtocols(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class CustomOriginConfig(Model):
    http_port = IntType(deserialize_from="HTTPPort")
    https_port = IntType(deserialize_from="HTTPSPort")
    origin_protocol_policy = StringType(deserialize_from="OriginProtocolPolicy",
                                        choices=("http-only", "match-viewer", "https-only"))
    origin_ssl_protocols = ModelType(OriginSslProtocols, deserialize_from="OriginSslProtocols")
    origin_read_timeout = IntType(deserialize_from="OriginReadTimeout")
    origin_keepalive_timeout = IntType(deserialize_from="OriginKeepaliveTimeout")


class OriginShield(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    origin_shield_region = StringType(deserialize_from="OriginShieldRegion")


class OriginsItems(Model):
    id = StringType(deserialize_from="Id")
    domain_name = StringType(deserialize_from="DomainName")
    origin_path = StringType(deserialize_from="OriginPath")
    custom_headers = ModelType(CustomHeaders, deserialize_from="CustomHeaders")
    s3_origin_config = ModelType(S3OriginConfig, deserialize_from="S3OriginConfig")
    custom_origin_config = ModelType(CustomOriginConfig, deserialize_from="CustomOriginConfig")
    connection_attempts = IntType(deserialize_from="ConnectionAttempts")
    connection_timeout = IntType(deserialize_from="ConnectionTimeout")
    origin_shield = ModelType(OriginShield, deserialize_from="OriginShield")


class Origins(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(OriginsItems), deserialize_from="Items")


class StatusCodes(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(IntType, deserialize_from="Items")


class FailoverCriteria(Model):
    status_codes = ModelType(StatusCodes, deserialize_from="StatusCodes")


class MembersItems(Model):
    origin_id = StringType(deserialize_from="OriginId")


class Members(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(MembersItems), deserialize_from="Items")


class OriginGroupsItems(Model):
    id = StringType(deserialize_from="Id")
    failover_criteria = ModelType(FailoverCriteria, deserialize_from="FailoverCriteria")
    members = ModelType(Members, deserialize_from="Members")


class OriginGroups(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(OriginGroupsItems), deserialize_from="Items")


class WhitelistedNames(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class Cookies(Model):
    forward = StringType(deserialize_from="Forward", choices=("none", "whitelist", "all"))
    whitelisted_names = ModelType(WhitelistedNames, deserialize_from="WhitelistedNames")


class Headers(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class QueryStringCacheKeys(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class ForwardedValues(Model):
    query_string = BooleanType(deserialize_from="QueryString")
    cookies = ModelType(Cookies, deserialize_from="Cookies")
    headers = ModelType(Headers, deserialize_from="Headers")
    query_string_cache_keys = ModelType(QueryStringCacheKeys, deserialize_from="QueryStringCacheKeys")


class TrustedSigners(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class TrustedKeyGroups(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class CachedMethods(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class AllowedMethods(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")
    cached_methods = ModelType(CachedMethods, deserialize_from="CachedMethods")


class LambdaFunctionAssociationsItems(Model):
    lambda_function_arn = StringType(deserialize_from="LambdaFunctionARN")
    event_type = StringType(deserialize_from="EventType",
                            choices=("viewer-request", "viewer-response", "origin-request", "origin-response"))
    include_body = BooleanType(deserialize_from="IncludeBody")


class LambdaFunctionAssociations(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(LambdaFunctionAssociationsItems), deserialize_from="Items")


class DefaultCacheBehavior(Model):
    target_origin_id = StringType(deserialize_from="TargetOriginId")
    trusted_signers = ModelType(TrustedSigners, deserialize_from="TrustedSigners")
    trusted_key_groups = ModelType(TrustedKeyGroups, deserialize_from="TrustedKeyGroups")
    viewer_protocol_policy = StringType(deserialize_from="ViewerProtocolPolicy",
                                        choices=("allow-all", "https-only", "redirect-to-https"))
    allowed_methods = ModelType(AllowedMethods, deserialize_from="AllowedMethods")
    smooth_streaming = BooleanType(deserialize_from="SmoothStreaming")
    compress = BooleanType(deserialize_from="Compress")
    lambda_function_associations = ModelType(LambdaFunctionAssociations, deserialize_from="LambdaFunctionAssociations")
    field_level_encryption_id = StringType(deserialize_from="FieldLevelEncryptionId")
    cache_policy_id = StringType(deserialize_from="CachePolicyId")
    origin_request_policy_id = StringType(deserialize_from="OriginRequestPolicyId")
    forwarded_values = ModelType(ForwardedValues, deserialize_from="ForwardedValues")
    min_ttl = IntType(deserialize_from="MinTTL")
    default_ttl = IntType(deserialize_from="DefaultTTL")
    max_ttl = IntType(deserialize_from="MaxTTL")


class CacheBehaviorsItems(Model):
    path_pattern = StringType(deserialize_from="PathPattern")
    target_origin_id = StringType(deserialize_from="TargetOriginId")
    forwarded_values = ModelType(ForwardedValues, deserialize_from="ForwardedValues")
    trusted_signers = ModelType(TrustedSigners, deserialize_from="TrustedSigners")
    viewer_protocol_policy = StringType(deserialize_from="ViewerProtocolPolicy",
                                        choices=("allow-all", "https-only", "redirect-to-https"))
    min_ttl = IntType(deserialize_from="MinTTL")
    allowed_methods = ModelType(AllowedMethods, deserialize_from="AllowedMethods")
    smooth_streaming = BooleanType(deserialize_from="SmoothStreaming")
    default_ttl = IntType(deserialize_from="DefaultTTL")
    max_ttl = IntType(deserialize_from="MaxTTL")
    compress = BooleanType(deserialize_from="Compress")
    lambda_function_associations = ModelType(LambdaFunctionAssociations, deserialize_from="LambdaFunctionAssociations")
    field_level_encryption_id = StringType(deserialize_from="FieldLevelEncryptionId")


class CacheBehaviors(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(CacheBehaviorsItems), deserialize_from="Items")


class CustomErrorResponsesItems(Model):
    error_code = IntType(deserialize_from="ErrorCode")
    response_page_path = StringType(deserialize_from="ResponsePagePath")
    response_code = StringType(deserialize_from="ResponseCode")
    error_caching_min_ttl = IntType(deserialize_from="ErrorCachingMinTTL")


class CustomErrorResponses(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(CustomErrorResponsesItems), deserialize_from="Items")


class Logging(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    include_cookies = BooleanType(deserialize_from="IncludeCookies")
    bucket = StringType(deserialize_from="Bucket")
    prefix = StringType(deserialize_from="Prefix")


class ViewerCertificate(Model):
    cloud_front_default_certificate = BooleanType(deserialize_from="CloudFrontDefaultCertificate")
    iam_certificate_id = StringType(deserialize_from="IAMCertificateId")
    acm_certificate_arn = StringType(deserialize_from="ACMCertificateArn")
    ssl_support_method = StringType(deserialize_from="SSLSupportMethod", choices=("sni-only", "vip"))
    minimum_protocol_version = StringType(deserialize_from="MinimumProtocolVersion",
                                          choices=("SSLv3", "TLSv1", "TLSv1_2016", "TLSv1.1_2016", "TLSv1.2_2018"))
    certificate = StringType(deserialize_from="Certificate")
    certificate_source = StringType(deserialize_from="CertificateSource", choices=("cloudfront", "iam", "acm"))


class GeoRestriction(Model):
    restriction_type = StringType(deserialize_from="RestrictionType", choices=("blacklist", "whitelist", "none"))
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class Restrictions(Model):
    geo_restriction = ModelType(GeoRestriction, deserialize_from="GeoRestriction")


class OriginCustomHeaderItem(Model):
    header_name = StringType(deserialize_from="HeaderName")
    header_value = StringType(deserialize_from="HeaderValue")


class OriginCustomHeader(Model):
    quantity = IntType(deserialize_from="Quantity")
    Items = ListType(StringType, deserialize_from="Items", default=[])


class DistributionConfig(Model):
    caller_reference = StringType(deserialize_from="CallerReference")
    aliases = ModelType(Aliases, deserialize_from="Aliases")
    default_root_object = StringType(deserialize_from="DefaultRootObject")
    origins = ModelType(Origins, deserialize_from="Origins")
    origin_groups = ModelType(OriginGroups, deserialize_from="OriginGroups")
    default_cache_behavior = ModelType(DefaultCacheBehavior, deserialize_from="DefaultCacheBehavior")
    cache_behaviors = ModelType(CacheBehaviors, deserialize_from="CacheBehaviors")
    custom_error_responses = ModelType(CustomErrorResponses, deserialize_from="CustomErrorResponses")
    comment = StringType(deserialize_from="Comment")
    logging = ModelType(Logging, deserialize_from="Logging")
    price_class = StringType(deserialize_from="PriceClass",
                             choices=("PriceClass_100", "PriceClass_200", "PriceClass_All"))
    enabled = BooleanType(deserialize_from="Enabled")
    viewer_certificate = ModelType(ViewerCertificate, deserialize_from="ViewerCertificate")
    restrictions = ModelType(Restrictions, deserialize_from="Restrictions")
    web_acl_id = StringType(deserialize_from="WebACLId")
    http_version = StringType(deserialize_from="HttpVersion", choices=("http1.1", "http2"))
    is_ipv6_enabled = BooleanType(deserialize_from="IsIPV6Enabled")


class OriginItem(Model):
    id = StringType(deserialize_from="Id")
    domain_name = StringType(deserialize_from="DomainName")
    origin_path = StringType(deserialize_from="OriginPath")
    custom_headers = ModelType(OriginCustomHeader, deserialize_from="CustomHeaders")


class AliasICPRecordals(Model):
    cname = StringType(deserialize_from="CNAME")
    icp_recordal_status = StringType(deserialize_from="ICPRecordalStatus", choices=("APPROVED", "SUSPENDED", "PENDING"))


class Aliases(Model):
    quantity = IntType(deserialize_from="Quantity")
    Items = ListType(StringType, deserialize_from="Items", default=[])


class OriginGroup(Model):
    quantity = IntType(deserialize_from="Quantity")
    Items = ListType(StringType, deserialize_from="Items", default=[])


class Origin(Model):
    quantity = IntType(deserialize_from="Quantity")
    Items = ListType(StringType, deserialize_from="Items", default=[])


class CustomErrorResponseItem(Model):
    error_code = IntType(deserialize_from="ErrorCode")
    response_page_path = StringType(deserialize_from="ResponsePagePath")
    response_code = StringType(deserialize_from="ResponseCode")
    error_caching_min_ttl = IntType(deserialize_from="ErrorCachingMinTTL")


class CustomErrorResponse(Model):
    quantity = IntType(deserialize_from="Quantity")
    Items = ListType(ModelType(CustomErrorResponseItem), deserialize_from="Items")


class ViewerCertificate(Model):
    cloud_front_default_certificate = BooleanType(deserialize_from="CloudFrontDefaultCertificate")
    iam_certificate_id = StringType(deserialize_from="IAMCertificateId")
    acm_certificate_arn = StringType(deserialize_from="ACMCertificateArn")
    ssl_support_method = StringType(deserialize_from="SSLSupportMethod", choices=('sni-only', 'vip', 'static-ip'))
    minimum_protocol_version = StringType(deserialize_from="MinimumProtocolVersion",
                                          choices=('SSLv3', 'TLSv1', 'TLSv1_2016', 'TLSv1.1_2016', 'TLSv1.2_2018',
                                                   'TLSv1.2_2019'))
    certificate = StringType(deserialize_from="Certificate")
    certificate_source = StringType(deserialize_from="CertificateSource", choices=('cloudfront', 'iam', 'acm'))


class GeoRestriction(Model):
    restriction_type = StringType(deserialize_from="RestrictionType", choices=('blacklist', 'whitelist', 'none'))
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items")


class Restriction(Model):
    geo_restriction = ModelType(GeoRestriction, deserialize_from="GeoRestriction")


class DistributionData(Model):
    id = StringType(deserialize_from="Id")
    arn = StringType(deserialize_from="ARN")
    status = StringType(deserialize_from="Status")
    last_modified_time = DateTimeType(deserialize_from="LastModifiedTime")
    in_progress_invalidation_batches = IntType(deserialize_from="InProgressInvalidationBatches")
    domain_name = StringType(deserialize_from="DomainName")
    active_trusted_signers = ModelType(ActiveTrustedSigners, deserialize_from="ActiveTrustedSigners")
    active_trusted_key_groups = ModelType(ActiveTrustedKeyGroups, deserialize_from="ActiveTrustedKeyGroups")
    distribution_config = ModelType(DistributionConfig, deserialize_from="DistributionConfig")
    alias_icp_recordals = ListType(ModelType(AliasICPRecordals), deserialize_from="AliasICPRecordals")
    account_id = StringType()
    tags = ListType(ModelType(Tags), default=[])
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/cloudfront/home?#distribution-settings:{self.id}"
        }

    def set_cloudwatch(self, region_code='us-east-1'):
        return {
            "namespace": "AWS/CloudFront",
            "dimensions": [CloudWatchDimensionModel({'Name': 'DistributionId', 'Value': self.id})],
            "region_name": region_code
        }
