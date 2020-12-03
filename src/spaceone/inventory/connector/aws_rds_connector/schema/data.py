import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel
_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")


'''
OPTION GROUP
'''
class OptionGroupOptionSettings(Model):
    name = StringType(deserialize_from="Name")
    value = StringType(deserialize_from="Value")
    default_value = StringType(deserialize_from="DefaultValue")
    description = StringType(deserialize_from="Description")
    apply_type = StringType(deserialize_from="ApplyType")
    data_type = StringType(deserialize_from="DataType")
    allowed_values = StringType(deserialize_from="AllowedValues")
    is_modifiable = BooleanType(deserialize_from="IsModifiable")
    is_collection = BooleanType(deserialize_from="IsCollection")


class OptionGroupDBSecurityGroupMemberships(Model):
    db_security_group_name = StringType(deserialize_from="DBSecurityGroupName")
    status = StringType(deserialize_from="Status")


class OptionGroupVpcSecurityGroupMemberships(Model):
    vpc_security_group_id = StringType(deserialize_from="VpcSecurityGroupId")
    status = StringType(deserialize_from="Status")


class Option(Model):
    option_name = StringType(deserialize_from="OptionName")
    option_description = StringType(deserialize_from="OptionDescription")
    persistent = BooleanType(deserialize_from="Persistent")
    permanent = BooleanType(deserialize_from="Permanent")
    port = IntType(deserialize_from="Port")
    option_version = StringType(deserialize_from="OptionVersion")
    option_settings = ListType(ModelType(OptionGroupOptionSettings), deserialize_from="OptionSettings")
    db_security_group_memberships = ListType(ModelType(OptionGroupDBSecurityGroupMemberships),
                                             deserialize_from="DBSecurityGroupMemberships")
    vpc_security_group_memberships = ListType(ModelType(OptionGroupVpcSecurityGroupMemberships),
                                              deserialize_from="VpcSecurityGroupMemberships")


class OptionGroup(Model):
    option_group_name = StringType(deserialize_from="OptionGroupName")
    option_group_description = StringType(deserialize_from="OptionGroupDescription")
    engine_name = StringType(deserialize_from="EngineName")
    major_engine_version = StringType(deserialize_from="MajorEngineVersion")
    options = ListType(ModelType(Option), deserialize_from="Options")
    allows_vpc_and_non_vpc_instance_memberships = BooleanType(deserialize_from="AllowsVpcAndNonVpcInstanceMemberships")
    vpc_id = StringType(deserialize_from="VpcId")
    option_group_arn = StringType(deserialize_from="OptionGroupArn")
    account_id = StringType()

    def reference(self, region_code):
        return {
            "resource_id": self.option_group_arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#option-group-details:option-group-name={self.option_group_name}"
        }



'''
PARAMETER GROUP
'''
class Parameter(Model):
    parameter_name = StringType(deserialize_from="ParameterName")
    parameter_value = StringType(deserialize_from="ParameterValue")
    description = StringType(deserialize_from="Description")
    source = StringType(deserialize_from="Source")
    apply_type = StringType(deserialize_from="ApplyType")
    data_type = StringType(deserialize_from="DataType")
    allowed_values = StringType(deserialize_from="AllowedValues")
    is_modifiable = BooleanType(deserialize_from="IsModifiable")
    minimum_engine_version = StringType(deserialize_from="MinimumEngineVersion")
    apply_method = StringType(deserialize_from="ApplyMethod",choices=("immediate","pending-reboot"))
    supported_engine_modes = ListType(StringType,deserialize_from="SupportedEngineModes")


