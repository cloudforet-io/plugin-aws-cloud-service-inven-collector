import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, FloatType, DateTimeType, serializable, ListType, \
    BooleanType

_LOGGER = logging.getLogger(__name__)

'''
NOTIFICATION CONFIGURATION
'''
class NotificationConfiguration(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    topic_arn = StringType(deserialize_from="TopicARN")
    notification_type = StringType(deserialize_from="NotificationType")

'''
LIFECYCLE HOOK
'''
class LifecycleHook(Model):
    lifecycle_hook_name = StringType(deserialize_from="LifecycleHookName")
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    lifecycle_transition = StringType(deserialize_from="LifecycleTransition")
    notification_target_arn = StringType(deserialize_from="NotificationTargetARN")
    role_arn = StringType(deserialize_from="RoleARN")
    notification_metadata = StringType(deserialize_from="NotificationMetadata")
    heartbeat_timeout = IntType(deserialize_from="HeartbeatTimeout")
    global_timeout = IntType(deserialize_from="GlobalTimeout")
    default_result = StringType(deserialize_from="DefaultResult")

'''
SCHEDULED ACTION
'''
class ScheduledAction(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    scheduled_action_name = StringType(deserialize_from="ScheduledActionName")
    scheduled_action_arn = StringType(deserialize_from="ScheduledActionARN")
    time = DateTimeType(deserialize_from="Time")
    start_time = DateTimeType(deserialize_from="StartTime")
    end_time = DateTimeType(deserialize_from="EndTime")
    recurrence = StringType(deserialize_from="Recurrence")
    min_size = IntType(deserialize_from="MinSize")
    max_size = IntType(deserialize_from="MaxSize")
    desired_capacity = IntType(deserialize_from="DesiredCapacity")

'''
POLICY
'''
class PredefinedMetricSpecification(Model):
    predefined_metric_type = StringType(deserialize_from="PredefinedMetricType", choices=("ASGAverageCPUUtilization",
                                                                                          "ASGAverageNetworkIn",
                                                                                          "ASGAverageNetworkOut",
                                                                                          "ALBRequestCountPerTarget"))
    resource_label = StringType(deserialize_from="ResourceLabel")


class CustomizedMetricSpecificationDimensions(Model):
    name = StringType(deserialize_from="Name")
    value = StringType(deserialize_from="Value")


class CustomizedMetricSpecification(Model):
    metric_name = StringType(deserialize_from="MetricName")
    namespace = StringType(deserialize_from="Namespace")
    dimensions = ListType(ModelType(CustomizedMetricSpecificationDimensions), deserialize_from="Dimensions")
    statistic = StringType(deserialize_from="Statistic", choices=("Average",
                                                                  "Minimum",
                                                                  "Maximum",
                                                                  "SampleCount",
                                                                  "Sum"))
    unit = StringType(deserialize_from="Unit")


class TargetTrackingConfiguration(Model):
    predefined_metric_specification = ModelType(PredefinedMetricSpecification,
                                                deserialize_from="PredefinedMetricSpecification")
    customized_metric_specification = ModelType(CustomizedMetricSpecification,
                                                deserialize_from="CustomizedMetricSpecification")
    target_value = FloatType(deserialize_from="TargetValue")
    disable_scale_in = BooleanType(deserialize_from="DisableScaleIn")


class AutoScalingPolicyStepAdjustments(Model):
    metric_interval_lower_bound = FloatType(deserialize_from="MetricIntervalLowerBound")
    metric_interval_upper_bound = FloatType(deserialize_from="MetricIntervalUpperBound")
    scaling_adjustment = IntType(deserialize_from="ScalingAdjustment")


class AutoScalingPolicyAlarms(Model):
    alarm_name = StringType(deserialize_from="AlarmName")
    alarm_arn = StringType(deserialize_from="AlarmARN")


class AutoScalingPolicy(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    policy_name = StringType(deserialize_from="PolicyName")
    policy_arn = StringType(deserialize_from="PolicyARN")
    policy_type = StringType(deserialize_from="PolicyType")
    adjustment_type = StringType(deserialize_from="AdjustmentType")
    min_adjustment_step = IntType(deserialize_from="MinAdjustmentStep")
    min_adjustment_magnitude = IntType(deserialize_from="MinAdjustmentMagnitude")
    scaling_adjustment = IntType(deserialize_from="ScalingAdjustment")
    cooldown = IntType(deserialize_from="Cooldown")
    step_adjustments = ListType(ModelType(AutoScalingPolicyStepAdjustments), deserialize_from="StepAdjustments")
    metric_aggregation_type = StringType(deserialize_from="MetricAggregationType")
    estimated_instance_warmup = IntType(deserialize_from="EstimatedInstanceWarmup")
    alarms = ListType(ModelType(AutoScalingPolicyAlarms), deserialize_from="Alarms")
    target_tracking_configuration = ModelType(TargetTrackingConfiguration,
                                              deserialize_from="TargetTrackingConfiguration")
    enabled = BooleanType(deserialize_from="Enabled")

'''
LAUNCH CONFIGURATION
'''
class Ebs(Model):
    snapshot_id = StringType(deserialize_from="SnapshotId")
    volume_size = IntType(deserialize_from="VolumeSize")
    volume_type = StringType(deserialize_from="VolumeType")
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination")
    iops = IntType(deserialize_from="Iops")
    encrypted = BooleanType(deserialize_from="Encrypted")


class InstanceMonitoring(Model):
    enabled = BooleanType(deserialize_from="Enabled")


class AutoScalingLaunchConfigurationBlockDeviceMappings(Model):
    virtual_name = StringType(deserialize_from="VirtualName")
    device_name = StringType(deserialize_from="DeviceName")
    ebs = ModelType(Ebs, deserialize_from="Ebs")
    no_device = BooleanType(deserialize_from="NoDevice")


class LaunchConfiguration(Model):
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName")
    launch_configuration_arn = StringType(deserialize_from="LaunchConfigurationARN")
    image_id = StringType(deserialize_from="ImageId")
    key_name = StringType(deserialize_from="KeyName")
    security_groups = ListType(StringType, deserialize_from="SecurityGroups")
    classic_link_vpc_id = StringType(deserialize_from="ClassicLinkVPCId")
    classic_link_vpc_security_groups = ListType(StringType, deserialize_from="ClassicLinkVPCSecurityGroups")
    user_data = StringType(deserialize_from="UserData")
    instance_type = StringType(deserialize_from="InstanceType")
    kernel_id = StringType(deserialize_from="KernelId")
    ramdisk_id = StringType(deserialize_from="RamdiskId")
    block_device_mappings = ListType(ModelType(AutoScalingLaunchConfigurationBlockDeviceMappings),
                                     deserialize_from="BlockDeviceMappings")
    instance_monitoring = ModelType(InstanceMonitoring, deserialize_from="InstanceMonitoring")
    spot_price = StringType(deserialize_from="SpotPrice")
    iam_instance_profile = StringType(deserialize_from="IamInstanceProfile")
    created_time = DateTimeType(deserialize_from="CreatedTime")
    ebs_optimized = BooleanType(deserialize_from="EbsOptimized")
    associate_public_ip_address = BooleanType(deserialize_from="AssociatePublicIpAddress")
    placement_tenancy = StringType(deserialize_from="PlacementTenancy")
    region_name = StringType(default='')
    account_id = StringType(default='')

    @serializable
    def reference(self):
        return {
            "resource_id": self.launch_configuration_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/autoscaling/home?region={self.region_name}#LaunchConfigurations:id={self.launch_configuration_name}"
        }


'''
LAUNCH TEMPLATE
'''


class LicenseSpecification(Model):
    license_configuration_arn = StringType(deserialize_from="LicenseConfigurationArn")


class ElasticInferenceAccelerators(Model):
    type = StringType(deserialize_from="Type")
    count = IntType(deserialize_from="Count")


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


class TagSpecifications(Model):
    resource_type = StringType(deserialize_from="ResourceType")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")


class Placement(Model):
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    affinity = StringType(deserialize_from="Affinity")
    group_name = StringType(deserialize_from="GroupName")
    host_id = StringType(deserialize_from="HostId")
    tenancy = StringType(deserialize_from="Tenancy", choices=("default", "dedicated", "host"))
    spread_domain = StringType(deserialize_from="SpreadDomain")
    host_resource_group_arn = StringType(deserialize_from="HostResourceGroupARN")
    partition_num = IntType(deserialize_from="PartitionNumber")


class Monitoring(Model):
    enabled = BooleanType(deserialize_from="Enabled")


class PrivateIpAddresses(Model):
    primary = BooleanType(deserialize_from="Primary")
    private_ip_address = StringType(deserialize_from="PrivateIpAddress")


class Ipv6Addresses(Model):
    Ipv6Address = StringType(deserialize_from="Ipv6Address")


class NetworkInterfaces(Model):
    associate_carrier_ip_address = BooleanType(deserialize_from="AssociateCarrierIpAddress")
    associate_public_ip_address = BooleanType(deserialize_from="AssociatePublicIpAddress")
    delete_on_termination = BooleanType(deserialize_from="DeleteOnTermination")
    description = StringType(deserialize_from="Description")
    device_index = IntType(deserialize_from="DeviceIndex")
    groups = ListType(StringType, deserialize_from="Groups")
    interface_type = StringType(deserialize_from="InterfaceType")
    ipv6_address_count = IntType(deserialize_from="Ipv6AddressCount")
    ipv6_addresses = ListType(ModelType(Ipv6Addresses), deserialize_from="Ipv6Addresses")
    network_interface_id = StringType(deserialize_from="NetworkInterfaceId")
    private_ip_address = StringType(deserialize_from="PrivateIpAddress")
    private_ip_addresses = ListType(ModelType(PrivateIpAddresses), deserialize_from="PrivateIpAddresses")
    primary_ip_address = StringType(deserialize_from="PrimaryIpAddress")
    secondary_private_ip_address_count = IntType(deserialize_from="SecondaryPrivateIpAddressCount")
    subnet_id = StringType(deserialize_from="SubnetId")


class AutoScalingLaunchTemplateBlockDeviceMappings(Model):
    device_name = StringType(deserialize_from="DeviceName")
    virtual_name = StringType(deserialize_from="VirtualName")
    ebs = ModelType(Ebs, deserialize_from="Ebs")
    no_device = BooleanType(deserialize_from="NoDevice")


class IamInstanceProfile(Model):
    arn = StringType(deserialize_from="ARN")
    name = StringType(deserialize_from="Name")


class LaunchTemplateData(Model):
    kernel_id = StringType(deserialize_from="KernelId")
    ebs_optimized = BooleanType(deserialize_from="EbsOptimized")
    iam_instance_profile = ModelType(IamInstanceProfile, deserialize_from="IamInstanceProfile")
    block_device_mappings = ListType(ModelType(AutoScalingLaunchTemplateBlockDeviceMappings),
                                     deserialize_from="BlockDeviceMappings")
    network_interfaces = ListType(ModelType(NetworkInterfaces), deserialize_from="NetworkInterfaces")
    image_id = StringType(deserialize_from="ImageId")
    instance_type = StringType(deserialize_from="InstanceType")
    key_name = StringType(deserialize_from="KeyName")
    monitoring = ModelType(Monitoring, deserialize_from="Monitoring")
    placement = ModelType(Placement, deserialize_from="Placement")
    ram_disk_id = StringType(deserialize_from="RamDiskId")
    disable_api_termination = BooleanType(deserialize_from="DisableApiTermination")
    instance_initiated_shutdown_behavior = StringType(deserialize_from="InstanceInitiatedShutdownBehavior",
                                                      choices=("stop", "terminate"))
    user_data = StringType(deserialize_from="UserData")
    tag_specifications = ListType(ModelType(TagSpecifications), deserialize_from="TagSpecifications")
    elastic_inference_accelerators = ListType(ModelType(ElasticInferenceAccelerators),
                                              deserialize_from="ElasticInferenceAccelerators")
    security_group_ids = ListType(StringType, deserialize_from="SecurityGroupIds")
    security_groups = ListType(StringType, deserialize_from="SecurityGroups")
    license_specification = ListType(ModelType(LicenseSpecification), deserialize_from="LicenseSpecification")


class LaunchTemplateDetail(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId")
    launch_template_name = StringType(deserialize_from="LaunchTemplateName")
    version = IntType(deserialize_from="Version")
    version_description = StringType(deserialize_from="VersionDescription")
    create_time = DateTimeType(deserialize_from="CreateTime")
    created_by = StringType(deserialize_from="CreatedBy")
    default_version = BooleanType(deserialize_from="DefaultVersion")
    launch_template_data = ModelType(LaunchTemplateData, deserialize_from="LaunchTemplateData")
    region_name = StringType(default='')
    account_id = StringType(default='')
    arn = StringType()

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/ec2autoscaling/home?region={self.region_name}#/details?id={self.launch_template_id}"
        }

'''
AUTO SCALING GROUPS
'''


class LaunchTemplate(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId")
    launch_template_name = StringType(deserialize_from="LaunchTemplateName")
    version = StringType(deserialize_from="Version")


class LaunchTemplateSpecification(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId")
    launch_template_name = StringType(deserialize_from="LaunchTemplateName")
    version = StringType(deserialize_from="Version")


class LaunchTemplateOverrides(Model):
    instance_type = StringType(deserialize_from="InstanceType")
    weighted_capacity = StringType(deserialize_from="WeightedCapacity")


class MixedInstancesPolicyLaunchTemplate(Model):
    launch_template_specification = ModelType(LaunchTemplateSpecification,
                                              deserialize_from="LaunchTemplateSpecification")
    overrides = ListType(ModelType(LaunchTemplateOverrides), deserialize_from="Overrides")


class InstancesDistribution(Model):
    on_demand_allocation_strategy = StringType(deserialize_from="OnDemandAllocationStrategy")
    on_demand_base_capacity = IntType(deserialize_from="OnDemandBaseCapacity")
    on_demand_percentage_above_base_capacity = IntType(deserialize_from="OnDemandPercentageAboveBaseCapacity")
    spot_allocation_strategy = StringType(deserialize_from="SpotAllocationStrategy")
    spot_instance_pools = IntType(deserialize_from="SpotInstancePools")
    spot_max_price = StringType(deserialize_from="SpotMaxPrice")


class MixedInstancesPolicy(Model):
    launch_template = ModelType(MixedInstancesPolicyLaunchTemplate, deserialize_from="LaunchTemplate")
    instances_distribution = ModelType(InstancesDistribution, deserialize_from="InstancesDistribution")


class AutoScalingGroupInstances(Model):
    instance_id = StringType(deserialize_from="InstanceId")
    instance_type = StringType(deserialize_from="InstanceType")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    lifecycle_state = StringType(deserialize_from="LifecycleState")
    health_status = StringType(deserialize_from="HealthStatus")
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName")
    launch_template = ModelType(LaunchTemplate, deserialize_from="LaunchTemplate")
    protected_from_scale_in = BooleanType(deserialize_from="ProtectedFromScaleIn")
    weighted_capacity = StringType(deserialize_from="WeightedCapacity")


class AutoScalingGroupSuspendedProcesses(Model):
    process_name = StringType(deserialize_from="ProcessName")
    suspension_reason = StringType(deserialize_from="SuspensionReason")


class AutoScalingGroupEnabledMetrics(Model):
    metric = StringType(deserialize_from="Metric")
    granularity = StringType(deserialize_from="Granularity")


class AutoScalingGroupTags(Model):
    resource_id = StringType(deserialize_from="ResourceId")
    resource_type = StringType(deserialize_from="ResourceType")
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")
    propagate_at_launch = BooleanType(deserialize_from="PropagateAtLaunch")


class AutoScalingGroup(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    auto_scaling_group_arn = StringType(deserialize_from="AutoScalingGroupARN")
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName")
    launch_configuration = ModelType(LaunchConfiguration)
    policies = ListType(ModelType(AutoScalingPolicy))
    scheduled_actions = ListType(ModelType(ScheduledAction))
    lifecycle_hooks = ListType(ModelType(LifecycleHook))
    notification_configurations = ListType(ModelType(NotificationConfiguration))
    launch_template = ModelType(LaunchTemplate, deserialize_from="LaunchTemplate")
    mixed_instances_policy = ModelType(MixedInstancesPolicy, deserialize_from="MixedInstancesPolicy")
    min_size = IntType(deserialize_from="MinSize")
    max_size = IntType(deserialize_from="MaxSize")
    desired_capacity = IntType(deserialize_from="DesiredCapacity")
    default_cooldown = IntType(deserialize_from="DefaultCooldown")
    availability_zones = ListType(StringType, deserialize_from="AvailabilityZones")
    load_balancer_names = ListType(StringType, deserialize_from="LoadBalancerNames")
    target_group_arns = ListType(StringType, deserialize_from="TargetGroupARNs")
    health_check_type = StringType(deserialize_from="HealthCheckType")
    health_check_grace_period = IntType(deserialize_from="HealthCheckGracePeriod")
    instances = ListType(ModelType(AutoScalingGroupInstances), deserialize_from="Instances")
    created_time = DateTimeType(deserialize_from="CreatedTime")
    suspended_processes = ListType(ModelType(AutoScalingGroupSuspendedProcesses, deserialize_from="SuspendedProcesses"))
    placement_group = StringType(deserialize_from="PlacementGroup")
    vpc_zone_identifier = StringType(deserialize_from="VPCZoneIdentifier")
    enabled_metrics = ListType(ModelType(AutoScalingGroupEnabledMetrics), deserialize_from="EnabledMetrics")
    status = StringType(deserialize_from="Status")
    tags = ListType(ModelType(AutoScalingGroupTags), deserialize_from="Tags")
    termination_policies = ListType(StringType, deserialize_from="TerminationPolicies")
    new_instances_protected_from_scale_in = BooleanType(deserialize_from="NewInstancesProtectedFromScaleIn")
    service_linked_role_arn = StringType(deserialize_from="ServiceLinkedRoleARN")
    max_instance_lifetime = IntType(deserialize_from="MaxInstanceLifetime")
    region_name = StringType(default='')
    account_id = StringType(default='')

    @serializable
    def reference(self):
        return {
            "resource_id": self.auto_scaling_group_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/autoscaling/home?region={self.region_name}#AutoScalingGroups:id={self.auto_scaling_group_name}"
        }

    @serializable
    def cloudwatch(self):
        return {
            "namespace": "AWS/AutoScaling",
            "dimensions": [
                {
                    "Name": "AutoScalingGroupName",
                    "Value": self.auto_scaling_group_name
                }
            ],
            "region_name": self.region_name
        }
