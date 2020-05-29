import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, \
    BooleanType, FloatType

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="key")
    value = StringType(deserialize_from="value")


class AttachmentsDetails(Model):
    name = StringType(deserialize_from="name")
    value = StringType(deserialize_from="value")


class Attachments(Model):
    id = StringType(deserialize_from="id")
    type = StringType(deserialize_from="type")
    status = StringType(deserialize_from="status")
    details = ListType(ModelType(AttachmentsDetails), deserialize_from="details")


class Attributes(Model):
    name = StringType(deserialize_from="name")
    value = StringType(deserialize_from="value")
    target_type = StringType(deserialize_from="targetType")
    target_id = StringType(deserialize_from="targetId")


'''
ECS Instance
'''
class VersionInfo(Model):
    agent_version = StringType(deserialize_from="agentVersion")
    agent_hash = StringType(deserialize_from="agentHash")
    docker_version = StringType(deserialize_from="dockerVersion")


class ContainerInstanceRemainingResources(Model):
    name = StringType(deserialize_from="name")
    type = StringType(deserialize_from="type")
    double_value = FloatType(deserialize_from="doubleValue")
    long_value = IntType(deserialize_from="longValue")
    integer_value = IntType(deserialize_from="integerValue")
    string_set_value = ListType(StringType, deserialize_from="stringSetValue")


class ContainerInstanceRegisteredResources(Model):
    name = StringType(deserialize_from="name")
    type = StringType(deserialize_from="type")
    double_value = FloatType(deserialize_from="doubleValue")
    long_value = IntType(deserialize_from="longValue")
    integer_value = IntType(deserialize_from="integerValue")
    string_set_value = ListType(StringType, deserialize_from="stringSetValue")


class ContainerInstance(Model):
    container_instance_arn = StringType(deserialize_from="containerInstanceArn")
    ec2_instance_id = StringType(deserialize_from="ec2InstanceId")
    capacity_provider_name = StringType(deserialize_from="capacityProviderName")
    version = IntType(deserialize_from="version")
    version_info = ModelType(VersionInfo, deserialize_from="versionInfo")
    remaining_resources = ListType(ModelType(ContainerInstanceRemainingResources),
                                   deserialize_from="remainingResources")
    registered_resources = ListType(ModelType(ContainerInstanceRegisteredResources),
                                    deserialize_from="registeredResources")
    status = StringType(deserialize_from="status")
    status_reason = StringType(deserialize_from="statusReason")
    agent_connected = BooleanType(deserialize_from="agentConnected")
    running_tasks_count = IntType(deserialize_from="runningTasksCount")
    pending_tasks_count = IntType(deserialize_from="pendingTasksCount")
    agent_update_status = StringType(deserialize_from="agentUpdateStatus",
                                     choices=("PENDING", "STAGING", "STAGED", "UPDATING", "UPDATED", "FAILED"))
    attributes = ListType(ModelType(Attributes), deserialize_from="attributes")
    registered_at = DateTimeType(deserialize_from="registeredAt")
    attachments = ListType(ModelType(Attachments), deserialize_from="attachments")
    tags = ListType(ModelType(Tags), deserialize_from="tags")


'''
TASK
'''
class InterfaceAcceleratorOverrides(Model):
    device_name = StringType(deserialize_from="deviceName")
    device_type = StringType(deserialize_from="deviceType")


class ContainerOverrideEnvironment(Model):
    name = StringType(deserialize_from="name")
    value = StringType(deserialize_from="value")


class ContainerOverrideResourceRequirements(Model):
    value = StringType(deserialize_from="value")
    type = StringType(deserialize_from="type", choices=("GPU", "InferenceAccelerator"))


class ContainerOverride(Model):
    name = StringType(deserialize_from="name")
    command = ListType(StringType, deserialize_from="command")
    environment = ListType(ModelType(ContainerOverrideEnvironment), deserialize_from="environment")
    cpu = IntType(deserialize_from="cpu")
    memory = IntType(deserialize_from="memory")
    memory_reservation = IntType(deserialize_from="memoryReservation")
    resource_requirements = ListType(ModelType(ContainerOverrideResourceRequirements),
                                     deserialize_from="resourceRequirements")


class NetworkBinding(Model):
    bind_ip = StringType(deserialize_from="bindIP")
    container_port = IntType(deserialize_from="containerPort")
    host_port = IntType(deserialize_from="hostPort")
    protocol = StringType(deserialize_from="protocol", choices=("tcp", "udp"))