class ParameterGroup(Model):
    db_parameter_group_name = StringType(deserialize_from="DBParameterGroupName")
    db_parameter_group_family = StringType(deserialize_from="DBParameterGroupFamily")
    description = StringType(deserialize_from="Description")
    db_parameter_group_arn = StringType(deserialize_from="DBParameterGroupArn")
    account_id = StringType()
    parameters = ListType(ModelType(Parameter), default=[])
    tags = ListType(ModelType(Tags), default=[])
    db_parameter_group_type = StringType()

    def reference(self, region_code):
        return {
            "resource_id": self.db_parameter_group_arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#parameter-groups-detail:ids={self.db_parameter_group_name};type={self.db_parameter_group_type};editing=false"
        }


'''
SUBNET GROUP
'''
class SubnetAvailabilityZone(Model):
    name = StringType(deserialize_from="Name")


class SubnetGroupSubnets(Model):
    subnet_identifier = StringType(deserialize_from="SubnetIdentifier")
    subnet_availability_zone = ModelType(SubnetAvailabilityZone,deserialize_from="SubnetAvailabilityZone")
    subnet_status = StringType(deserialize_from="SubnetStatus")


class SubnetGroup(Model):
    db_subnet_group_name = StringType(deserialize_from="DBSubnetGroupName")
    db_subnet_group_description = StringType(deserialize_from="DBSubnetGroupDescription")
    vpc_id = StringType(deserialize_from="VpcId")
    subnet_group_status = StringType(deserialize_from="SubnetGroupStatus")
    subnets = ListType(ModelType(SubnetGroupSubnets), deserialize_from="Subnets")
    db_subnet_group_arn = StringType(deserialize_from="DBSubnetGroupArn")
    account_id = StringType()
    tags = ListType(ModelType(Tags), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.db_subnet_group_arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#db-subnet-group:id={self.db_subnet_group_name}"
        }

'''
SNAPSHOT
'''
class Features(Model):
    name = StringType(deserialize_from="Name")
    value = StringType(deserialize_from="Value")


class Snapshot(Model):
    db_snapshot_identifier = StringType(deserialize_from="DBSnapshotIdentifier")
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier")
    snapshot_create_time = DateTimeType(deserialize_from="SnapshotCreateTime")
    engine = StringType(deserialize_from="Engine")
    allocated_storage = IntType(deserialize_from="AllocatedStorage")
    status = StringType(deserialize_from="Status")
    port = IntType(deserialize_from="Port")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    vpc_id = StringType(deserialize_from="VpcId")
    instance_create_time = DateTimeType(deserialize_from="InstanceCreateTime")
    master_username = StringType(deserialize_from="MasterUsername")
    engine_version = StringType(deserialize_from="EngineVersion")
    license_model = StringType(deserialize_from="LicenseModel")
    snapshot_type = StringType(deserialize_from="SnapshotType")
    iops = IntType(deserialize_from="Iops")
    option_group_name = StringType(deserialize_from="OptionGroupName")
    percent_progress = IntType(deserialize_from="PercentProgress")
    source_region = StringType(deserialize_from="SourceRegion")
    source_db_snapshot_identifier = StringType(deserialize_from="SourceDBSnapshotIdentifier")
    storage_type = StringType(deserialize_from="StorageType")
    tde_credential_arn = StringType(deserialize_from="TdeCredentialArn")
    encrypted = BooleanType(deserialize_from="Encrypted")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    db_snapshot_arn = StringType(deserialize_from="DBSnapshotArn")
    timezone = StringType(deserialize_from="Timezone")
    iam_database_authentication_enabled = BooleanType(deserialize_from="IAMDatabaseAuthenticationEnabled")
    processor_features = ListType(ModelType(Features), deserialize_from="ProcessorFeatures")
    dbi_resource_id = StringType(deserialize_from="DbiResourceId")
    account_id = StringType()
    tags = ListType(ModelType(Tags), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.db_snapshot_arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#snapshot:engine={self.engine};id={self.db_snapshot_identifier}"
        }


'''
INSTANCE
'''
class Endpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")
    hosted_zone_id = StringType(deserialize_from="HostedZoneId")


class SubnetAvailabilityZone(Model):
    name = StringType(deserialize_from="Name")


