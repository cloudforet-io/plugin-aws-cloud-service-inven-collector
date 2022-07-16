import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


class UpdateParams(Model):
    type = StringType(deserialize_from="type", choices=("Version", "PlatformVersion", "EndpointPrivateAccess",
                                                        "EndpointPublicAccess", "ClusterLogging", "DesiredSize",
                                                        "LabelsToAdd", "LabelsToRemove", "MaxSize", "MinSize",
                                                        "ReleaseVersion", "PublicAccessCidrs"))
    value = StringType(deserialize_from="value")


class UpdateErrors(Model):
    error_code = StringType(deserialize_from="errorCode", choices=("SubnetNotFound", "SecurityGroupNotFound",
                                                                   "EniLimitReached", "IpNotAvailable", "AccessDenied",
                                                                   "OperationNotPermitted", "VpcIdNotFound", "Unknown",
                                                                   "NodeCreationFailure", "PodEvictionFailure",
                                                                   "InsufficientFreeAddresses"))
    error_message = StringType(deserialize_from="errorMessage")
    resource_ids = ListType(StringType, deserialize_from="resourceIds")


class Update(Model):
    id = StringType(deserialize_from="id")
    status = StringType(deserialize_from="status", choices=("InProgress", "Failed", "Cancelled", "Successful"))
    type = StringType(deserialize_from="type", choices=("VersionUpdate", "EndpointAccessUpdate",
                                                        "LoggingUpdate", "ConfigUpdate"))
    params = ListType(ModelType(UpdateParams), deserialize_from="params")
    created_at = DateTimeType(deserialize_from="createdAt")
    errors = ListType(ModelType(UpdateErrors), deserialize_from="errors")


class scalingConfig(Model):
    min_size = IntType(deserialize_from="minSize")
    max_size = IntType(deserialize_from="maxSize")
    desired_size = IntType(deserialize_from="desiredSize")


class remoteAccess(Model):
    ec2_ssh_key = StringType(deserialize_from="ec2SshKey")
    source_security_groups = ListType(StringType, deserialize_from="sourceSecurityGroups")


class labels(Model):
    string = StringType(deserialize_from="string")


class resourcesAutoScalingGroups(Model):
    name = StringType(deserialize_from="name")
    arn = StringType(deserialize_from="arn")


class resources(Model):
    auto_scaling_groups = ListType(ModelType(resourcesAutoScalingGroups), deserialize_from="autoScalingGroups")
    remote_access_security_group = StringType(deserialize_from="remoteAccessSecurityGroup")


class healthIssues(Model):
    code = StringType(deserialize_from="code", choices=("AutoScalingGroupNotFound",
                                                        "AutoScalingGroupInvalidConfiguration",
                                                        "Ec2SecurityGroupNotFound",
                                                        "Ec2SecurityGroupDeletionFailure",
                                                        "Ec2LaunchTemplateNotFound",
                                                        "Ec2LaunchTemplateVersionMismatch",
                                                        "Ec2SubnetNotFound",
                                                        "Ec2SubnetInvalidConfiguration",
                                                        "IamInstanceProfileNotFound",
                                                        "IamLimitExceeded",
                                                        "IamNodeRoleNotFound",
                                                        "NodeCreationFailure",
                                                        "AsgInstanceLaunchFailures",
                                                        "InstanceLimitExceeded",
                                                        "InsufficientFreeAddresses",
                                                        "AccessDenied",
                                                        "InternalFailure"))
    message = StringType(deserialize_from="message")
    resource_ids = ListType(StringType, deserialize_from="resourceIds")


class health(Model):
    issues = ListType(ModelType(healthIssues), deserialize_from="issues")