class NetworkInterfaces(Model):
    attachment_id = StringType(deserialize_from="attachmentId")
    private_ipv4_address = StringType(deserialize_from="privateIpv4Address")
    ipv6_address = StringType(deserialize_from="ipv6Address")


class Overrides(Model):
    container_overrides = ListType(ModelType(ContainerOverride), deserialize_from="containerOverrides")
    cpu = StringType(deserialize_from="cpu")
    inference_accelerator_overrides = ListType(ModelType(InterfaceAcceleratorOverrides),
                                               deserialize_from="inferenceAcceleratorOverrides")
    execution_role_arn = StringType(deserialize_from="executionRoleArn")
    memory = StringType(deserialize_from="memory")
    task_role_arn = StringType(deserialize_from="taskRoleArn")


class TaskContainers(Model):
    container_arn = StringType(deserialize_from="containerArn")
    task_arn = StringType(deserialize_from="taskArn")
    name = StringType(deserialize_from="name")
    image = StringType(deserialize_from="image")
    image_digest = StringType(deserialize_from="imageDigest")
    runtime_id = StringType(deserialize_from="runtimeId")
    last_status = StringType(deserialize_from="lastStatus")
    exit_code = IntType(deserialize_from="exitCode")
    reason = StringType(deserialize_from="reason")
    network_bindings = ListType(ModelType(NetworkBinding), deserialize_from="networkBindings")
    network_interfaces = ListType(ModelType(NetworkInterfaces), deserialize_from="networkInterfaces")
    health_status = StringType(deserialize_from="healthStatus", choices=("HEALTHY", "UNHEALTHY", "UNKNOWN"))
    cpu = StringType(deserialize_from="cpu")
    memory = StringType(deserialize_from="memory")
    memory_reservation = StringType(deserialize_from="memoryReservation")
    gpu_ids = ListType(StringType(), deserialize_from="gpuIds")


class TaskInferenceAccelerators(Model):
    device_name = StringType(deserialize_from="deviceName")
    device_type = StringType(deserialize_from="deviceType")


class Task(Model):
    attachments = ListType(ModelType(Attachments), deserialize_from='attachments')
    attributes = ListType(ModelType(Attributes), deserialize_from="attributes")
    availability_zone = StringType(deserialize_from="availabilityZone")
    capacity_provider_name = StringType(deserialize_from="capacityProviderName")
    cluster_arn = StringType(deserialize_from="clusterArn")
    connectivity = StringType(deserialize_from="connectivity", choices=("CONNECTED", "DISCONNECTED"))
    connectivity_at = DateTimeType(deserialize_from="connectivityAt")
    container_instance_arn = StringType(deserialize_from="containerInstanceArn")
    containers = ListType(ModelType(TaskContainers), deserialize_from="containers")
    cpu = StringType(deserialize_from="cpu")
    created_at = DateTimeType(deserialize_from="createdAt")
    desired_status = StringType(deserialize_from="desiredStatus")
    execution_stopped_at = DateTimeType(deserialize_from="executionStoppedAt")
    group = StringType(deserialize_from="group")
    health_status = StringType(deserialize_from="healthStatus", choices=("HEALTHY", "UNHEALTHY", "UNKNOWN"))
    inference_accelerators = ListType(ModelType(TaskInferenceAccelerators), deserialize_from="inferenceAccelerators")
    last_status = StringType(deserialize_from="lastStatus")
    launch_type = StringType(deserialize_from="launchType", choices=("EC2", "FARGATE"))
    memory = StringType(deserialize_from="memory")
    overrides = ModelType(Overrides, deserialize_from="overrides")
    platform_version = StringType(deserialize_from="platformVersion")
    pull_started_at = DateTimeType(deserialize_from="pullStartedAt")
    pull_stopped_at = DateTimeType(deserialize_from="pullStoppedAt")
    started_at = DateTimeType(deserialize_from="startedAt")
    started_by = StringType(deserialize_from="startedBy")
    stop_code = StringType(deserialize_from="stopCode", choices=("TaskFailedToStart",
                                                                 "EssentialContainerExited",
                                                                 "UserInitiated"))
    stopped_at = DateTimeType(deserialize_from="stoppedAt")
    stopped_reason = StringType(deserialize_from="stoppedReason")
    stopping_at = DateTimeType(deserialize_from="stoppingAt")
    tags = ListType(ModelType(Tags), deserialize_from="tags")
    task_arn = StringType(deserialize_from="taskArn")
    task = StringType(default="")
    task_definition_arn = StringType(deserialize_from="taskDefinitionArn")
    task_definition = StringType(default="")
    version = IntType(deserialize_from="version")