class DBSubnetGroupSubnets(Model):
    subnet_identifier = StringType(deserialize_from="SubnetIdentifier")
    subnet_availability_zone = ModelType(SubnetAvailabilityZone, deserialize_from="SubnetAvailabilityZone")
    subnet_status = StringType(deserialize_from="SubnetStatus")


class DBSubnetGroup(Model):
    db_subnet_group_name = StringType(deserialize_from="DBSubnetGroupName")
    db_subnet_group_description = StringType(deserialize_from="DBSubnetGroupDescription")
    vpc_id = StringType(deserialize_from="VpcId")
    subnet_group_status = StringType(deserialize_from="SubnetGroupStatus")
    subnets = ListType(ModelType(DBSubnetGroupSubnets), deserialize_from="Subnets")
    db_subnet_group_arn = StringType(deserialize_from="DBSubnetGroupArn")


class PendingCloudwatchLogsExports(Model):
    log_types_to_enable = ListType(StringType, deserialize_from="LogTypesToEnable")
    log_types_to_disable = ListType(StringType, deserialize_from="LogTypesToDisable")


class PendingModifiedValues(Model):
    db_instance_class = StringType(deserialize_from="DBInstanceClass")
    allocated_storage = IntType(deserialize_from="AllocatedStorage")
    master_user_password = StringType(deserialize_from="MasterUserPassword")
    port = IntType(deserialize_from="Port")
    backup_retention_period = IntType(deserialize_from="BackupRetentionPeriod")
    multi_az = BooleanType(deserialize_from="MultiAZ")
    engine_version = StringType(deserialize_from="EngineVersion")
    license_model = StringType(deserialize_from="LicenseModel")
    iops = IntType(deserialize_from="Iops")
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier")
    storage_type = StringType(deserialize_from="StorageType")
    ca_certificate_identifier = StringType(deserialize_from="CACertificateIdentifier")
    db_subnet_group_name = StringType(deserialize_from="DBSubnetGroupName")
    pending_cloudwatch_logs_exports = ModelType(PendingCloudwatchLogsExports,
                                                deserialize_from="PendingCloudwatchLogsExports")
    processor_features = ListType(ModelType(Features), deserialize_from="ProcessorFeatures")


class ListenerEndpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")
    hosted_zone_id = StringType(deserialize_from="HostedZoneId")


class InstanceDBSecurityGroups(Model):
    db_security_group_name = StringType(deserialize_from="DBSecurityGroupName")
    status = StringType(deserialize_from="Status")


class VpcSecurityGroups(Model):
    vpc_security_group_id = StringType(deserialize_from="VpcSecurityGroupId")
    status = StringType(deserialize_from="Status")


class InstanceDBParameterGroups(Model):
    db_parameter_group_name = StringType(deserialize_from="DBParameterGroupName")
    parameter_apply_status = StringType(deserialize_from="ParameterApplyStatus")


class InstanceOptionGroupMemberships(Model):
    option_group_name = StringType(deserialize_from="OptionGroupName")
    status = StringType(deserialize_from="Status")


class InstanceStatusInfos(Model):
    status_type = StringType(deserialize_from="StatusType")
    normal = BooleanType(deserialize_from="Normal")
    status = StringType(deserialize_from="Status")
    message = StringType(deserialize_from="Message")


class InstanceDomainMemberships(Model):
    domain = StringType(deserialize_from="Domain")
    status = StringType(deserialize_from="Status")
    fqdn = StringType(deserialize_from="FQDN")
    iam_role_name = StringType(deserialize_from="IAMRoleName")


class InstanceProcessorFeatures(Model):
    name = StringType(deserialize_from="Name")
    value = StringType(deserialize_from="Value")


class InstanceAssociatedRoles(Model):
    role_arn = StringType(deserialize_from="RoleArn")
    feature_name = StringType(deserialize_from="FeatureName")
    status = StringType(deserialize_from="Status")


