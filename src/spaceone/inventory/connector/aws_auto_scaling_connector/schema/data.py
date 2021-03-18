import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, FloatType, DateTimeType, serializable, ListType, \
    BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType()
    value = StringType()


'''
NOTIFICATION CONFIGURATION
'''
class NotificationConfiguration(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName", serialize_when_none=False)
    topic_arn = StringType(deserialize_from="TopicARN", serialize_when_none=False)
    notification_type = StringType(deserialize_from="NotificationType", serialize_when_none=False)

'''
LIFECYCLE HOOK
'''
class LifecycleHook(Model):
    lifecycle_hook_name = StringType(deserialize_from="LifecycleHookName", serialize_when_none=False)
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName", serialize_when_none=False)
    lifecycle_transition = StringType(deserialize_from="LifecycleTransition", serialize_when_none=False)
    notification_target_arn = StringType(deserialize_from="NotificationTargetARN", serialize_when_none=False)
    role_arn = StringType(deserialize_from="RoleARN", serialize_when_none=False)
    notification_metadata = StringType(deserialize_from="NotificationMetadata", serialize_when_none=False)
    heartbeat_timeout = IntType(deserialize_from="HeartbeatTimeout", serialize_when_none=False)
    global_timeout = IntType(deserialize_from="GlobalTimeout", serialize_when_none=False)
    default_result = StringType(deserialize_from="DefaultResult", serialize_when_none=False)

'''
SCHEDULED ACTION
'''
class ScheduledAction(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName", serialize_when_none=False)
    scheduled_action_name = StringType(deserialize_from="ScheduledActionName", serialize_when_none=False)
    scheduled_action_arn = StringType(deserialize_from="ScheduledActionARN", serialize_when_none=False)
    time = DateTimeType(deserialize_from="Time", serialize_when_none=False)
    start_time = DateTimeType(deserialize_from="StartTime", serialize_when_none=False)
    end_time = DateTimeType(deserialize_from="EndTime", serialize_when_none=False)
    recurrence = StringType(deserialize_from="Recurrence", serialize_when_none=False)
    min_size = IntType(deserialize_from="MinSize", serialize_when_none=False)
    max_size = IntType(deserialize_from="MaxSize", serialize_when_none=False)
    desired_capacity = IntType(deserialize_from="DesiredCapacity", serialize_when_none=False)

'''
POLICY
'''
class PredefinedMetricSpecification(Model):
    predefined_metric_type = StringType(deserialize_from="PredefinedMetricType", choices=("ASGAverageCPUUtilization",
                                                                                          "ASGAverageNetworkIn",
                                                                                          "ASGAverageNetworkOut",
                                                                                          "ALBRequestCountPerTarget"))
    resource_label = StringType(deserialize_from="ResourceLabel", serialize_when_none=False)


class CustomizedMetricSpecificationDimensions(Model):
    name = StringType(deserialize_from="Name", serialize_when_none=False)
    value = StringType(deserialize_from="Value", serialize_when_none=False)


class CustomizedMetricSpecification(Model):
    metric_name = StringType(deserialize_from="MetricName", serialize_when_none=False)
    namespace = StringType(deserialize_from="Namespace", serialize_when_none=False)
    dimensions = ListType(ModelType(CustomizedMetricSpecificationDimensions),
                          deserialize_from="Dimensions",
                          serialize_when_none=False)
    statistic = StringType(deserialize_from="Statistic", choices=("Average",
                                                                  "Minimum",
                                                                  "Maximum",
                                                                  "SampleCount",
                                                                  "Sum"))
    unit = StringType(deserialize_from="Unit", serialize_when_none=False)


class TargetTrackingConfiguration(Model):
    predefined_metric_specification = ModelType(PredefinedMetricSpecification,
                                                deserialize_from="PredefinedMetricSpecification",
                                                serialize_when_none=False)
    customized_metric_specification = ModelType(CustomizedMetricSpecification,
                                                deserialize_from="CustomizedMetricSpecification",
                                                serialize_when_none=False)
    target_value = FloatType(deserialize_from="TargetValue", serialize_when_none=False)
    disable_scale_in = BooleanType(deserialize_from="DisableScaleIn", serialize_when_none=False)


class AutoScalingPolicyStepAdjustments(Model):
    metric_interval_lower_bound = FloatType(deserialize_from="MetricIntervalLowerBound", serialize_when_none=False)
    metric_interval_upper_bound = FloatType(deserialize_from="MetricIntervalUpperBound", serialize_when_none=False)
    scaling_adjustment = IntType(deserialize_from="ScalingAdjustment", serialize_when_none=False)


class AutoScalingPolicyAlarms(Model):
    alarm_name = StringType(deserialize_from="AlarmName", serialize_when_none=False)
    alarm_arn = StringType(deserialize_from="AlarmARN", serialize_when_none=False)


class AutoScalingPolicy(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName", serialize_when_none=False)
    policy_name = StringType(deserialize_from="PolicyName", serialize_when_none=False)
    policy_arn = StringType(deserialize_from="PolicyARN", serialize_when_none=False)
    policy_type = StringType(deserialize_from="PolicyType", serialize_when_none=False)
    adjustment_type = StringType(deserialize_from="AdjustmentType", serialize_when_none=False)
    min_adjustment_step = IntType(deserialize_from="MinAdjustmentStep", serialize_when_none=False)
    min_adjustment_magnitude = IntType(deserialize_from="MinAdjustmentMagnitude", serialize_when_none=False)
    scaling_adjustment = IntType(deserialize_from="ScalingAdjustment", serialize_when_none=False)
    cooldown = IntType(deserialize_from="Cooldown", serialize_when_none=False)
    step_adjustments = ListType(ModelType(AutoScalingPolicyStepAdjustments),
                                deserialize_from="StepAdjustments",
                                serialize_when_none=False)
    metric_aggregation_type = StringType(deserialize_from="MetricAggregationType", serialize_when_none=False)
    estimated_instance_warmup = IntType(deserialize_from="EstimatedInstanceWarmup", serialize_when_none=False)
    alarms = ListType(ModelType(AutoScalingPolicyAlarms), deserialize_from="Alarms", serialize_when_none=False)
    target_tracking_configuration = ModelType(TargetTrackingConfiguration,
                                              deserialize_from="TargetTrackingConfiguration",
                                              serialize_when_none=False)
    enabled = BooleanType(deserialize_from="Enabled", serialize_when_none=False)

'''
LAUNCH CONFIGURATION
'''
class Ebs(Model):
    snapshot_id = StringType(deserialize_from="SnapshotId", serialize_when_none=False)
    volume_size = IntType(deserialize_from="VolumeSize", serialize_when_none=False)
    volume_type = StringType(deserialize_from="VolumeType", serialize_when_none=False)
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination", serialize_when_none=False)
    iops = IntType(deserialize_from="Iops", serialize_when_none=False)
    encrypted = BooleanType(deserialize_from="Encrypted", serialize_when_none=False)


class InstanceMonitoring(Model):
    enabled = BooleanType(deserialize_from="Enabled", serialize_when_none=False)


class AutoScalingLaunchConfigurationBlockDeviceMappings(Model):
    virtual_name = StringType(deserialize_from="VirtualName", serialize_when_none=False)
    device_name = StringType(deserialize_from="DeviceName", serialize_when_none=False)
    ebs = ModelType(Ebs, deserialize_from="Ebs", serialize_when_none=False)
    no_device = BooleanType(deserialize_from="NoDevice", serialize_when_none=False)


class LaunchConfiguration(Model):
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName", serialize_when_none=False)
    launch_configuration_arn = StringType(deserialize_from="LaunchConfigurationARN", serialize_when_none=False)
    image_id = StringType(deserialize_from="ImageId", serialize_when_none=False)
    key_name = StringType(deserialize_from="KeyName", serialize_when_none=False)
    security_groups = ListType(StringType, deserialize_from="SecurityGroups", serialize_when_none=False)
    classic_link_vpc_id = StringType(deserialize_from="ClassicLinkVPCId", serialize_when_none=False)
    classic_link_vpc_security_groups = ListType(StringType,
                                                deserialize_from="ClassicLinkVPCSecurityGroups",
                                                serialize_when_none=False)
    user_data = StringType(deserialize_from="UserData", serialize_when_none=False)
    instance_type = StringType(deserialize_from="InstanceType", serialize_when_none=False)
    kernel_id = StringType(deserialize_from="KernelId", serialize_when_none=False)
    ramdisk_id = StringType(deserialize_from="RamdiskId", serialize_when_none=False)
    block_device_mappings = ListType(ModelType(AutoScalingLaunchConfigurationBlockDeviceMappings),
                                     deserialize_from="BlockDeviceMappings", serialize_when_none=False)
    instance_monitoring = ModelType(InstanceMonitoring, deserialize_from="InstanceMonitoring", serialize_when_none=False)
    spot_price = StringType(deserialize_from="SpotPrice", serialize_when_none=False)
    iam_instance_profile = StringType(deserialize_from="IamInstanceProfile", serialize_when_none=False)
    created_time = DateTimeType(deserialize_from="CreatedTime", serialize_when_none=False)
    ebs_optimized = BooleanType(deserialize_from="EbsOptimized", serialize_when_none=False)
    associate_public_ip_address = BooleanType(deserialize_from="AssociatePublicIpAddress", serialize_when_none=False)
    placement_tenancy = StringType(deserialize_from="PlacementTenancy", serialize_when_none=False)
    region_name = StringType(serialize_when_none=False)
    account_id = StringType(serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.launch_configuration_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/autoscaling/home?region={region_code}#LaunchConfigurations:id={self.launch_configuration_name}"
        }


'''
LAUNCH TEMPLATE
'''
class LicenseSpecification(Model):
    license_configuration_arn = StringType(deserialize_from="LicenseConfigurationArn", serialize_when_none=False)


class ElasticInferenceAccelerators(Model):
    type = StringType(deserialize_from="Type", serialize_when_none=False)
    count = IntType(deserialize_from="Count", serialize_when_none=False)


class TagSpecifications(Model):
    resource_type = StringType(deserialize_from="ResourceType", serialize_when_none=False)
    tags = ListType(ModelType(Tags), deserialize_from="Tags", serialize_when_none=False)


class Placement(Model):
    availability_zone = StringType(deserialize_from="AvailabilityZone", serialize_when_none=False)
    affinity = StringType(deserialize_from="Affinity", serialize_when_none=False)
    group_name = StringType(deserialize_from="GroupName", serialize_when_none=False)
    host_id = StringType(deserialize_from="HostId", serialize_when_none=False)
    tenancy = StringType(deserialize_from="Tenancy", choices=("default", "dedicated", "host"))
    spread_domain = StringType(deserialize_from="SpreadDomain", serialize_when_none=False)
    host_resource_group_arn = StringType(deserialize_from="HostResourceGroupARN", serialize_when_none=False)
    partition_num = IntType(deserialize_from="PartitionNumber", serialize_when_none=False)


class Monitoring(Model):
    enabled = BooleanType(deserialize_from="Enabled", serialize_when_none=False)


class PrivateIpAddresses(Model):
    primary = BooleanType(deserialize_from="Primary", serialize_when_none=False)
    private_ip_address = StringType(deserialize_from="PrivateIpAddress", serialize_when_none=False)


class Ipv6Addresses(Model):
    Ipv6Address = StringType(deserialize_from="Ipv6Address", serialize_when_none=False)


class NetworkInterfaces(Model):
    associate_carrier_ip_address = BooleanType(deserialize_from="AssociateCarrierIpAddress",
                                               serialize_when_none=False)
    associate_public_ip_address = BooleanType(deserialize_from="AssociatePublicIpAddress",
                                              serialize_when_none=False)
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination", serialize_when_none=False)
    description = StringType(deserialize_from="Description", serialize_when_none=False)
    device_index = IntType(deserialize_from="DeviceIndex", serialize_when_none=False)
    groups = ListType(StringType, deserialize_from="Groups", serialize_when_none=False)
    interface_type = StringType(deserialize_from="InterfaceType", serialize_when_none=False)
    ipv6_address_count = IntType(deserialize_from="Ipv6AddressCount", serialize_when_none=False)
    ipv6_addresses = ListType(ModelType(Ipv6Addresses), deserialize_from="Ipv6Addresses", serialize_when_none=False)
    network_interface_id = StringType(deserialize_from="NetworkInterfaceId", serialize_when_none=False)
    private_ip_address = StringType(deserialize_from="PrivateIpAddress", serialize_when_none=False)
    private_ip_addresses = ListType(ModelType(PrivateIpAddresses),
                                    deserialize_from="PrivateIpAddresses",
                                    serialize_when_none=False)
    primary_ip_address = StringType(deserialize_from="PrimaryIpAddress", serialize_when_none=False)
    secondary_private_ip_address_count = IntType(deserialize_from="SecondaryPrivateIpAddressCount",
                                                 serialize_when_none=False)
    subnet_id = StringType(deserialize_from="SubnetId", serialize_when_none=False)


class AutoScalingLaunchTemplateBlockDeviceMappings(Model):
    device_name = StringType(deserialize_from="DeviceName", serialize_when_none=False)
    virtual_name = StringType(deserialize_from="VirtualName", serialize_when_none=False)
    ebs = ModelType(Ebs, deserialize_from="Ebs", serialize_when_none=False)
    no_device = BooleanType(deserialize_from="NoDevice", serialize_when_none=False)


class IamInstanceProfile(Model):
    arn = StringType(deserialize_from="ARN", serialize_when_none=False)
    name = StringType(deserialize_from="Name", serialize_when_none=False)


class LaunchTemplateData(Model):
    kernel_id = StringType(deserialize_from="KernelId", serialize_when_none=False)
    ebs_optimized = BooleanType(deserialize_from="EbsOptimized", serialize_when_none=False)
    iam_instance_profile = ModelType(IamInstanceProfile, deserialize_from="IamInstanceProfile",
                                     serialize_when_none=False)
    block_device_mappings = ListType(ModelType(AutoScalingLaunchTemplateBlockDeviceMappings),
                                     deserialize_from="BlockDeviceMappings",
                                     serialize_when_none=False)
    network_interfaces = ListType(ModelType(NetworkInterfaces),
                                  deserialize_from="NetworkInterfaces",
                                  serialize_when_none=False)
    image_id = StringType(deserialize_from="ImageId", serialize_when_none=False)
    instance_type = StringType(deserialize_from="InstanceType", serialize_when_none=False)
    key_name = StringType(deserialize_from="KeyName", serialize_when_none=False)
    monitoring = ModelType(Monitoring, deserialize_from="Monitoring", serialize_when_none=False)
    placement = ModelType(Placement, deserialize_from="Placement", serialize_when_none=False)
    ram_disk_id = StringType(deserialize_from="RamDiskId", serialize_when_none=False)
    disable_api_termination = BooleanType(deserialize_from="DisableApiTermination", serialize_when_none=False)
    instance_initiated_shutdown_behavior = StringType(deserialize_from="InstanceInitiatedShutdownBehavior",
                                                      choices=("stop", "terminate"))
    user_data = StringType(deserialize_from="UserData", serialize_when_none=False)
    tag_specifications = ListType(ModelType(TagSpecifications),
                                  deserialize_from="TagSpecifications",
                                  serialize_when_none=False)
    elastic_inference_accelerators = ListType(ModelType(ElasticInferenceAccelerators),
                                              deserialize_from="ElasticInferenceAccelerators",
                                              serialize_when_none=False)
    security_group_ids = ListType(StringType, deserialize_from="SecurityGroupIds", serialize_when_none=False)
    security_groups = ListType(StringType, deserialize_from="SecurityGroups", serialize_when_none=False)
    license_specification = ListType(ModelType(LicenseSpecification),
                                     deserialize_from="LicenseSpecification",
                                     serialize_when_none=False)


class LaunchTemplateDetail(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId", serialize_when_none=False)
    launch_template_name = StringType(deserialize_from="LaunchTemplateName", serialize_when_none=False)
    version = IntType(deserialize_from="Version", serialize_when_none=False)
    version_description = StringType(deserialize_from="VersionDescription", serialize_when_none=False)
    create_time = DateTimeType(deserialize_from="CreateTime", serialize_when_none=False)
    created_by = StringType(deserialize_from="CreatedBy", serialize_when_none=False)
    default_version = BooleanType(deserialize_from="DefaultVersion", serialize_when_none=False)
    launch_template_data = ModelType(LaunchTemplateData, serialize_when_none=False)
    account_id = StringType(default='')
    arn = StringType()

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/ec2autoscaling/home?region={region_code}#/details?id={self.launch_template_id}"
        }


'''
AUTO SCALING GROUPS
'''
class LaunchTemplate(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId", serialize_when_none=False)
    launch_template_name = StringType(deserialize_from="LaunchTemplateName", serialize_when_none=False)
    version = StringType(deserialize_from="Version", serialize_when_none=False)


class LaunchTemplateSpecification(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId", serialize_when_none=False)
    launch_template_name = StringType(deserialize_from="LaunchTemplateName", serialize_when_none=False)
    version = StringType(deserialize_from="Version", serialize_when_none=False)


class LaunchTemplateOverrides(Model):
    instance_type = StringType(deserialize_from="InstanceType", serialize_when_none=False)
    weighted_capacity = StringType(deserialize_from="WeightedCapacity", serialize_when_none=False)


class MixedInstancesPolicyLaunchTemplate(Model):
    launch_template_specification = ModelType(LaunchTemplateSpecification,
                                              deserialize_from="LaunchTemplateSpecification",
                                              serialize_when_none=False)
    overrides = ListType(ModelType(LaunchTemplateOverrides), deserialize_from="Overrides", serialize_when_none=False)


class InstancesDistribution(Model):
    on_demand_allocation_strategy = StringType(deserialize_from="OnDemandAllocationStrategy", serialize_when_none=False)
    on_demand_base_capacity = IntType(deserialize_from="OnDemandBaseCapacity", serialize_when_none=False)
    on_demand_percentage_above_base_capacity = IntType(deserialize_from="OnDemandPercentageAboveBaseCapacity", serialize_when_none=False)
    spot_allocation_strategy = StringType(deserialize_from="SpotAllocationStrategy", serialize_when_none=False)
    spot_instance_pools = IntType(deserialize_from="SpotInstancePools", serialize_when_none=False)
    spot_max_price = StringType(deserialize_from="SpotMaxPrice", serialize_when_none=False)


class MixedInstancesPolicy(Model):
    launch_template = ModelType(MixedInstancesPolicyLaunchTemplate,
                                deserialize_from="LaunchTemplate",
                                serialize_when_none=False)
    instances_distribution = ModelType(InstancesDistribution,
                                       deserialize_from="InstancesDistribution",
                                       serialize_when_none=False)


class AutoScalingGroupInstances(Model):
    instance_id = StringType(deserialize_from="InstanceId", serialize_when_none=False)
    instance_type = StringType(deserialize_from="InstanceType", serialize_when_none=False)
    availability_zone = StringType(deserialize_from="AvailabilityZone", serialize_when_none=False)
    lifecycle_state = StringType(deserialize_from="LifecycleState", serialize_when_none=False)
    lifecycle = StringType(choices=('spot', 'scheduled'), serialize_when_none=False)
    lifecycle_test = StringType(choices=('spot', 'scheduled'), serialize_when_none=False)
    health_status = StringType(deserialize_from="HealthStatus", serialize_when_none=False)
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName", serialize_when_none=False)
    launch_template = ModelType(LaunchTemplate, deserialize_from="LaunchTemplate", serialize_when_none=False)
    protected_from_scale_in = BooleanType(deserialize_from="ProtectedFromScaleIn", serialize_when_none=False)
    weighted_capacity = StringType(deserialize_from="WeightedCapacity", serialize_when_none=False)


class AutoScalingGroupSuspendedProcesses(Model):
    process_name = StringType(deserialize_from="ProcessName", serialize_when_none=False)
    suspension_reason = StringType(deserialize_from="SuspensionReason", serialize_when_none=False)


class AutoScalingGroupEnabledMetrics(Model):
    metric = StringType(deserialize_from="Metric", serialize_when_none=False)
    granularity = StringType(deserialize_from="Granularity", serialize_when_none=False)


class AutoScalingGroupTags(Model):
    resource_id = StringType(deserialize_from="ResourceId", serialize_when_none=False)
    resource_type = StringType(deserialize_from="ResourceType", serialize_when_none=False)
    key = StringType(deserialize_from="Key", serialize_when_none=False)
    value = StringType(deserialize_from="Value", serialize_when_none=False)
    propagate_at_launch = BooleanType(deserialize_from="PropagateAtLaunch", serialize_when_none=False)


class AutoScalingGroup(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    auto_scaling_group_arn = StringType(deserialize_from="AutoScalingGroupARN")
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName", serialize_when_none=False)
    launch_configuration = ModelType(LaunchConfiguration, serialize_when_none=False)
    policies = ListType(ModelType(AutoScalingPolicy), default=[])
    scheduled_actions = ListType(ModelType(ScheduledAction), default=[])
    lifecycle_hooks = ListType(ModelType(LifecycleHook), default=[])
    notification_configurations = ListType(ModelType(NotificationConfiguration), default=[])
    # launch_template = ModelType(LaunchTemplate, deserialize_from="LaunchTemplate", serialize_when_none=False)
    launch_template = ModelType(LaunchTemplateDetail, serialize_when_none=False)
    display_launch_configuration_template = StringType(default="")
    mixed_instances_policy = ModelType(MixedInstancesPolicy,
                                       deserialize_from="MixedInstancesPolicy",
                                       serialize_when_none=False)
    min_size = IntType(deserialize_from="MinSize", serialize_when_none=False)
    max_size = IntType(deserialize_from="MaxSize", serialize_when_none=False)
    desired_capacity = IntType(deserialize_from="DesiredCapacity", serialize_when_none=False)
    default_cooldown = IntType(deserialize_from="DefaultCooldown", serialize_when_none=False)
    availability_zones = ListType(StringType, deserialize_from="AvailabilityZones", default=[])
    load_balancer_names = ListType(StringType, deserialize_from="LoadBalancerNames", default=[])
    target_group_arns = ListType(StringType, deserialize_from="TargetGroupARNs", default=[])
    load_balancer_arns = ListType(StringType, default=[])
    health_check_type = StringType(deserialize_from="HealthCheckType", serialize_when_none=False)
    health_check_grace_period = IntType(deserialize_from="HealthCheckGracePeriod", serialize_when_none=False)
    instances = ListType(ModelType(AutoScalingGroupInstances), default=[])
    created_time = DateTimeType(deserialize_from="CreatedTime")
    suspended_processes = ListType(ModelType(AutoScalingGroupSuspendedProcesses),
                                   deserialize_from="SuspendedProcesses",
                                   serialize_when_none=False)
    placement_group = StringType(deserialize_from="PlacementGroup", serialize_when_none=False)
    vpc_zone_identifier = StringType(deserialize_from="VPCZoneIdentifier", serialize_when_none=False)
    enabled_metrics = ListType(ModelType(AutoScalingGroupEnabledMetrics),
                               deserialize_from="EnabledMetrics",
                               serialize_when_none=False)
    status = StringType(deserialize_from="Status", serialize_when_none=False)
    autoscaling_tags = ListType(ModelType(AutoScalingGroupTags), default=[])
    tags = ListType(ModelType(Tags), default=[])
    termination_policies = ListType(StringType, deserialize_from="TerminationPolicies", serialize_when_none=False)
    new_instances_protected_from_scale_in = BooleanType(deserialize_from="NewInstancesProtectedFromScaleIn",
                                                        serialize_when_none=False)
    service_linked_role_arn = StringType(deserialize_from="ServiceLinkedRoleARN", serialize_when_none=False)
    max_instance_lifetime = IntType(deserialize_from="MaxInstanceLifetime", serialize_when_none=False)
    account_id = StringType(default='')
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.auto_scaling_group_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/autoscaling/home?region={region_code}#AutoScalingGroups:id={self.auto_scaling_group_name}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/AutoScaling",
            "dimensions": [CloudWatchDimensionModel({'Name': 'AutoScalingGroupName', 'Value': self.auto_scaling_group_name})],
            "region_name": region_code
        }