class NodeGroup(AWSCloudService):
    nodegroup_name = StringType(deserialize_from="nodegroupName")
    nodegroup_arn = StringType(deserialize_from="nodegroupArn")
    cluster_name = StringType(deserialize_from="clusterName")
    cluster_arn = StringType()
    version = StringType(deserialize_from="version")
    release_version = StringType(deserialize_from="releaseVersion")
    created_at = DateTimeType(deserialize_from="createdAt")
    modified_at = DateTimeType(deserialize_from="modifiedAt")
    status = StringType(deserialize_from="status", choices=("CREATING", "ACTIVE", "UPDATING", "DELETING",
                                                            "CREATE_FAILED", "DELETE_FAILED", "DEGRADED"))
    scaling_config = ModelType(scalingConfig, deserialize_from="scalingConfig")
    instance_types = ListType(StringType, deserialize_from="instanceTypes")
    subnets = ListType(StringType, deserialize_from="subnets")
    remote_access = ModelType(remoteAccess, deserialize_from="remoteAccess")
    ami_type = StringType(deserialize_from="amiType", choices=("AL2_x86_64", "AL2_x86_64_GPU"))
    node_role = StringType(deserialize_from="nodeRole")
    labels = ModelType(labels, deserialize_from="labels")
    resources = ModelType(resources, deserialize_from="resources")
    disk_size = IntType(deserialize_from="diskSize")
    health = ModelType(health, deserialize_from="health")

    def reference(self, region_code):
        return {
            "resource_id": self.nodegroup_arn,
            "external_link": f"https://console.aws.amazon.com/eks/home?region={region_code}#/clusters/{self.cluster_name}"
        }

'''
CLUSTER
'''
class resourcesVpcConfig(Model):
    subnet_ids = ListType(StringType, deserialize_from="subnetIds")
    security_group_ids = ListType(StringType, deserialize_from="securityGroupIds")
    cluster_security_group_id = StringType(deserialize_from="clusterSecurityGroupId")
    vpc_id = StringType(deserialize_from="vpcId")
    endpoint_public_access = BooleanType(deserialize_from="endpointPublicAccess")
    endpoint_private_access = BooleanType(deserialize_from="endpointPrivateAccess")
    public_access_cidrs = ListType(StringType, deserialize_from="publicAccessCidrs")


class loggingClusterLogging(Model):
    types = ListType(StringType, deserialize_from="types")
    enabled = BooleanType(deserialize_from="enabled")


class logging(Model):
    cluster_logging = ListType(ModelType(loggingClusterLogging), deserialize_from="clusterLogging")


class oidc(Model):
    issuer = StringType(deserialize_from="issuer")


class identity(Model):
    oidc = ModelType(oidc, deserialize_from="oidc")


class certificateAuthority(Model):
    data = StringType(deserialize_from="data")


class provider(Model):
    key_arn = StringType(deserialize_from="keyArn")


class ClusterencryptionConfig(Model):
    resources = ListType(StringType, deserialize_from="resources")
    provider = ModelType(provider, deserialize_from="provider")


class Cluster(AWSCloudService):
    name = StringType(deserialize_from="name")
    arn = StringType(deserialize_from="arn")
    created_at = DateTimeType(deserialize_from="createdAt")
    version = StringType(deserialize_from="version")
    endpoint = StringType(deserialize_from="endpoint")
    role_arn = StringType(deserialize_from="roleArn")
    resources_vpc_config = ModelType(resourcesVpcConfig, deserialize_from="resourcesVpcConfig")
    logging = ModelType(logging, deserialize_from="logging")
    identity = ModelType(identity, deserialize_from="identity")
    status = StringType(deserialize_from="status", choices=("CREATING", "ACTIVE", "DELETING", "FAILED", "UPDATING"))
    certificate_authority = ModelType(certificateAuthority, deserialize_from="certificateAuthority")
    client_request_token = StringType(deserialize_from="clientRequestToken")
    platform_version = StringType(deserialize_from="platformVersion")
    encryption_config = ListType(ModelType(ClusterencryptionConfig), deserialize_from="encryptionConfig")
    node_groups = ListType(ModelType(NodeGroup))
    updates = ListType(ModelType(Update))

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/eks/home?region={region_code}#/clusters/{self.name}"
        }