'''
SERVICE
'''
class CapacityProviderStrategy(Model):
    capacity_provider = StringType(deserialize_from="capacityProvider")
    weight = IntType(deserialize_from="weight")
    base = IntType(deserialize_from="base")


class AWSVPCConfiguration(Model):
    subnets = ListType(StringType, deserialize_from="subnets")
    security_groups = ListType(StringType, deserialize_from="securityGroups")
    assign_public_ip = StringType(deserialize_from="assignPublicIp", choices=("ENABLED", "DISABLED"))


class NetworkConfiguration(Model):
    aws_vpc_configuration = ModelType(AWSVPCConfiguration, deserialize_from="awsvpcConfiguration")


class ServiceRegistry(Model):
    registry_arn = StringType(deserialize_from="registryArn")
    port = IntType(deserialize_from="port")
    container_name = StringType(deserialize_from="containerName")
    container_port = IntType(deserialize_from="containerPort")


class LoadBalancer(Model):
    target_group_arn = StringType(deserialize_from="targetGroupArn")
    load_balancer_name = StringType(deserialize_from="loadBalancerName")
    container_name = StringType(deserialize_from="containerName")
    container_port = IntType(deserialize_from="containerPort")


class DeploymentConfiguration(Model):
    maximum_percent = IntType(deserialize_from="maximumPercent")
    minimum_healthy_percent = IntType(deserialize_from="minimumHealthyPercent")


class Scale(Model):
    value = FloatType(deserialize_from="value")
    unit = StringType(deserialize_from="unit")


class DeploymentController(Model):
    type = StringType(deserialize_from="type", choices=("ECS", "CODE_DEPLOY", "EXTERNAL"))


class ServiceTaskSets(Model):
    id = StringType(deserialize_from="id")
    task_set_arn = StringType(deserialize_from="taskSetArn")
    service_arn = StringType(deserialize_from="serviceArn")
    cluster_arn = StringType(deserialize_from="clusterArn")
    started_by = StringType(deserialize_from="startedBy")
    external_id = StringType(deserialize_from="externalId")
    status = StringType(deserialize_from="status")
    task_definition = StringType(deserialize_from="taskDefinition")
    computed_desired_count = IntType(deserialize_from="computedDesiredCount")
    pending_count = IntType(deserialize_from="pendingCount")
    running_count = IntType(deserialize_from="runningCount")
    created_at = DateTimeType(deserialize_from="createdAt")
    updated_at = DateTimeType(deserialize_from="updatedAt")
    launch_type = StringType(deserialize_from="launchType", choices=("EC2","FARGATE"))
    capacity_provider_strategy = ListType(ModelType(CapacityProviderStrategy),
                                          deserialize_from="capacityProviderStrategy")
    platform_version = StringType(deserialize_from="platformVersion")
    network_configuration = ListType(ModelType(NetworkConfiguration), deserialize_from="networkConfiguration")
    load_balancers = ListType(ModelType(LoadBalancer))
    service_registries = ListType(ModelType(ServiceRegistry))
    scale = ModelType(Scale, deserialize_from="scale")
    stability_status = StringType(deserialize_from="stabilityStatus", choices=("STEADY_STATE", "STABILIZING"))
    stability_status_at = DateTimeType(deserialize_from="stabilityStatusAt")
    tags = ListType(ModelType(Tags))


class ServiceDeployments(Model):
    id = StringType(deserialize_from="id")
    status = StringType(deserialize_from="status")
    task_definition = StringType(deserialize_from="taskDefinition")
    desired_count = IntType(deserialize_from="desiredCount")
    pending_count = IntType(deserialize_from="pendingCount")
    running_count = IntType(deserialize_from="runningCount")
    created_at = DateTimeType(deserialize_from="createdAt")
    updated_at = DateTimeType(deserialize_from="updatedAt")
    capacity_provider_strategy = ListType(ModelType(CapacityProviderStrategy),
                                          deserialize_from="capacityProviderStrategy")
    launch_type = StringType(deserialize_from="launchType", choices=("EC2", "FARGATE"))
    platform_version = StringType(deserialize_from="platformVersion")
    network_configuration = ModelType(NetworkConfiguration, deserialize_from="networkConfiguration")


class ServiceEvents(Model):
    id = StringType(deserialize_from="id")
    created_at = DateTimeType(deserialize_from="createdAt")
    message = StringType(deserialize_from="message")


