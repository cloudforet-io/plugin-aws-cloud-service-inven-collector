import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class PermissionsBoundary(Model):
    permissions_boundary_type = StringType(deserialize_from="PermissionsBoundaryType", choices=("PermissionsBoundaryPolicy"))
    permissions_boundary_arn = StringType(deserialize_from="PermissionsBoundaryArn")


class PermissionSummary(Model):
    version = StringType(StringType())
    Statement = ListType(StringType())


class Permission(Model):
    version = StringType()
    statement = ModelType(PermissionSummary)
    resource = StringType()


# Policies
class Policy(Model):
    policy_name = StringType(deserialize_from="PolicyName")
    policy_id = StringType(deserialize_from="PolicyId")
    arn = StringType(deserialize_from="Arn")
    path = StringType(deserialize_from="Path")
    default_version_id = StringType(deserialize_from="DefaultVersionId")
    attachment_count = IntType(deserialize_from="AttachmentCount")
    permissions_boundary_usage_count = IntType(deserialize_from="PermissionsBoundaryUsageCount")
    is_attachable = BooleanType(deserialize_from="IsAttachable")
    description = StringType(deserialize_from="Description")
    create_date = DateTimeType(deserialize_from="CreateDate")
    update_date = DateTimeType(deserialize_from="UpdateDate")
    permission = ListType(ModelType(Permission))

    # TODO: add Policy Type
    # TODO: add Permissions


    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region_name}#/policies/{self.arn}/$serviceLevelSummary"
        }


class User(Model):
    path = StringType(deserialize_from="Path")
    user_name = StringType(deserialize_from="UserName")
    user_id = StringType(deserialize_from="UserId")
    arn = StringType(deserialize_from="Arn")
    groups = ListType(StringType())
    create_date = DateTimeType(deserialize_from="CreateDate")
    access_key_age = IntType(default=0)
    access_key_age_display = StringType(default="")
    password_last_used = DateTimeType(deserialize_from="PasswordLastUsed")
    last_activity = StringType(default="")
    mfa_device = StringType(default="Not enabled")
    permissions_boundary = ModelType(PermissionsBoundary, deserialize_from="PermissionsBoundary")
    policies = ListType(ModelType(Policy))
    tags = ListType(ModelType(Tags), deserialize_from="Tags")

    # TODO: add sign-in credentials
    # TODO: add access keys
    # TODO: add SSH keys for AWS codecommit
    # TODO: add HTTPS Git credentials for AWS codecommit
    # TODO: addCredentials for Amazon Keyspaces (for Apache Cassandra)

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


class Roles(Model):
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

    # TODO: add trust relationship
    # TODO: add trusted entities


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

