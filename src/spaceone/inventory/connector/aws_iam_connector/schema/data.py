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