class Instance(Model):
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier", serialize_when_none=False)
    db_instance_class = StringType(deserialize_from="DBInstanceClass", serialize_when_none=False)
    engine = StringType(deserialize_from="Engine", serialize_when_none=False)
    db_instance_status = StringType(deserialize_from="DBInstanceStatus", serialize_when_none=False)
    master_username = StringType(deserialize_from="MasterUsername", serialize_when_none=False)
    db_name = StringType(deserialize_from="DBName", serialize_when_none=False)
    endpoint = ModelType(Endpoint, deserialize_from="Endpoint", serialize_when_none=False)
    allocated_storage = IntType(deserialize_from="AllocatedStorage", serialize_when_none=False)
    instance_create_time = DateTimeType(deserialize_from="InstanceCreateTime", serialize_when_none=False)
    preferred_backup_window = StringType(deserialize_from="PreferredBackupWindow", serialize_when_none=False)
    backup_retention_period = IntType(deserialize_from="BackupRetentionPeriod", serialize_when_none=False)
    db_security_groups = ListType(ModelType(InstanceDBSecurityGroups), deserialize_from="DBSecurityGroups",
                                  serialize_when_none=False)
    vpc_security_groups = ListType(ModelType(VpcSecurityGroups), deserialize_from="VpcSecurityGroups",
                                   serialize_when_none=False)
    db_parameter_groups = ListType(ModelType(InstanceDBParameterGroups), deserialize_from="DBParameterGroups",
                                   serialize_when_none=False)
    availability_zone = StringType(deserialize_from="AvailabilityZone", serialize_when_none=False)
    db_subnet_group = ModelType(DBSubnetGroup, deserialize_from="DBSubnetGroup", serialize_when_none=False)
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow", serialize_when_none=False)
    pending_modified_values = ModelType(PendingModifiedValues, deserialize_from="PendingModifiedValues",
                                        serialize_when_none=False)
    latest_restorable_time = DateTimeType(deserialize_from="LatestRestorableTime", serialize_when_none=False)
    multi_az = BooleanType(deserialize_from="MultiAZ", serialize_when_none=False)
    engine_version = StringType(deserialize_from="EngineVersion", serialize_when_none=False)
    auto_minor_version_upgrade = BooleanType(deserialize_from="AutoMinorVersionUpgrade", serialize_when_none=False)
    read_replica_source_db_instance_identifier = StringType(deserialize_from="ReadReplicaSourceDBInstanceIdentifier",
                                                            serialize_when_none=False)
    read_replica_db_instance_identifiers = ListType(StringType, deserialize_from="ReadReplicaDBInstanceIdentifiers",
                                                    serialize_when_none=False)
    read_replica_db_cluster_identifiers = ListType(StringType, deserialize_from="ReadReplicaDBClusterIdentifiers",
                                                   serialize_when_none=False)
    license_model = StringType(deserialize_from="LicenseModel", serialize_when_none=False)
    iops = IntType(deserialize_from="Iops", serialize_when_none=False)
    option_group_memberships = ListType(ModelType(InstanceOptionGroupMemberships),
                                        deserialize_from="OptionGroupMemberships", serialize_when_none=False)
    character_set_name = StringType(deserialize_from="CharacterSetName", serialize_when_none=False)
    secondary_availability_zone = StringType(deserialize_from="SecondaryAvailabilityZone", serialize_when_none=False)
    publicly_accessible = BooleanType(deserialize_from="PubliclyAccessible", serialize_when_none=False)
    status_infos = ListType(ModelType(InstanceStatusInfos), deserialize_from="StatusInfos", serialize_when_none=False)
    storage_type = StringType(deserialize_from="StorageType", serialize_when_none=False)
    tde_credential_arn = StringType(deserialize_from="TdeCredentialArn", serialize_when_none=False)
    db_instance_port = IntType(deserialize_from="DbInstancePort", serialize_when_none=False)
    db_cluster_identifier = StringType(deserialize_from="DBClusterIdentifier", serialize_when_none=False)
    storage_encrypted = BooleanType(deserialize_from="StorageEncrypted", serialize_when_none=False)
    kms_key_id = StringType(deserialize_from="KmsKeyId", serialize_when_none=False)
    dbi_resource_id = StringType(deserialize_from="DbiResourceId", serialize_when_none=False)
    ca_certificate_identifier = StringType(deserialize_from="CACertificateIdentifier",
                                           serialize_when_none=False)
    domain_memberships = ListType(ModelType(InstanceDomainMemberships), deserialize_from="DomainMemberships",
                                  serialize_when_none=False)
    copy_tags_to_snapshot = BooleanType(deserialize_from="CopyTagsToSnapshot", serialize_when_none=False)
    monitoring_interval = IntType(deserialize_from="MonitoringInterval", serialize_when_none=False)
    enhanced_monitoring_resource_arn = StringType(deserialize_from="EnhancedMonitoringResourceArn",
                                                  serialize_when_none=False)
    monitoring_role_arn = StringType(deserialize_from="MonitoringRoleArn", serialize_when_none=False)
    promotion_tier = IntType(deserialize_from="PromotionTier", serialize_when_none=False)
    db_instance_arn = StringType(deserialize_from="DBInstanceArn", serialize_when_none=False)
    timezone = StringType(deserialize_from="Timezone", serialize_when_none=False)
    iam_database_authentication_enabled = BooleanType(deserialize_from="IAMDatabaseAuthenticationEnabled",
                                                      serialize_when_none=False)
    performance_insights_enabled = BooleanType(deserialize_from="PerformanceInsightsEnabled",
                                               serialize_when_none=False)
    performance_insights_kms_key_id = StringType(deserialize_from="PerformanceInsightsKMSKeyId",
                                                 serialize_when_none=False)
    performance_insights_retention_period = IntType(deserialize_from="PerformanceInsightsRetentionPeriod",
                                                    serialize_when_none=False)
    enabled_cloudwatch_logs_exports = ListType(StringType, deserialize_from="EnabledCloudwatchLogsExports",
                                               serialize_when_none=False)
    processor_features = ListType(ModelType(InstanceProcessorFeatures), deserialize_from="ProcessorFeatures",
                                  serialize_when_none=False)
    deletion_protection = BooleanType(deserialize_from="DeletionProtection", serialize_when_none=False)
    associated_roles = ListType(ModelType(InstanceAssociatedRoles), deserialize_from="AssociatedRoles",
                                serialize_when_none=False)
    listener_endpoint = ModelType(ListenerEndpoint, deserialize_from="ListenerEndpoint",
                                  serialize_when_none=False)
    max_allocated_storage = IntType(deserialize_from="MaxAllocatedStorage", serialize_when_none=False)
    tags = ListType(ModelType(Tags), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.db_instance_arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#database:id={self.db_instance_identifier};is-cluster=false"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/RDS",
            "dimensions": [CloudWatchDimensionModel({"Name": "DBInstanceIdentifier", "Value": self.db_instance_identifier})],
            "region_name": region_code
        }

