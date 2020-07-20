import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class PermissionsBoundary(Model):
    permissions_boundary_type = StringType(deserialize_from="PermissionsBoundaryType", choices=("PermissionsBoundaryPolicy"))
    permissions_boundary_arn = StringType(deserialize_from="PermissionsBoundaryArn")


class UserTags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class User(Model):
    path = StringType(deserialize_from="Path")
    user_name = StringType(deserialize_from="UserName")
    user_id = StringType(deserialize_from="UserId")
    arn = StringType(deserialize_from="Arn")
    create_date = DateTimeType(deserialize_from="CreateDate")
    password_last_used = DateTimeType(deserialize_from="PasswordLastUsed")
    permissions_boundary = ModelType(PermissionsBoundary, deserialize_from="PermissionsBoundary")
    tags = ListType(ModelType(UserTags), deserialize_from="Tags")


class Group(Model):
    path = StringType(deserialize_from="Path")
    group_name = StringType(deserialize_from="GroupName")
    group_id = StringType(deserialize_from="GroupId")
    arn = StringType(deserialize_from="Arn")
    users = ListType(ModelType(User))
    create_date = DateTimeType(deserialize_from="CreateDate")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region=ap-northeast-2#/groups/{self.group_name}"
        }


class RoleTags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


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
    tags = ListType(ModelType(RoleTags))
    role_last_used = ModelType(RoleLastUsed, deserialize_from="RoleLastUsed")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region}#/roles/{self.role_name}"
        }



# Policies
class Policy:
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

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={self.region_name}#/policies/{self.arn}/$serviceLevelSummary"
        }


# Do I need to attach them into each IAMs?
class UserAttachedPolicies:
    attached_policies = ListType(ModelType(Policy, deserialize_from="AttachedPolicies"))

class RoleAttachedPolicies:
    attached_policies = ListType(ModelType(Policy, deserialize_from="AttachedPolicies"))

class GroupAttachedPolicies:
    attached_policies = ListType(ModelType(Policy, deserialize_from="AttachedPolicies"))

