from schematics.types import ModelType, StringType, PolyModelType
from spaceone.inventory.connector.aws_s3_connector.schema.data import Bucket
from spaceone.inventory.libs.schema.resource import (
    CloudServiceResource,
    CloudServiceResponse,
    CloudServiceMeta,
)
from spaceone.inventory.libs.schema.dynamic_field import (
    TextDyField,
    ListDyField,
    EnumDyField,
    SizeField,
    MoreField,
    DictDyField,
)
from spaceone.inventory.libs.schema.dynamic_layout import (
    ItemDynamicLayout,
    TableDynamicLayout,
    SimpleTableDynamicLayout,
)

bucket = ItemDynamicLayout.set_fields(
    "Buckets",
    fields=[
        TextDyField.data_source("Name", "data.name"),
        TextDyField.data_source("ARN", "data.arn"),
        TextDyField.data_source("Region", "data.region_name"),
        EnumDyField.data_source(
            "Public Access",
            "data.public_access",
            default_badge={"indigo.500": ["Private"], "coral.600": ["Public"]},
        ),
    ],
)

object_info = ItemDynamicLayout.set_fields(
    "Objects",
    fields=[
        TextDyField.data_source("Object Counts", "data.object_count"),
        SizeField.data_source("Object Total Size", "data.object_total_size"),
    ],
)

bucket_policy_info = ItemDynamicLayout.set_fields(
    "Bucket Policy",
    fields=[
        TextDyField.data_source(
            "Policy Document Exists", "data.policy_document_exists"
        ),
        MoreField.data_source(
            "Bucket Policy Document",
            "data.output_display",
            options={
                "sub_key": "data.bucket_policy.policy_document",
                "layout": {
                    "name": "Bucket Policy Document",
                    "type": "popup",
                    "options": {"layout": {"type": "raw"}},
                },
            },
        ),
    ],
)

bucket_acl_info = TableDynamicLayout.set_fields(
    "Access Control List",
    "data.bucket_acl.grants",
    fields=[
        TextDyField.data_source("Grantee Type", "grantee.type"),
        TextDyField.data_source("Canonical ID", "grantee.id"),
        TextDyField.data_source("Group URI", "grantee.uri"),
        TextDyField.data_source("Email(If Exists)", "grantee.email"),
        TextDyField.data_source("Permission", "readable_permission"),
    ],
)

versioning = ItemDynamicLayout.set_fields(
    "Versioning",
    fields=[
        EnumDyField.data_source(
            "Status",
            "data.versioning.status",
            default_state={"safe": ["Enabled"], "alert": ["Suspended"]},
        ),
        EnumDyField.data_source(
            "MFA Delete",
            "data.versioning.mfa_delete",
            default_badge={"indigo.500": ["Enabled"], "coral.600": ["Disabled"]},
        ),
    ],
)

website_hosting = ItemDynamicLayout.set_fields(
    "Website Hosting",
    fields=[
        TextDyField.data_source(
            "Hostname", "data.website_hosting.redirect_all_requests_to.host_name"
        ),
        EnumDyField.data_source(
            "Protocol",
            "data.website_hosting.redirect_all_requests_to.protocol",
            default_outline_badge=["HTTP", "HTTPS"],
        ),
        TextDyField.data_source(
            "Index Document", "data.website_hosting.index_document.suffix"
        ),
        TextDyField.data_source(
            "Error Document", "data.website_hosting.index_document.key"
        ),
        TextDyField.data_source(
            "Hostname", "data.website_hosting.redirect_all_requests_to.host_name"
        ),
        ListDyField.data_source(
            "Routing Rule Conditions",
            "data.website_hosting.routing_rules",
            default_badge={"type": "outline", "sub_key": "condition"},
        ),
        ListDyField.data_source(
            "Routing Rule Redirect",
            "data.website_hosting.routing_rules",
            default_badge={"type": "outline", "sub_key": "redirect"},
        ),
    ],
)

server_access_log = ItemDynamicLayout.set_fields(
    "Server Access Logging",
    fields=[
        TextDyField.data_source(
            "Target Bucket", "data.server_access_logging.target_bucket"
        ),
        TextDyField.data_source(
            "Target Prefix", "data.server_access_logging.target_prefix"
        ),
    ],
)

encryption = ItemDynamicLayout.set_fields(
    "Encryption",
    fields=[
        ListDyField.data_source(
            "Algorithm",
            "data.encryption.rules",
            default_badge={
                "type": "outline",
                "sub_key": "apply_server_side_encryption_by_default.sse_algorithm",
            },
        )
    ],
)

object_lock = ItemDynamicLayout.set_fields(
    "Object Lock",
    fields=[
        EnumDyField.data_source(
            "Object Lock",
            "data.object_lock.object_lock_enabled",
            default_badge={"indigo.500": ["Enabled"], "coral.600": ["Disabled"]},
        ),
        TextDyField.data_source("Mode", "data.object_lock.rule.default_retention.mode"),
        TextDyField.data_source(
            "Default Retention Days", "data.object_lock.rule.default_retention.days"
        ),
    ],
)

transfer_acc = ItemDynamicLayout.set_fields(
    "Transfer Acceleration",
    fields=[
        EnumDyField.data_source(
            "Status",
            "data.transfer_acceleration.transfer_acceleration",
            default_state={"safe": ["Enabled"], "alert": ["Suspended"]},
        ),
    ],
)

requester_pays = ItemDynamicLayout.set_fields(
    "Requester Pays",
    fields=[
        EnumDyField.data_source(
            "Payers",
            "data.request_payment.request_payment",
            default_badge={"indigo.500": ["BucketOwner"], "coral.600": ["Requester"]},
        ),
    ],
)

topic_conf = TableDynamicLayout.set_fields(
    "Events",
    "data.notification_configurations",
    fields=[
        TextDyField.data_source("ID", "id"),
        TextDyField.data_source("Type", "notification_type"),
        TextDyField.data_source("ARN", "arn"),
        ListDyField.data_source("Events", "events"),
    ],
)

lifecycle_rules = TableDynamicLayout.set_fields(
    "Lifecycle Rules",
    "data.lifecycle_rules",
    fields=[
        TextDyField.data_source("ID", "id"),
        EnumDyField.data_source(
            "Status",
            "status",
            default_state={"safe": ["Enabled"], "alert": ["Disabled"]},
        ),
        DictDyField.data_source("Expiration", "expiration"),
        DictDyField.data_source(
            "Noncurrent Version Expiration", "noncurrent_version_expiration"
        ),
        DictDyField.data_source(
            "Noncurrent Version Expiration", "noncurrent_version_expiration"
        ),
    ],
)

metadata = CloudServiceMeta.set_layouts(
    layouts=[
        bucket,
        object_info,
        bucket_policy_info,
        bucket_acl_info,
        versioning,
        website_hosting,
        server_access_log,
        encryption,
        object_lock,
        transfer_acc,
        requester_pays,
        topic_conf,
        lifecycle_rules,
    ]
)


class S3Resource(CloudServiceResource):
    cloud_service_group = StringType(default="S3")


class BucketResource(S3Resource):
    cloud_service_type = StringType(default="Bucket")
    data = ModelType(Bucket)
    _metadata = ModelType(
        CloudServiceMeta, default=metadata, serialized_name="metadata"
    )


class BucketResponse(CloudServiceResponse):
    resource = PolyModelType(BucketResource)