'''
CLUSTER
'''
class ScalingConfigurationInfo(Model):
    min_capacity = IntType(deserialize_from="MinCapacity")
    max_capacity = IntType(deserialize_from="MaxCapacity")
    auto_pause = BooleanType(deserialize_from="AutoPause")
    seconds_until_auto_pause = IntType(deserialize_from="SecondsUntilAutoPause")
    timeout_action = StringType(deserialize_from="TimeoutAction")


class ClusterDBClusterOptionGroupMemberships(Model):
    db_cluster_option_group_name = StringType(deserialize_from="DBClusterOptionGroupName")
    status = StringType(deserialize_from="Status")


class ClusterDBClusterMembers(Model):
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier")
    is_cluster_writer = BooleanType(deserialize_from="IsClusterWriter")
    db_cluster_parameter_group_status = StringType(deserialize_from="DBClusterParameterGroupStatus")
    promotion_tier = IntType(deserialize_from="PromotionTier")


class ClusterAssociatedRoles(Model):
    role_arn = StringType(deserialize_from="RoleArn")
    status = StringType(deserialize_from="Status")
    feature_name = StringType(deserialize_from="FeatureName")


class ClusterDomainMemberships(Model):
    domain = StringType(deserialize_from="Domain")
    status = StringType(deserialize_from="Status")
    fqdn = StringType(deserialize_from="FQDN")
    iam_role_name = StringType(deserialize_from="IAMRoleName")


