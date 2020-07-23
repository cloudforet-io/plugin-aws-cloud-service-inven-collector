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
    action = ListType(StringType())
    resource = StringType(deserialize_from="Resource")
    condition = DictType(deserialize_from="Condition", serialize_when_none=False)

class PermissionSummary(Model):
    version = StringType(StringType())
    Statement = ListType(ModelType(Permission))

# Policies
# Policy Type list_policy by scope AWS, Local
# AWS -> AWS Managed
# Local -> Customer managed


class Policy(Model):
    policy_name = StringType(deserialize_from="PolicyName")
    policy_id = StringType(deserialize_from="PolicyId")
    policy_type = StringType()
    arn = StringType(deserialize_from="Arn")
    path = StringType(deserialize_from="Path")
    default_version_id = StringType(deserialize_from="DefaultVersionId")
    attachment_count = IntType(deserialize_from="AttachmentCount")
    permissions_boundary_usage_count = IntType(deserialize_from="PermissionsBoundaryUsageCount")
    is_attachable = BooleanType(deserialize_from="IsAttachable")
    description = StringType(deserialize_from="Description")
    create_date = DateTimeType(deserialize_from="CreateDate")
    update_date = DateTimeType(deserialize_from="UpdateDate")
    permission = ListType(ModelType(PermissionSummary))

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region_name}#/policies/{self.arn}/$serviceLevelSummary"
        }


class CredentialKeyInfo(Model):
    key_id = StringType()
    status = StringType()
    create_date = DateTimeType(deserialize_from="CreateDate")


# Paginator.ListAccessKeys(list_access_keys)(UserName) : access_key
# Paginator.ListSSHPublicKeys(list_ssh_public_keys)(UserName): ssh_public_key
# cl.list_service_specific_credentials() : cassandra_credential, code_commit_credential
# filter with userName

class User(Model):
    path = StringType(deserialize_from="Path")
    user_name = StringType(deserialize_from="UserName")
    user_id = StringType(deserialize_from="UserId")
    arn = StringType(deserialize_from="Arn")
    groups = ListType(StringType())
    create_date = DateTimeType(deserialize_from="CreateDate")
    access_key = ListType(ModelType(CredentialKeyInfo))
    ssh_public_key = ListType(ModelType(CredentialKeyInfo))
    code_commit_credential = ListType(ModelType(CredentialKeyInfo))
    cassandra_credential = ListType(ModelType(CredentialKeyInfo))
    access_key_age = IntType(default=0)
    access_key_age_display = StringType(default="")
    password_last_used = DateTimeType(deserialize_from="PasswordLastUsed")
    last_activity = StringType(default="")
    mfa_device = StringType(default="Not enabled")
    permissions_boundary = ModelType(PermissionsBoundary, deserialize_from="PermissionsBoundary")
    policies = ListType(ModelType(Policy))
    tags = ListType(ModelType(Tags), deserialize_from="Tags")

    # TODO: add sign-in credentials

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


class RoleLastUsed(Model):
    last_used_data = DateTimeType(deserialize_from="LastUsedDate")
    region = StringType(deserialize_from="Region")


class Condition(Model):
    condition = StringType()
    Key = StringType()
    Value = StringType()


class Role(Model):
    path = StringType(deserialize_from="Path")
    role_name = StringType(deserialize_from="RoleName")
    role_id = StringType(deserialize_from="RoleId")
    arn = StringType(deserialize_from="Arn")
    create_date = DateTimeType(deserialize_from="CreateDate")
    assume_role_policy_document = StringType(deserialize_from="AssumeRolePolicyDocument")
    description = StringType(deserialize_from="Description")
    max_session_duration = IntType(deserialize_from="MaxSessionDuration")
    permissions_boundary = ModelType(PermissionsBoundary, deserialize_from="PermissionsBoundary")
    policies = ListType(ModelType(Policy))
    tags = ListType(ModelType(Tags))
    role_last_used = ModelType(RoleLastUsed, deserialize_from="RoleLastUsed")
    last_activity = StringType(default="")
    trusted_entities = StringType(default="")
    condition = ListType(ModelType(Condition))

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

