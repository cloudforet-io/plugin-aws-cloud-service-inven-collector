import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType, DictType

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")

class PermissionsBoundary(Model):
    permissions_boundary_type = StringType(deserialize_from="PermissionsBoundaryType", choices=("PermissionsBoundaryPolicy"))
    permissions_boundary_arn = StringType(deserialize_from="PermissionsBoundaryArn")

class Permission(Model):
    effect = StringType(deserialize_from="Effect")
    action = ListType(StringType(), default=[])
    resource = ListType(deserialize_from="Resource", default=[])
    condition = DictType(deserialize_from="Condition", serialize_when_none=False)
    sid = StringType(deserialize_from="Sid", serialize_when_none=False)

class PermissionSummary(Model):
    version = StringType(deserialize_from="Version")
    Statement = ListType(ModelType(Permission))

class PermissionVersions(Model):
    create_date = DateTimeType(deserialize_from="CreateDate")
    is_default_version = BooleanType(deserialize_from="IsDefaultVersion")
    version_id = StringType(deserialize_from="VersionId")

class Policy(Model):
    arn = StringType(deserialize_from="Arn")
    attachment_count = IntType(deserialize_from="AttachmentCount")
    is_attachable = BooleanType(deserialize_from="IsAttachable")
    default_version_id = StringType(deserialize_from="DefaultVersionId")
    path = StringType(deserialize_from="Path")
    permissions_boundary_usage_count = IntType(deserialize_from="PermissionsBoundaryUsageCount")
    policy_id = StringType(deserialize_from="PolicyId")
    policy_name = StringType(deserialize_from="PolicyName")
    policy_type = StringType()
    description = StringType(deserialize_from="Description", default='')
    create_date = DateTimeType(deserialize_from="CreateDate")
    update_date = DateTimeType(deserialize_from="UpdateDate")
    permission = ListType(ModelType(PermissionSummary))
    permission_versions = ListType(ModelType(PermissionVersions))

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region_name}#/policies/{self.arn}/$serviceLevelSummary"
        }


class SignInCredential(Model):
    summary = ListType(StringType())
    console_password = StringType()
    assigned_mfa_device = StringType()

class AccessKeyLastUsed(Model):
    last_update_date = DateTimeType(deserialize_from="LastUsedDate", serialize_when_none=False)
    service_name = StringType(deserialize_from="ServiceName")
    region = StringType(deserialize_from="Region")

class AccessKeyInfo(Model):
    key_id = StringType()
    status = StringType(deserialize_from="Status", choices=("Active", "Inactive")),
    access_key_last_used = ModelType(AccessKeyLastUsed, serialize_when_none=False)
    last_update_date_display = StringType(default='N/A')
    create_date = DateTimeType(deserialize_from="CreateDate")

class SSHKeyInfo(Model):
    key_id = StringType()
    status = StringType(deserialize_from="Status", choices=("Active", "Inactive"))
    upload_date = DateTimeType(deserialize_from="UploadDate")

class ServiceSpecificCredentialInfo(Model):
    service_name = StringType(deserialize_from="ServiceName")
    service_specific_credential_id = StringType(deserialize_from="ServiceSpecificCredentialId")
    service_user_name = StringType(deserialize_from="ServiceUserName")
    status = StringType(deserialize_from="Status")
    create_date = DateTimeType(deserialize_from="CreateDate")


class GroupForUser(Model):
    group_name = StringType()
    attached_policy_name = ListType(StringType())
    create_date = DateTimeType(deserialize_from="CreateDate")


class User(Model):
    path = StringType(deserialize_from="Path")
    user_name = StringType(deserialize_from="UserName")
    user_id = StringType(deserialize_from="UserId")
    arn = StringType(deserialize_from="Arn")
    create_date = DateTimeType(deserialize_from="CreateDate")
    password_last_used = DateTimeType(deserialize_from="PasswordLastUsed", serialize_when_none=False)
    groups = ListType(GroupForUser)
    groups_display = StringType(default='')
    sign_in_credential = ModelType(SignInCredential)
    access_key = ListType(ModelType(AccessKeyInfo))
    ssh_public_key = ListType(ModelType(SSHKeyInfo))
    code_commit_credential = ListType(ModelType(ServiceSpecificCredentialInfo))
    cassandra_credential = ListType(ModelType(ServiceSpecificCredentialInfo))
    access_key_age = IntType(default=0)
    access_key_age_display = StringType(default="")
    last_active_age = IntType(default=0)
    last_activity = StringType(default="")
    mfa_device = StringType(default="Not enabled")
    policies = ListType(ModelType(Policy))
    tags = ListType(ModelType(Tags), deserialize_from="Tags")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region_name}#/users/{self.user_name}"
        }


class Group(Model):
    path = StringType(deserialize_from="Path")
    group_name = StringType(deserialize_from="GroupName")
    group_id = StringType(deserialize_from="GroupId")
    arn = StringType(deserialize_from="Arn")
    users = ListType(ModelType(User))
    user_count = IntType(default=0)
    create_date = DateTimeType(deserialize_from="CreateDate")
    attached_permission = ListType(ModelType(Policy))

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region_name}#/groups/{self.group_name}"
        }
#
# class Principal(Model):
#     federated = StringType(deserialize_from="Federated", serialize_when_none=False)
#     service = StringType(deserialize_from="Service", serialize_when_none=False)
#     aws = StringType(deserialize_from="AWS", serialize_when_none=False)

class RolePolicyDocument(Model):
    action = StringType(deserialize_from="Action")
    condition = DictType(deserialize_from="Condition", serialize_when_none=False)
    effect = StringType(deserialize_from="Effect")
    principal = DictType(deserialize_from="Principal")
    sid = StringType(deserialize_from="Sid", serialize_when_none=False)

class Condition:
    condition = StringType()
    key = StringType()
    value = StringType()

class TrustRelationShip(Model):
    trust_relationship = ListType(StringType())
    condition = ListType(ModelType(Condition), default=[])

class AssumeRolePolicyDocument(Model):
    version = StringType(deserialize_from="Version")
    statement = ListType(ModelType(RolePolicyDocument))

class RoleLastUsed(Model):
    last_used_data = DateTimeType(deserialize_from="LastUsedDate")
    region = StringType(deserialize_from="Region")

class Role(Model):
    arn = StringType(deserialize_from="Arn")
    assume_role_policy_document = ModelType(AssumeRolePolicyDocument, deserialize_from="AssumeRolePolicyDocument")
    create_date = DateTimeType(deserialize_from="CreateDate")
    description = StringType(deserialize_from="Description", default='')
    max_session_duration = IntType(deserialize_from="MaxSessionDuration")
    path = StringType(deserialize_from="Path")
    role_id = StringType(deserialize_from="RoleId")
    role_name = StringType(deserialize_from="RoleName")
    last_activity = StringType(default="None")
    role_last_used = ModelType(RoleLastUsed, deserialize_from="RoleLastUsed", default={})
    trusted_entities = ListType(StringType())
    trust_relationship = ListType(ModelType(TrustRelationShip))
    policies = ListType(ModelType(Policy))
    tags = ListType(ModelType(Tags))

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region}#/roles/{self.role_name}"
        }


class IdentityProvider(Model):
    arn = StringType(deserialize_from="Arn")
    url = StringType(deserialize_from="Url")
    provider_type = StringType()
    client_id_list = ListType(StringType, deserialize_from="ClientIDList")
    thumbprint_list = ListType(StringType, deserialize_from="ThumbprintList")
    create_date = DateTimeType(deserialize_from="CreateDate")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region}#/providers/{self.arn}"
        }

