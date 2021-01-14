import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class RotationRules(Model):
    automatically_after_days = IntType(deserialize_from="AutomaticallyAfterDays")


class SecretVersionsToStages(Model):
    string = ListType(StringType,deserialize_from="string")


class SecretTags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class Secret(Model):
    arn = StringType(deserialize_from="ARN")
    name = StringType(deserialize_from="Name")
    description = StringType(deserialize_from="Description")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    rotation_enabled = BooleanType(deserialize_from="RotationEnabled")
    rotation_lambda_arn = StringType(deserialize_from="RotationLambdaARN")
    rotation_rules = ModelType(RotationRules, deserialize_from="RotationRules")
    last_rotated_date = DateTimeType(deserialize_from="LastRotatedDate")
    last_changed_date = DateTimeType(deserialize_from="LastChangedDate")
    last_accessed_date = DateTimeType(deserialize_from="LastAccessedDate")
    deleted_date = DateTimeType(deserialize_from="DeletedDate")
    tags = ListType(ModelType(SecretTags), deserialize_from="Tags", default=[])
    secret_versions_to_stages = ModelType(SecretVersionsToStages, deserialize_from="SecretVersionsToStages")
    owning_service = StringType(deserialize_from="OwningService")
    account_id = StringType(default='')

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/secretsmanager/home?region={region_code}#/secret?name={self.name}"
        }
