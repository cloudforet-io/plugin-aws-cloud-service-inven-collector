import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

DEFAULT_REGION = 'us-east-1'

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class Condition(Model):
    condition = StringType(serialized_name='condition')
    key = StringType()
    value = StringType()


class PermissionsBoundary(Model):
    permissions_boundary_type = StringType(deserialize_from="PermissionsBoundaryType")
    permissions_boundary_arn = StringType(deserialize_from="PermissionsBoundaryArn")


class Permission(Model):
    action = ListType(StringType(), default=[])
    resource = ListType(StringType(), default=[])
    effect = StringType(deserialize_from="Effect")
    condition = ListType(ModelType(Condition), serialize_when_none=False)
    sid = StringType(deserialize_from="Sid", serialize_when_none=False)


class PermissionSummary(Model):
    version = StringType(deserialize_from="Version")
    statement = ListType(ModelType(Permission), default=[], deserialize_from="Statement")


class PermissionVersions(Model):
    create_date = DateTimeType(deserialize_from="CreateDate")
    is_default_version = BooleanType(deserialize_from="IsDefaultVersion")
    version_id = StringType(deserialize_from="VersionId")


class PolicyUsage(Model):
    name = StringType()
    type = StringType()


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
    policy_usage = ListType(ModelType(PolicyUsage), default=[])
    description = StringType(deserialize_from="Description", default='')
    create_date = DateTimeType(deserialize_from="CreateDate")
    update_date = DateTimeType(deserialize_from="UpdateDate")
    permission = ModelType(PermissionSummary)
    permission_versions = ListType(ModelType(PermissionVersions))

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={DEFAULT_REGION}#/policies/{self.arn}$serviceLevelSummary"
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
    groups = ListType(ModelType(GroupForUser))
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

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={DEFAULT_REGION}#/users/{self.user_name}"
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

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={DEFAULT_REGION}#/groups/{self.group_name}"
        }


class PrincipalMeta(Model):
    key = StringType()
    value = StringType()


class RolePolicyDocument(Model):
    action = ListType(StringType(), deserialize_from="Action")
    condition = ListType(ModelType(Condition), serialize_when_none=False)
    effect = ListType(StringType(), deserialize_from="Effect")
    principal = ListType(ModelType(PrincipalMeta), deserialize_from="Principal")
    sid = ListType(StringType(), serialize_when_none=False)


class TrustRelationShip(Model):
    trusted_entities = ListType(StringType())
    condition_name = ListType(StringType())
    condition_key = ListType(StringType())
    condition_value = ListType(StringType())


class AssumeRolePolicyDocument(Model):
    version = StringType(deserialize_from="Version")
    statement = ListType(ModelType(RolePolicyDocument), default=[])


class RoleLastUsed(Model):
    last_used_data = DateTimeType(deserialize_from="LastUsedDate")
    region = StringType(deserialize_from="Region")


class Role(Model):
    arn = StringType(deserialize_from="Arn")
    assume_role_policy_document = ModelType(AssumeRolePolicyDocument, deserialize_from="AssumeRolePolicyDocument",
                                            default={})
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
    tags = ListType(ModelType(Tags), default=[])

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={DEFAULT_REGION}#/roles/{self.role_name}"
        }


class IdentityProvider(Model):
    arn = StringType(deserialize_from="Arn")
    url = StringType(deserialize_from="Url")
    provider_type = StringType()
    client_id_list = ListType(StringType, deserialize_from="ClientIDList")
    thumbprint_list = ListType(StringType, deserialize_from="ThumbprintList")
    create_date = DateTimeType(deserialize_from="CreateDate")

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={DEFAULT_REGION}#/providers/{self.arn}"
        }

