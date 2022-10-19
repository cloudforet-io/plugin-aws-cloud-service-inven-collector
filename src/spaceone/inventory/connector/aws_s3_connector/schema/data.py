import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, FloatType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)

TOPIC_EVENTS = ("s3:ReducedRedundancyLostObject", "s3:ObjectCreated:*", "s3:ObjectCreated:Put", "s3:ObjectCreated:Post",
                "s3:ObjectCreated:Copy", "s3:ObjectCreated:CompleteMultipartUpload", "s3:ObjectRemoved:*",
                "s3:ObjectRemoved:Delete", "s3:ObjectRemoved:DeleteMarkerCreated", "s3:ObjectRestore:*",
                "s3:ObjectRestore:Post", "s3:ObjectRestore:Completed", "s3:Replication:*",
                "s3:Replication:OperationFailedReplication", "s3:Replication:OperationNotTracked",
                "s3:Replication:OperationMissedThreshold", "s3:Replication:OperationReplicatedAfterThreshold")

'''
TOPIC NOTIFICATION
'''
class KeyFilterRules(Model):
    name = StringType(deserialize_from="Name", choices=("prefix", "suffix"))
    value = StringType(deserialize_from="Value")


class NotificationFilterKey(Model):
    filter_rules = ListType(ModelType(KeyFilterRules), deserialize_from="FilterRules")


class NotificationFilter(Model):
    key = ModelType(NotificationFilterKey, deserialize_from="Key")


class NotificationConfiguration(Model):
    id = StringType(deserialize_from="Id")
    notification_type = StringType(choices=("SNS Topic", "Queue", "Lambda Function"))
    arn = StringType()
    events = ListType(StringType, choices=TOPIC_EVENTS)
    filter = ModelType(NotificationFilter, deserialize_from="filter")

'''
REQUEST PAYMENT
'''
class RequestPayment(Model):
    request_payment = StringType(choices=("Requester", "BucketOwner"))


'''
TRANSFER ACCELERATION
'''
class TransferAcceleration(Model):
    transfer_acceleration = StringType(choices=("Enabled", "Suspended"))


'''
OBJECT LOCK
'''
class DefaultRetention(Model):
    mode = StringType(deserialize_from="Mode", choices=("GOVERNANCE", "COMPLIANCE"))
    days = IntType(deserialize_from="Days")
    years = IntType(deserialize_from="Years")


class ObjectLockRule(Model):
    default_retention = ModelType(DefaultRetention, deserialize_from="DefaultRetention")


class ObjectLock(Model):
    object_lock_enabled = StringType(deserialize_from="ObjectLockEnabled", choices=("Enabled", "Disabled"))
    rule = ModelType(ObjectLockRule, deserialize_from="Rule")


'''
ENCRYPTION
'''
class ApplyServerSideEncryptionByDefault(Model):
    sse_algorithm = StringType(deserialize_from="SSEAlgorithm", choices=("AES256", "aws:kms"))
    kms_master_key_id = StringType(deserialize_from="KMSMasterKeyID")


class EncryptionRules(Model):
    apply_server_side_encryption_by_default = ModelType(ApplyServerSideEncryptionByDefault,
                                                        deserialize_from="ApplyServerSideEncryptionByDefault")


class Encryption(Model):
    rules = ListType(ModelType(EncryptionRules), deserialize_from="Rules")


'''
WEBSITE HOSTING
'''
class RedirectAllRequestsTo(Model):
    host_name = StringType(deserialize_from="HostName")
    protocol = StringType(deserialize_from="Protocol", choices=("http", "https"))


class IndexDocument(Model):
    suffix = StringType(deserialize_from="Suffix")


class ErrorDocument(Model):
    key = StringType(deserialize_from="Key")


class Condition(Model):
    http_error_code_returned_equals = StringType(deserialize_from="HttpErrorCodeReturnedEquals")
    key_prefix_equals = StringType(deserialize_from="KeyPrefixEquals")


class Redirect(Model):
    host_name = StringType(deserialize_from="HostName")
    http_redirect_code = StringType(deserialize_from="HttpRedirectCode")
    protocol = StringType(deserialize_from="Protocol", choices=("http", "https"))
    replace_key_prefix_with = StringType(deserialize_from="ReplaceKeyPrefixWith")
    replace_key_with = StringType(deserialize_from="ReplaceKeyWith")


class WebsiteHostingRoutingRules(Model):
    condition = ModelType(Condition, deserialize_from="Condition")
    redirect = ModelType(Redirect, deserialize_from="Redirect")


class WebsiteHosting(Model):
    redirect_all_requests_to = ModelType(RedirectAllRequestsTo, deserialize_from="RedirectAllRequestsTo")
    index_document = ModelType(IndexDocument, deserialize_from="IndexDocument")
    error_document = ModelType(ErrorDocument, deserialize_from="ErrorDocument")
    routing_rules = ListType(ModelType(WebsiteHostingRoutingRules), deserialize_from="RoutingRules")


'''
LOGGING
'''
class Grantee(Model):
    display_name = StringType(deserialize_from="DisplayName")
    email_address = StringType(deserialize_from="EmailAddress")
    id = StringType(deserialize_from="ID")
    type = StringType(deserialize_from="Type", choices=("CanonicalUser", "AmazonCustomerByEmail", "Group"))
    uri = StringType(deserialize_from="URI")


class LoggingEnabledTargetGrants(Model):
    grantee = ModelType(Grantee,deserialize_from="Grantee")
    permission = StringType(deserialize_from="Permission", choices=("FULL_CONTROL", "READ", "WRITE"))


class ServerAccessLogging(Model):
    target_bucket = StringType(deserialize_from="TargetBucket")
    target_grants = ListType(ModelType(LoggingEnabledTargetGrants), deserialize_from="TargetGrants")
    target_prefix = StringType(deserialize_from="TargetPrefix")


'''
VERSIONING
'''
class Versioning(Model):
    status = StringType(deserialize_from="Status", choices=("Enabled", "Disabled"))
    mfa_delete = StringType(deserialize_from="MFADelete", choices=("Enabled", "Disabled"), serialize_when_none=False)


class Bucket(AWSCloudService):
    arn = StringType(default="")
    name = StringType(deserialize_from="Name")
    public_access = StringType(choices=("Public", "Private"))
    versioning = ModelType(Versioning, serialize_when_none=False)
    server_access_logging = ModelType(ServerAccessLogging, serialize_when_none=False)
    website_hosting = ModelType(WebsiteHosting, serialize_when_none=False)
    encryption = ModelType(Encryption, serialize_when_none=False)
    object_lock = ModelType(ObjectLock, serialize_when_none=False)
    transfer_acceleration = ModelType(TransferAcceleration, serialize_when_none=False)
    request_payment = ModelType(RequestPayment, serialize_when_none=False)
    notification_configurations = ListType(ModelType(NotificationConfiguration), default=[])
    region_name = StringType(default="")
    object_count = IntType(default=0)
    object_total_size = FloatType(default=0.0)
    size = FloatType(default=0.0)

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/s3/buckets/{self.name}/?region={self.region_name}"
        }
