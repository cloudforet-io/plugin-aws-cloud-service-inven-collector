import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel


_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


# OK
class CustomHeadersItems(Model):
    header_name = StringType(deserialize_from="HeaderName")
    header_value = StringType(deserialize_from="HeaderValue")


# OK
class CustomHeaders(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(CustomHeadersItems), deserialize_from="Items", serialize_when_none=False)


# OK
class S3OriginConfig(Model):
    origin_access_identity = StringType(deserialize_from="OriginAccessIdentity", serialize_when_none=False)


# OK
class OriginSslProtocols(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items", choices=('SSLv3', 'TLSv1', 'TLSv1.1', 'TLSv1.2'))


# OK
class CustomOriginConfig(Model):
    http_port = IntType(deserialize_from="HTTPPort", serialize_when_none=False)
    https_port = IntType(deserialize_from="HTTPSPort", serialize_when_none=False)
    origin_protocol_policy = StringType(deserialize_from="OriginProtocolPolicy",
                                        choices=("http-only", "match-viewer", "https-only"))
    origin_ssl_protocols = ModelType(OriginSslProtocols, deserialize_from="OriginSslProtocols",
                                     serialize_when_none=False)
    origin_read_timeout = IntType(deserialize_from="OriginReadTimeout", serialize_when_none=False)
    origin_keepalive_timeout = IntType(deserialize_from="OriginKeepaliveTimeout", serialize_when_none=False)


# OK
class OriginShield(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    origin_shield_region = StringType(deserialize_from="OriginShieldRegion", serialize_when_none=False)


# OK
class OriginsItems(Model):
    id = StringType(deserialize_from="Id")
    domain_name = StringType(deserialize_from="DomainName", serialize_when_none=False)
    origin_path = StringType(deserialize_from="OriginPath", serialize_when_none=False)
    custom_headers = ModelType(CustomHeaders, deserialize_from="CustomHeaders", serialize_when_none=False)
    s3_origin_config = ModelType(S3OriginConfig, deserialize_from="S3OriginConfig", serialize_when_none=False)
    custom_origin_config = ModelType(CustomOriginConfig, deserialize_from="CustomOriginConfig",
                                     serialize_when_none=False)
    connection_attempts = IntType(deserialize_from="ConnectionAttempts", serialize_when_none=False)
    connection_timeout = IntType(deserialize_from="ConnectionTimeout", serialize_when_none=False)
    origin_shield = ModelType(OriginShield, deserialize_from="OriginShield", serialize_when_none=False)


# OK
class Origins(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(OriginsItems), deserialize_from="Items", serialize_when_none=False)


# OK
class StatusCodes(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(IntType, deserialize_from="Items", serialize_when_none=False)


# OK
class FailoverCriteria(Model):
    status_codes = ModelType(StatusCodes, deserialize_from="StatusCodes", serialize_when_none=False)


# OK
class MembersItems(Model):
    origin_id = StringType(deserialize_from="OriginId", serialize_when_none=False)


# OK
class Members(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(MembersItems), deserialize_from="Items", serialize_when_none=False)


# OK
class OriginGroupsItems(Model):
    id = StringType(deserialize_from="Id")
    failover_criteria = ModelType(FailoverCriteria, deserialize_from="FailoverCriteria", serialize_when_none=False)
    members = ModelType(Members, deserialize_from="Members", serialize_when_none=False)


# OK
class OriginGroups(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(OriginGroupsItems), deserialize_from="Items", serialize_when_none=False)


# OK
class WhitelistedNames(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class Cookies(Model):
    forward = StringType(deserialize_from="Forward", choices=("none", "whitelist", "all"))
    whitelisted_names = ModelType(WhitelistedNames, deserialize_from="WhitelistedNames", serialize_when_none=False)


# OK
class Headers(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class QueryStringCacheKeys(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class ForwardedValues(Model):
    query_string = BooleanType(deserialize_from="QueryString", serialize_when_none=False)
    cookies = ModelType(Cookies, deserialize_from="Cookies", serialize_when_none=False)
    headers = ModelType(Headers, deserialize_from="Headers", serialize_when_none=False)
    query_string_cache_keys = ModelType(QueryStringCacheKeys, deserialize_from="QueryStringCacheKeys",
                                        serialize_when_none=False)


# OK
class TrustedSigners(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    quantity = IntType(deserialize_from="Quantity", serialize_when_none=False)
    items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class TrustedKeyGroups(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    quantity = IntType(deserialize_from="Quantity", serialize_when_none=False)
    items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class CachedMethods(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items",
                     choices=('GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'))


# OK
class AllowedMethods(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items",
                     choices=('GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'))
    cached_methods = ModelType(CachedMethods, deserialize_from="CachedMethods", serialize_when_none=False)


# OK
class LambdaFunctionAssociationsItems(Model):
    lambda_function_arn = StringType(deserialize_from="LambdaFunctionARN", serialize_when_none=False)
    event_type = StringType(deserialize_from="EventType",
                            choices=("viewer-request", "viewer-response", "origin-request", "origin-response"))
    include_body = BooleanType(deserialize_from="IncludeBody", serialize_when_none=False)


# OK
class LambdaFunctionAssociations(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(LambdaFunctionAssociationsItems), deserialize_from="Items", serialize_when_none=False)


# OK
class DefaultCacheBehavior(Model):
    target_origin_id = StringType(deserialize_from="TargetOriginId", serialize_when_none=False)
    trusted_signers = ModelType(TrustedSigners, deserialize_from="TrustedSigners", serialize_when_none=False)
    trusted_key_groups = ModelType(TrustedKeyGroups, deserialize_from="TrustedKeyGroups", serialize_when_none=False)
    viewer_protocol_policy = StringType(deserialize_from="ViewerProtocolPolicy",
                                        choices=("allow-all", "https-only", "redirect-to-https"))
    allowed_methods = ModelType(AllowedMethods, deserialize_from="AllowedMethods", serialize_when_none=False)
    smooth_streaming = BooleanType(deserialize_from="SmoothStreaming", serialize_when_none=False)
    compress = BooleanType(deserialize_from="Compress", serialize_when_none=False)
    lambda_function_associations = ModelType(LambdaFunctionAssociations, deserialize_from="LambdaFunctionAssociations",
                                             serialize_when_none=False)
    field_level_encryption_id = StringType(deserialize_from="FieldLevelEncryptionId", serialize_when_none=False)
    realtime_log_config_arn = StringType(deserialize_from="RealtimeLogConfigArn", serialize_when_none=False)
    cache_policy_id = StringType(deserialize_from="CachePolicyId", serialize_when_none=False)
    origin_request_policy_id = StringType(deserialize_from="OriginRequestPolicyId", serialize_when_none=False)
    forwarded_values = ModelType(ForwardedValues, deserialize_from="ForwardedValues", serialize_when_none=False)
    min_ttl = IntType(deserialize_from="MinTTL", serialize_when_none=False)
    default_ttl = IntType(deserialize_from="DefaultTTL", serialize_when_none=False)
    max_ttl = IntType(deserialize_from="MaxTTL", serialize_when_none=False)


# OK
class CacheBehaviorsItems(Model):
    path_pattern = StringType(deserialize_from="PathPattern", serialize_when_none=False)
    target_origin_id = StringType(deserialize_from="TargetOriginId", serialize_when_none=False)
    trusted_signers = ModelType(TrustedSigners, deserialize_from="TrustedSigners", serialize_when_none=False)
    trusted_key_groups = ModelType(TrustedKeyGroups, deserialize_from="TrustedKeyGroups", serialize_when_none=False)
    viewer_protocol_policy = StringType(deserialize_from="ViewerProtocolPolicy",
                                        choices=("allow-all", "https-only", "redirect-to-https"))
    allowed_methods = ModelType(AllowedMethods, deserialize_from="AllowedMethods", serialize_when_none=False)
    smooth_streaming = BooleanType(deserialize_from="SmoothStreaming", serialize_when_none=False)
    compress = BooleanType(deserialize_from="Compress", serialize_when_none=False)
    lambda_function_associations = ModelType(LambdaFunctionAssociations, deserialize_from="LambdaFunctionAssociations",
                                             serialize_when_none=False)
    field_level_encryption_id = StringType(deserialize_from="FieldLevelEncryptionId", serialize_when_none=False)
    realtime_log_config_arn = StringType(deserialize_from="RealtimeLogConfigArn", serialize_when_none=False)
    cache_policy_id = StringType(deserialize_from="CachePolicyId", serialize_when_none=False)
    origin_request_policy_id = StringType(deserialize_from="OriginRequestPolicyId", serialize_when_none=False)
    forwarded_values = ModelType(ForwardedValues, deserialize_from="ForwardedValues", serialize_when_none=False)
    min_ttl = IntType(deserialize_from="MinTTL", serialize_when_none=False)
    default_ttl = IntType(deserialize_from="DefaultTTL", serialize_when_none=False)
    max_ttl = IntType(deserialize_from="MaxTTL", serialize_when_none=False)


# OK
class CacheBehaviors(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(CacheBehaviorsItems), deserialize_from="Items", serialize_when_none=False)


# OK
class CustomErrorResponsesItems(Model):
    error_code = IntType(deserialize_from="ErrorCode", serialize_when_none=False)
    response_page_path = StringType(deserialize_from="ResponsePagePath", serialize_when_none=False)
    response_code = StringType(deserialize_from="ResponseCode", serialize_when_none=False)
    error_caching_min_ttl = IntType(deserialize_from="ErrorCachingMinTTL", serialize_when_none=False)


# OK
class CustomErrorResponses(Model):
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(ModelType(CustomErrorResponsesItems), deserialize_from="Items", serialize_when_none=False)


# OK
class GeoRestriction(Model):
    restriction_type = StringType(deserialize_from="RestrictionType", choices=("blacklist", "whitelist", "none"))
    quantity = IntType(deserialize_from="Quantity")
    items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class Restrictions(Model):
    geo_restriction = ModelType(GeoRestriction, deserialize_from="GeoRestriction", serialize_when_none=False)


# OK
class AliasICPRecordals(Model):
    cname = StringType(deserialize_from="CNAME", serialize_when_none=False)
    icp_recordal_status = StringType(deserialize_from="ICPRecordalStatus", choices=("APPROVED", "SUSPENDED", "PENDING"))

# OK
class Alias(Model):
    quantity = IntType(deserialize_from="Quantity")
    Items = ListType(StringType, deserialize_from="Items", serialize_when_none=False)


# OK
class ViewerCertificate(Model):
    cloud_front_default_certificate = BooleanType(deserialize_from="CloudFrontDefaultCertificate",
                                                  serialize_when_none=False)
    iam_certificate_id = StringType(deserialize_from="IAMCertificateId",
                                    serialize_when_none=False)
    acm_certificate_arn = StringType(deserialize_from="ACMCertificateArn",
                                     serialize_when_none=False)
    ssl_support_method = StringType(deserialize_from="SSLSupportMethod", choices=('sni-only', 'vip', 'static-ip'))
    minimum_protocol_version = StringType(deserialize_from="MinimumProtocolVersion",
                                          choices=('SSLv3', 'TLSv1', 'TLSv1_2016', 'TLSv1.1_2016', 'TLSv1.2_2018',
                                                   'TLSv1.2_2019'))
    certificate = StringType(deserialize_from="Certificate", serialize_when_none=False)
    certificate_source = StringType(deserialize_from="CertificateSource", choices=('cloudfront', 'iam', 'acm'))


class DistributionData(Model):
    id = StringType(deserialize_from="Id")
    arn = StringType(deserialize_from="ARN")
    status = StringType(deserialize_from="Status")
    last_modified_time = DateTimeType(deserialize_from="LastModifiedTime")
    domain_name = StringType(deserialize_from="DomainName", serialize_when_none=False)
    aliases = ModelType(Alias, deserialize_from="Aliases", serialize_when_none=False)
    origins = ModelType(Origins, deserialize_from="Origins", serialize_when_none=False)
    origin_groups = ModelType(OriginGroups, deserialize_from="OriginGroups", serialize_when_none=False)
    default_cache_behavior = ModelType(DefaultCacheBehavior, deserialize_from="DefaultCacheBehavior",
                                       serialize_when_none=False)
    cache_behavior = ModelType(CacheBehaviors, deserialize_from="CacheBehaviors", serialize_when_none=False)
    custom_error_responses = ModelType(CustomErrorResponses, deserialize_from="CustomErrorResponses",
                                       serialize_when_none=False)
    comment = StringType(deserialize_from="Comment", serialize_when_none=False)
    price_class = StringType(deserialize_from="PriceClass",
                             choices=("PriceClass_100", "PriceClass_200", "PriceClass_All"))
    enabled = BooleanType(deserialize_from="Enabled", serialize_when_none=False)
    viewer_certificate = ModelType(ViewerCertificate, deserialize_from="ViewerCertificate", serialize_when_none=False)
    restrictions = ModelType(Restrictions, deserialize_from="Restrictions", serialize_when_none=False)
    web_acl_id = StringType(deserialize_from="WebACLId", serialize_when_none=False)
    http_version = StringType(deserialize_from="HttpVersion", choices=("http1.1", "http2"))
    is_ipv6_enabled = BooleanType(deserialize_from="IsIPV6Enabled", serialize_when_none=False)
    alias_icp_recordals = ListType(ModelType(AliasICPRecordals), deserialize_from="AliasICPRecordals",
                                   serialize_when_none=False)
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
