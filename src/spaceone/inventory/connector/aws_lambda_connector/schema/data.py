import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, serializable

_LOGGER = logging.getLogger(__name__)

'''
LAYER
'''
class LatestMatchingVersion(Model):
    layer_version_arn = StringType(deserialize_from="LayerVersionArn")
    version = IntType(deserialize_from="Version")
    description = StringType(deserialize_from="Description")
    created_date = DateTimeType(deserialize_from="CreatedDate")
    compatible_runtimes = ListType(StringType,
                                   deserialize_from="CompatibleRuntimes",
                                   choices=('nodejs', 'nodejs4.3', 'nodejs6.10', 'nodejs8.10', 'nodejs10.x',
                                                        'nodejs12.x', 'java8', 'java11', 'python2.7', 'python3.6',
                                                        'python3.7', 'python3.8', 'dotnetcore1.0', 'dotnetcore2.0',
                                                        'dotnetcore2.1', 'dotnetcore3.1', 'nodejs4.3-edge', 'go1.x',
                                                        'ruby2.5', 'ruby2.7', 'provided'))
    license_info = StringType(deserialize_from="LicenseInfo")


class Layer(Model):
    layer_name = StringType(deserialize_from="LayerName")
    layer_arn = StringType(deserialize_from="LayerArn")
    latest_matching_version = ModelType(LatestMatchingVersion, deserialize_from="LatestMatchingVersion")
    version = IntType(default=1)
    region_name = StringType()
    account_id = StringType()

    @serializable
    def reference(self):
        return {
            "resource_id": self.layer_arn,
            "external_link": f"https://console.aws.amazon.com/lambda/home?region={self.region_name}#/layers/{self.layer_name}/versions/{self.version}"
        }


'''
FUNCTION
'''
class LambdaError(Model):
    error_code = StringType(deserialize_from='ErrorCode')
    message = StringType(deserialize_from='Message')


class EnvironmentVariable(Model):
    key = StringType()
    value = StringType(required=False)


class Environment(Model):
    variables = ListType(ModelType(EnvironmentVariable), default=[])
    error = ModelType(LambdaError, deserialize_from='Error')


class DLC(Model):
    target_arn = StringType(deserialize_from='TargetArn')
    target_name = StringType()


class TracingConfig(Model):
    mode = StringType(choices=['Active', 'PassThrough'], deserialize_from='Mode')


class FunctionLayer(Model):
    arn = StringType(deserialize_from='Arn')
    code_size = IntType(deserialize_from='CodeSize')
    name = StringType()


class LastUpdateStatus(Model):
    type = StringType(choices=['Successful', 'Failed', 'InProgress'])
    reason = StringType()
    reason_code = StringType(
        choices=['EniLimitExceeded', 'InsufficientRolePermissions', 'InvalidConfiguration', 'InternalError',
                 'SubnetOutOfIPAddresses', 'InvalidSubnet', 'InvalidSecurityGroup'])


class LambdaState(Model):
    type = StringType(choices=['Pending', 'Active', 'Inactive', 'Failed'])
    reason = StringType()
    reason_code = StringType(
        choices=['Idle', 'Creating', 'Restoring', 'EniLimitExceeded', 'InsufficientRolePermissions',
                 'InvalidConfiguration', 'InternalError', 'SubnetOutOfIPAddresses', 'InvalidSubnet',
                 'InvalidSecurityGroup', ])


class Subnet(Model):
    id = StringType()
    name = StringType()


class SecurityGroup(Model):
    id = StringType()
    name = StringType()


class VPC(Model):
    id = StringType()
    name = StringType(default='')
    is_default = BooleanType()


class VPCConfig(Model):
    subnets = ListType(ModelType(Subnet), default=[])
    security_groups = ListType(ModelType(SecurityGroup), default=[])
    vpc = ModelType(VPC)


class LambdaFunctionData(Model):
    name = StringType(deserialize_from='FunctionName', default='')
    arn = StringType(deserialize_from='FunctionArn', default='')
    master_arn = StringType(deserialize_from='MasterArn', default='')
    region_name = StringType(default='')
    account_id = StringType(default='')

    runtime = StringType(deserialize_from='Runtime', default='')
    role = StringType(deserialize_from='Role', default='')
    handler = StringType(deserialize_from='Handler', default='')
    code_size = IntType(deserialize_from='CodeSize')
    description = StringType(deserialize_from='Description', default='')
    time_out = IntType(deserialize_from='Timeout')
    memory_size = IntType(deserialize_from='MemorySize')
    last_modified = DateTimeType(deserialize_from='LastModified')
    code_sha256 = StringType(deserialize_from='CodeSha256')
    version = StringType(deserialize_from='Version', default='')
    trace_config = ModelType(TracingConfig, deserialize_from='TracingConfig')
    environment = ModelType(Environment, deserialize_from='Environment', default={})
    revision_id = StringType(deserialize_from='RevisionId', default='')
    kms_key_arn = StringType(deserialize_from='KMSKeyArn', default='')
    state = ModelType(LambdaState)
    last_update = ModelType(LastUpdateStatus)

    # get sub resource - vpc
    vpc_config = ModelType(VPCConfig, required=False)
    # get sub resource - sqs
    dead_letter_config = ModelType(DLC, deserialize_from='DeadLetterConfig', default={})
    # get sub resource - lambda layer
    layers = ListType(ModelType(FunctionLayer), deserialize_from='Layers', default=[])

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/lambda/home?region={self.region_name}#/functions/{self.name}"
        }