class Cluster(Model):
    allocated_storage = IntType(deserialize_from="AllocatedStorage", serialize_when_none=False)
    availability_zones = ListType(StringType, deserialize_from="AvailabilityZones", serialize_when_none=False)
    backup_retention_period = IntType(deserialize_from="BackupRetentionPeriod", serialize_when_none=False)
    character_set_name = StringType(deserialize_from="CharacterSetName", serialize_when_none=False)
    database_name = StringType(deserialize_from="DatabaseName", serialize_when_none=False)
    db_cluster_identifier = StringType(deserialize_from="DBClusterIdentifier", serialize_when_none=False)
    db_cluster_parameter_group = StringType(deserialize_from="DBClusterParameterGroup", serialize_when_none=False)
    db_subnet_group = StringType(deserialize_from="DBSubnetGroup", serialize_when_none=False)
    status = StringType(deserialize_from="Status", serialize_when_none=False)
    percent_progress = StringType(deserialize_from="PercentProgress", serialize_when_none=False)
    earliest_restorable_time = DateTimeType(deserialize_from="EarliestRestorableTime", serialize_when_none=False)
    endpoint = StringType(deserialize_from="Endpoint", serialize_when_none=False)
    reader_endpoint = StringType(deserialize_from="ReaderEndpoint", serialize_when_none=False)
    custom_endpoints = ListType(StringType, deserialize_from="CustomEndpoints", serialize_when_none=False)
    multi_az = BooleanType(deserialize_from="MultiAZ", serialize_when_none=False)
    engine = StringType(deserialize_from="Engine", serialize_when_none=False)
    engine_version = StringType(deserialize_from="EngineVersion", serialize_when_none=False)
    latest_restorable_time = DateTimeType(deserialize_from="LatestRestorableTime", serialize_when_none=False)
    port = IntType(deserialize_from="Port", serialize_when_none=False)
    master_username = StringType(deserialize_from="MasterUsername", serialize_when_none=False)
    db_cluster_option_group_memberships = ListType(ModelType(ClusterDBClusterOptionGroupMemberships),
                                                   deserialize_from="DBClusterOptionGroupMemberships",
                                                   serialize_when_none=False)
    preferred_backup_window = StringType(deserialize_from="PreferredBackupWindow", serialize_when_none=False)
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow",
                                              serialize_when_none=False)
    replication_source_identifier = StringType(deserialize_from="ReplicationSourceIdentifier",
                                               serialize_when_none=False)
    read_replica_identifiers = ListType(StringType, deserialize_from="ReadReplicaIdentifiers",
                                        serialize_when_none=False)
    db_cluster_members = ListType(ModelType(ClusterDBClusterMembers),
                                  deserialize_from="DBClusterMembers",
                                  serialize_when_none=False)
    db_cluster_member_counts = IntType(default=0, serialize_when_none=False)
    vpc_security_groups = ListType(ModelType(VpcSecurityGroups), deserialize_from="VpcSecurityGroups",
                                   serialize_when_none=False)
    hosted_zone_id = StringType(deserialize_from="HostedZoneId", serialize_when_none=False)
    storage_encrypted = BooleanType(deserialize_from="StorageEncrypted", serialize_when_none=False)
    kms_key_id = StringType(deserialize_from="KmsKeyId", serialize_when_none=False)
    db_cluster_resource_id = StringType(deserialize_from="DbClusterResourceId", serialize_when_none=False)
    db_cluster_arn = StringType(deserialize_from="DBClusterArn", serialize_when_none=False)
    associated_roles = ListType(ModelType(ClusterAssociatedRoles), deserialize_from="AssociatedRoles",
                                serialize_when_none=False)
    iam_database_authentication_enabled = BooleanType(deserialize_from="IAMDatabaseAuthenticationEnabled",
                                                      serialize_when_none=False)
    clone_group_id = StringType(deserialize_from="CloneGroupId", serialize_when_none=False)
    cluster_create_time = DateTimeType(deserialize_from="ClusterCreateTime", serialize_when_none=False)
    earliest_backtrack_time = DateTimeType(deserialize_from="EarliestBacktrackTime", serialize_when_none=False)
    backtrack_window = IntType(deserialize_from="BacktrackWindow", serialize_when_none=False)
    backtrack_consumed_change_records = IntType(deserialize_from="BacktrackConsumedChangeRecords",
                                                serialize_when_none=False)
    enabled_cloudwatch_logs_exports = ListType(StringType, deserialize_from="EnabledCloudwatchLogsExports",
                                               serialize_when_none=False)
    capacity = IntType(deserialize_from="Capacity", serialize_when_none=False)
    engine_mode = StringType(deserialize_from="EngineMode", serialize_when_none=False)
    scaling_configuration_info = ModelType(ScalingConfigurationInfo, deserialize_from="ScalingConfigurationInfo",
                                           serialize_when_none=False)
    deletion_protection = BooleanType(deserialize_from="DeletionProtection", serialize_when_none=False)
    http_endpoint_enabled = BooleanType(deserialize_from="HttpEndpointEnabled", serialize_when_none=False)
    activity_stream_mode = StringType(deserialize_from="ActivityStreamMode", choices=("sync", "async"),
                                      serialize_when_none=False)
    activity_stream_status = StringType(deserialize_from="ActivityStreamStatus",
                                        serialize_when_none=False,
                                        choices=("stopped", "starting", "started", "stopping"))
    activity_stream_kms_key_id = StringType(deserialize_from="ActivityStreamKmsKeyId",
                                            serialize_when_none=False)
    activity_stream_kinesis_stream_name = StringType(deserialize_from="ActivityStreamKinesisStreamName",
                                                     serialize_when_none=False)
    copy_tags_to_snapshot = BooleanType(deserialize_from="CopyTagsToSnapshot",
                                        serialize_when_none=False)
    cross_account_clone = BooleanType(deserialize_from="CrossAccountClone",
                                      serialize_when_none=False)
    domain_memberships = ListType(ModelType(ClusterDomainMemberships),
                                  deserialize_from="DomainMemberships",
                                  serialize_when_none=False)
    db_cluster_role = StringType()
    tags = ListType(ModelType(Tags), default=[])


class Database(Model):
    arn = StringType()
    db_identifier = StringType()
    status = StringType()
    role = StringType(choices=('cluster', 'instance'))
    engine = StringType()
    availability_zone = StringType()
    size = StringType()
    multi_az = BooleanType()
    cluster = ModelType(Cluster, serialize_when_none=False)
    instance = ModelType(Instance, serialize_when_none=False)
    account_id = StringType()
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        is_cluster = 'true' if self.role == 'cluster' else 'false'
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#database:id={self.db_identifier};is-cluster={is_cluster}"
        }

    def set_cloudwatch(self, region_code):
        dimensions = []

        if self.role == 'cluster':
            dimensions.append(CloudWatchDimensionModel({"Name": "DBClusterIdentifier", "Value": self.db_identifier}))
        elif self.role == 'instance':
            dimensions.append(CloudWatchDimensionModel({"Name": "DBInstanceIdentifier", "Value": self.db_identifier}))

        return {
            "namespace": "AWS/RDS",
            "dimensions": dimensions,
            "region_name": region_code
        }