class ServicePlacementConstraints(Model):
    type = StringType(deserialize_from="type", choices=("distinctInstance", "memberOf"))
    expression = StringType(deserialize_from="expression")


class ServicePlacementStrategy(Model):
    type = StringType(deserialize_from="type", choices=("random", "spread", "binpack"))
    field = StringType(deserialize_from="field")


class Service(Model):
    service_arn = StringType(deserialize_from="serviceArn")
    service_name = StringType(deserialize_from="serviceName")
    cluster_arn = StringType(deserialize_from="clusterArn")
    load_balancers = ListType(ModelType(LoadBalancer), deserialize_from="loadBalancers")
    service_registries = ListType(ModelType(ServiceRegistry), deserialize_from="serviceRegistries")
    status = StringType(deserialize_from="status")
    desired_count = IntType(deserialize_from="desiredCount")
    running_count = IntType(deserialize_from="runningCount")
    pending_count = IntType(deserialize_from="pendingCount")
    launch_type = StringType(deserialize_from="launchType", choices=("EC2", "FARGATE"))
    capacity_provider_strategy = ListType(ModelType(CapacityProviderStrategy),
                                          deserialize_from="capacityProviderStrategy")
    platform_version = StringType(deserialize_from="platformVersion")
    task_definition = StringType(deserialize_from="taskDefinition")
    deployment_configuration = ModelType(DeploymentConfiguration, deserialize_from="deploymentConfiguration")
    task_sets = ListType(ModelType(ServiceTaskSets), deserialize_from="taskSets")
    deployments = ListType(ModelType(ServiceDeployments), deserialize_from="deployments")
    role_arn = StringType(deserialize_from="roleArn")
    events = ListType(ModelType(ServiceEvents), deserialize_from="events")
    created_at = DateTimeType(deserialize_from="createdAt")
    placement_constraints = ListType(ModelType(ServicePlacementConstraints), deserialize_from="placementConstraints")
    placement_strategy = ListType(ModelType(ServicePlacementStrategy), deserialize_from="placementStrategy")
    network_configuration = ModelType(NetworkConfiguration, deserialize_from="networkConfiguration")
    health_check_grace_period_seconds = IntType(deserialize_from="healthCheckGracePeriodSeconds")
    scheduling_strategy = StringType(deserialize_from="schedulingStrategy", choices=("REPLICA", "DAEMON"))
    deployment_controller = ModelType(DeploymentController, deserialize_from="deploymentController")
    tags = ListType(ModelType(Tags), deserialize_from="tags")
    created_by = StringType(deserialize_from="createdBy")
    enable_ecs_managed_tags = BooleanType(deserialize_from="enableECSManagedTags")
    propagate_tags = StringType(deserialize_from="propagateTags", choices=("TASK_DEFINITION", "SERVICE"))


'''
CLUSTER
'''
class ClusterStatistics(Model):
    name = StringType(deserialize_from="name")
    value = StringType(deserialize_from="value")


class ClusterSettings(Model):
    name = StringType(deserialize_from="name")
    value = StringType(deserialize_from="value")


class Cluster(Model):
    cluster_arn = StringType(deserialize_from="clusterArn")
    cluster_name = StringType(deserialize_from="clusterName")
    status = StringType(deserialize_from="status")
    registered_container_instances_count = IntType(deserialize_from="registeredContainerInstancesCount")
    running_tasks_count = IntType(deserialize_from="runningTasksCount")
    pending_tasks_count = IntType(deserialize_from="pendingTasksCount")
    active_services_count = IntType(deserialize_from="activeServicesCount")
    statistics = ListType(ModelType(ClusterStatistics), deserialize_from="statistics")
    tags = ListType(ModelType(Tags), deserialize_from="tags")
    settings = ListType(ModelType(ClusterSettings), deserialize_from="settings")
    capacity_providers = ListType(StringType, deserialize_from="capacityProviders")
    default_capacity_provider_strategy = ListType(ModelType(CapacityProviderStrategy),
                                                  deserialize_from="defaultCapacityProviderStrategy")
    attachments = ListType(ModelType(Attachments), deserialize_from="attachments")
    attachments_status = StringType(deserialize_from="attachmentsStatus")
    services = ListType(ModelType(Service))
    tasks = ListType(ModelType(Task))
    container_instances = ListType(ModelType(ContainerInstance))
    region_name = StringType(default="")
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.cluster_arn,
            "external_link": f"https://console.aws.amazon.com/ecs/home?region={self.region_name}#/clusters/{self.cluster_name}/services"
        }
