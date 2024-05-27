import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType
from spaceone.inventory.libs.schema.resource import AWSCloudService


_LOGGER = logging.getLogger(__name__)

"""
LAYER
"""


class LatestMatchingVersion(Model):
    layer_version_arn = StringType(
        deserialize_from="LayerVersionArn", serialize_when_none=False
    )
    version = IntType(deserialize_from="Version", serialize_when_none=False)
    description = StringType(deserialize_from="Description", serialize_when_none=False)
    created_date = DateTimeType(
        deserialize_from="CreatedDate", serialize_when_none=False
    )
    compatible_runtimes = ListType(
        StringType,
        deserialize_from="CompatibleRuntimes",
        serialize_when_none=False,
        choices=(
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "nodejs14.x",
            "nodejs16.x",
            "java8",
            "java8.al2",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "python3.9",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "dotnetcore3.1",
            "dotnet6",
            "dotnet8",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
            "provided.al2",
            "nodejs18.x",
            "python3.10",
            "java17",
            "ruby3.2",
            "ruby3.3",
            "python3.11",
            "nodejs20.x",
            "provided.al2023",
            "python3.12",
            "java21",
        ),
    )
    license_info = StringType(deserialize_from="LicenseInfo", serialize_when_none=False)


class Layer(AWSCloudService):
    layer_name = StringType(deserialize_from="LayerName", serialize_when_none=False)
    layer_arn = StringType(deserialize_from="LayerArn", serialize_when_none=False)
    latest_matching_version = ModelType(
        LatestMatchingVersion,
        deserialize_from="LatestMatchingVersion",
        serialize_when_none=False,
    )
    version = IntType(default=1)

    def reference(self, region_code):
        return {
            "resource_id": self.layer_arn,
            "external_link": f"https://console.aws.amazon.com/lambda/home?region={region_code}#/layers/{self.layer_name}/versions/{self.version}",
        }


"""
FUNCTION
"""


class LambdaError(Model):
    error_code = StringType(deserialize_from="ErrorCode", serialize_when_none=False)
    message = StringType(deserialize_from="Message", serialize_when_none=False)


class EnvironmentVariable(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(required=False, serialize_when_none=False)


class Environment(Model):
    variables = ListType(ModelType(EnvironmentVariable), serialize_when_none=False)
    error = ModelType(LambdaError, deserialize_from="Error", serialize_when_none=False)


class DLC(Model):
    target_arn = StringType(deserialize_from="TargetArn", serialize_when_none=False)
    target_name = StringType(serialize_when_none=False)


class TracingConfig(Model):
    mode = StringType(
        choices=["Active", "PassThrough"],
        deserialize_from="Mode",
        serialize_when_none=False,
    )


class FunctionLayer(Model):
    arn = StringType(deserialize_from="Arn", serialize_when_none=False)
    code_size = IntType(deserialize_from="CodeSize", serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class LastUpdateStatus(Model):
    type = StringType(
        choices=["Successful", "Failed", "InProgress"], serialize_when_none=False
    )
    reason = StringType(serialize_when_none=False)
    reason_code = StringType(
        serialize_when_none=False,
        choices=[
            "EniLimitExceeded",
            "InsufficientRolePermissions",
            "InvalidConfiguration",
            "InternalError",
            "SubnetOutOfIPAddresses",
            "InvalidSubnet",
            "InvalidSecurityGroup",
            "ImageDeleted",
            "ImageAccessDenied",
            "InvalidImage",
            "KMSKeyAccessDenied",
            "KMSKeyNotFound",
            "InvalidStateKMSKey",
            "DisabledKMSKey",
            "EFSIOError",
            "EFSMountConnectivityError",
            "EFSMountFailure",
            "EFSMountTimeout",
            "InvalidRuntime",
            "InvalidZipFileException",
            "FunctionError",
        ],
    )


class LambdaState(Model):
    type = StringType(
        choices=["Pending", "Active", "Inactive", "Failed"], serialize_when_none=False
    )
    reason = StringType(serialize_when_none=False)
    reason_code = StringType(
        serialize_when_none=False,
        choices=[
            "Idle",
            "Creating",
            "Restoring",
            "EniLimitExceeded",
            "InsufficientRolePermissions",
            "InvalidConfiguration",
            "InternalError",
            "SubnetOutOfIPAddresses",
            "InvalidSubnet",
            "InvalidSecurityGroup",
            "ImageDeleted",
            "ImageAccessDenied",
            "InvalidImage",
            "KMSKeyAccessDenied",
            "KMSKeyNotFound",
            "InvalidStateKMSKey",
            "DisabledKMSKey",
            "EFSIOError",
            "EFSMountConnectivityError",
            "EFSMountFailure",
            "EFSMountTimeout",
            "InvalidRuntime",
            "InvalidZipFileException",
            "FunctionError",
        ],
    )


class VPCConfig(Model):
    subnet_ids = ListType(
        StringType, deserialize_from="SubnetIds", serialize_when_none=False
    )
    security_group_ids = ListType(
        StringType, deserialize_from="SecurityGroupIds", serialize_when_none=False
    )
    vpc_id = StringType(deserialize_from="VpcId", serialize_when_none=False)


class LambdaFunctionData(AWSCloudService):
    name = StringType(deserialize_from="FunctionName", serialize_when_none=False)
    arn = StringType(deserialize_from="FunctionArn", serialize_when_none=False)
    master_arn = StringType(deserialize_from="MasterArn", serialize_when_none=False)
    runtime = StringType(deserialize_from="Runtime", serialize_when_none=False)
    role = StringType(deserialize_from="Role", serialize_when_none=False)
    handler = StringType(deserialize_from="Handler", serialize_when_none=False)
    code_size = IntType(deserialize_from="CodeSize", serialize_when_none=False)
    description = StringType(deserialize_from="Description", serialize_when_none=False)
    time_out = IntType(deserialize_from="Timeout", serialize_when_none=False)
    memory_size = IntType(deserialize_from="MemorySize", serialize_when_none=False)
    last_modified = DateTimeType(
        deserialize_from="LastModified", serialize_when_none=False
    )
    code_sha256 = StringType(deserialize_from="CodeSha256", serialize_when_none=False)
    version = StringType(deserialize_from="Version", serialize_when_none=False)
    trace_config = ModelType(
        TracingConfig, deserialize_from="TracingConfig", serialize_when_none=False
    )
    environment = ModelType(
        Environment, deserialize_from="Environment", serialize_when_none=False
    )
    revision_id = StringType(deserialize_from="RevisionId", serialize_when_none=False)
    kms_key_arn = StringType(deserialize_from="KMSKeyArn", serialize_when_none=False)
    state = ModelType(LambdaState, serialize_when_none=False)
    last_update = ModelType(LastUpdateStatus, serialize_when_none=False)

    # get sub resource - vpc
    vpc_config = ModelType(VPCConfig, required=False, deserialize_from="VpcConfig")
    # get sub resource - sqs
    dead_letter_config = ModelType(
        DLC, deserialize_from="DeadLetterConfig", serialize_when_none=False
    )
    # get sub resource - lambda layer
    layers = ListType(
        ModelType(FunctionLayer), deserialize_from="Layers", serialize_when_none=False
    )
    # Add Package Type
    package_type = StringType(deserialize_from="PackageType", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/lambda/home?region={region_code}#/functions/{self.name}",
        }
