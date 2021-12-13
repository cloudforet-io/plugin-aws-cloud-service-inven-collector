from schematics import Model
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, \
    FloatType


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")

'''
SCHEDULED ACTION
'''
class ResizeCluster(Model):
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")
    cluster_type = StringType(deserialize_from="ClusterType")
    node_type = StringType(deserialize_from="NodeType")
    number_of_nodes = IntType(deserialize_from="NumberOfNodes")
    classic = BooleanType(deserialize_from="Classic")


class PauseCluster(Model):
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")


class ResumeCluster(Model):
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")


class TargetAction(Model):
    resize_cluster = ModelType(ResizeCluster,deserialize_from="ResizeCluster")
    pause_cluster = ModelType(PauseCluster,deserialize_from="PauseCluster")
    resume_cluster = ModelType(ResumeCluster,deserialize_from="ResumeCluster")


class ScheduledAction(Model):
    scheduled_action_name = StringType(deserialize_from="ScheduledActionName")
    target_action = ModelType(TargetAction,deserialize_from="TargetAction")
    schedule = StringType(deserialize_from="Schedule")
    iam_role = StringType(deserialize_from="IamRole")
    scheduled_action_description = StringType(deserialize_from="ScheduledActionDescription")
    state = StringType(deserialize_from="State", choices=("ACTIVE","DISABLED"))
    next_invocations = DateTimeType(deserialize_from="NextInvocations")
    start_time = DateTimeType(deserialize_from="StartTime")
    end_time = DateTimeType(deserialize_from="EndTime")


'''
SNAPSHOT SCHEDULE
'''
class SnapshotScheduleAssociatedClusters(Model):
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")
    schedule_association_state = StringType(deserialize_from="ScheduleAssociationState",
                                            choices=("MODIFYING", "ACTIVE", "FAILED"))


class SnapshotSchedule(Model):
    schedule_definitions = ListType(StringType, deserialize_from="ScheduleDefinitions")
    schedule_identifier = StringType(deserialize_from="ScheduleIdentifier")
    schedule_description = StringType(deserialize_from="ScheduleDescription")
    tags = ListType(ModelType(Tags), deserialize_from="Tags")
    next_invocations = ListType(DateTimeType, deserialize_from="NextInvocations")
    associated_cluster_count = IntType(deserialize_from="AssociatedClusterCount")
    associated_clusters = ListType(ModelType(SnapshotScheduleAssociatedClusters),
                                   deserialize_from="AssociatedClusters")
    associated_state = StringType()

'''
SNAPSHOT
'''
class SnapshotAccountsWithRestoreAccess(Model):
    account_id = StringType(deserialize_from="AccountId")
    account_alias = StringType(deserialize_from="AccountAlias")


class Snapshot(Model):
    snapshot_identifier = StringType(deserialize_from="SnapshotIdentifier")
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")
    snapshot_create_time = DateTimeType(deserialize_from="SnapshotCreateTime")
    status = StringType(deserialize_from="Status")
    port = IntType(deserialize_from="Port")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    cluster_create_time = DateTimeType(deserialize_from="ClusterCreateTime")
    master_username = StringType(deserialize_from="MasterUsername")
    cluster_version = StringType(deserialize_from="ClusterVersion")
    snapshot_type = StringType(deserialize_from="SnapshotType")
    node_type = StringType(deserialize_from="NodeType")
    number_of_nodes = IntType(deserialize_from="NumberOfNodes")
    db_name = StringType(deserialize_from="DBName")
    vpc_id = StringType(deserialize_from="VpcId")
    encrypted = BooleanType(deserialize_from="Encrypted")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    encrypted_with_hsm = BooleanType(deserialize_from="EncryptedWithHSM")
    accounts_with_restore_access = ListType(ModelType(SnapshotAccountsWithRestoreAccess),
                                            deserialize_from="AccountsWithRestoreAccess")
    owner_account = StringType(deserialize_from="OwnerAccount")
    total_backup_size_in_mega_bytes = FloatType(deserialize_from="TotalBackupSizeInMegaBytes")
    actual_incremental_backup_size_in_mega_bytes = FloatType(deserialize_from="ActualIncrementalBackupSizeInMegaBytes")
    backup_progress_in_mega_bytes = FloatType(deserialize_from="BackupProgressInMegaBytes")
    current_backup_rate_in_mega_bytes_per_second = FloatType(deserialize_from="CurrentBackupRateInMegaBytesPerSecond")
    estimated_seconds_to_completion = IntType(deserialize_from="EstimatedSecondsToCompletion")
    elapsed_time_in_seconds = IntType(deserialize_from="ElapsedTimeInSeconds")
    source_region = StringType(deserialize_from="SourceRegion")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    restorable_node_types = ListType(StringType, deserialize_from="RestorableNodeTypes")
    enhanced_vpc_routing = BooleanType(deserialize_from="EnhancedVpcRouting")
    maintenance_track_name = StringType(deserialize_from="MaintenanceTrackName")
    manual_snapshot_retention_period = IntType(deserialize_from="ManualSnapshotRetentionPeriod")
    manual_snapshot_remaining_days = IntType(deserialize_from="ManualSnapshotRemainingDays")
    snapshot_retention_start_time = DateTimeType(deserialize_from="SnapshotRetentionStartTime")


'''
CLUSTER
'''
class Endpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")


class PendingModifiedValues(Model):
    master_user_password = StringType(deserialize_from="MasterUserPassword")
    node_type = StringType(deserialize_from="NodeType")
    number_of_nodes = IntType(deserialize_from="NumberOfNodes")
    cluster_type = StringType(deserialize_from="ClusterType")
    cluster_version = StringType(deserialize_from="ClusterVersion")
    automated_snapshot_retention_period = IntType(deserialize_from="AutomatedSnapshotRetentionPeriod")
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")
    publicly_accessible = BooleanType(deserialize_from="PubliclyAccessible")
    enhanced_vpc_routing = BooleanType(deserialize_from="EnhancedVpcRouting")
    maintenance_track_name = StringType(deserialize_from="MaintenanceTrackName")
    encryption_type = StringType(deserialize_from="EncryptionType")


class RestoreStatus(Model):
    status = StringType(deserialize_from="Status")
    current_restore_rate_in_mega_bytes_per_second = FloatType(deserialize_from="CurrentRestoreRateInMegaBytesPerSecond")
    snapshot_size_in_mega_bytes = IntType(deserialize_from="SnapshotSizeInMegaBytes")
    progress_in_mega_bytes = IntType(deserialize_from="ProgressInMegaBytes")
    elapsed_time_in_seconds = IntType(deserialize_from="ElapsedTimeInSeconds")
    estimated_time_to_completion_in_seconds = IntType(deserialize_from="EstimatedTimeToCompletionInSeconds")


class DataTransferProgress(Model):
    status = StringType(deserialize_from="Status")
    current_rate_in_mega_bytes_per_second = FloatType(deserialize_from="CurrentRateInMegaBytesPerSecond")
    total_data_in_mega_bytes = IntType(deserialize_from="TotalDataInMegaBytes")
    data_transferred_in_mega_bytes = IntType(deserialize_from="DataTransferredInMegaBytes")
    estimated_time_to_completion_in_seconds = IntType(deserialize_from="EstimatedTimeToCompletionInSeconds")
    elapsed_time_in_seconds = IntType(deserialize_from="ElapsedTimeInSeconds")


class HsmStatus(Model):
    hsm_client_certificate_identifier = StringType(deserialize_from="HsmClientCertificateIdentifier")
    hsm_configuration_identifier = StringType(deserialize_from="HsmConfigurationIdentifier")
    status = StringType(deserialize_from="Status")


class ClusterSnapshotCopyStatus(Model):
    destination_region = StringType(deserialize_from="DestinationRegion")
    retention_period = IntType(deserialize_from="RetentionPeriod")
    manual_snapshot_retention_period = IntType(deserialize_from="ManualSnapshotRetentionPeriod")
    snapshot_copy_grant_name = StringType(deserialize_from="SnapshotCopyGrantName")


class ElasticIpStatus(Model):
    elastic_ip = StringType(deserialize_from="ElasticIp")
    status = StringType(deserialize_from="Status")


class ResizeInfo(Model):
    resize_type = StringType(deserialize_from="ResizeType")
    allow_cancel_resize = BooleanType(deserialize_from="AllowCancelResize")


class ClusterSecurityGroups(Model):
    cluster_security_group_name = StringType(deserialize_from="ClusterSecurityGroupName")
    status = StringType(deserialize_from="Status")


class ClusterVpcSecurityGroups(Model):
    vpc_security_group_id = StringType(deserialize_from="VpcSecurityGroupId")
    status = StringType(deserialize_from="Status")


class ClusterParameterGroupsStatusList(Model):
    parameter_name = StringType(deserialize_from="ParameterName")
    parameter_apply_status = StringType(deserialize_from="ParameterApplyStatus")
    parameter_apply_error_description = StringType(deserialize_from="ParameterApplyErrorDescription")


class ClusterParameterGroups(Model):
    parameter_group_name = StringType(deserialize_from="ParameterGroupName")
    parameter_apply_status = StringType(deserialize_from="ParameterApplyStatus")
    cluster_parameter_status_list = ListType(ModelType(ClusterParameterGroupsStatusList),
                                             deserialize_from="ClusterParameterStatusList")


class ClusterNodes(Model):
    node_role = StringType(deserialize_from="NodeRole")
    private_ip_address = StringType(deserialize_from="PrivateIPAddress")
    public_ip_address = StringType(deserialize_from="PublicIPAddress")


class ClusterIamRoles(Model):
    iam_role_arn = StringType(deserialize_from="IamRoleArn")
    apply_status = StringType(deserialize_from="ApplyStatus")


class ClusterDeferredMaintenanceWindows(Model):
    defer_maintenance_identifier = StringType(deserialize_from="DeferMaintenanceIdentifier")
    defer_maintenance_start_time = DateTimeType(deserialize_from="DeferMaintenanceStartTime")
    defer_maintenance_end_time = DateTimeType(deserialize_from="DeferMaintenanceEndTime")


class Cluster(Model):
    arn = StringType()
    cluster_identifier = StringType(deserialize_from="ClusterIdentifier")
    node_type = StringType(deserialize_from="NodeType")
    cluster_status = StringType(deserialize_from="ClusterStatus")
    cluster_availability_status = StringType(deserialize_from="ClusterAvailabilityStatus")
    modify_status = StringType(deserialize_from="ModifyStatus")
    master_username = StringType(deserialize_from="MasterUsername")
    db_name = StringType(deserialize_from="DBName")
    endpoint = ModelType(Endpoint, deserialize_from="Endpoint")
    cluster_create_time = DateTimeType(deserialize_from="ClusterCreateTime")
    automated_snapshot_retention_period = IntType(deserialize_from="AutomatedSnapshotRetentionPeriod")
    manual_snapshot_retention_period = IntType(deserialize_from="ManualSnapshotRetentionPeriod")
    cluster_security_groups = ListType(ModelType(ClusterSecurityGroups), deserialize_from="ClusterSecurityGroups")
    vpc_security_groups = ListType(ModelType(ClusterVpcSecurityGroups), deserialize_from="VpcSecurityGroups")
    cluster_parameter_groups = ListType(ModelType(ClusterParameterGroups),
                                        deserialize_from="ClusterParameterGroups")
    cluster_subnet_group_name = StringType(deserialize_from="ClusterSubnetGroupName")
    vpc_id = StringType(deserialize_from="VpcId")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow")
    pending_modified_values = ModelType(PendingModifiedValues, deserialize_from="PendingModifiedValues")
    cluster_version = StringType(deserialize_from="ClusterVersion")
    allow_version_upgrade = BooleanType(deserialize_from="AllowVersionUpgrade")
    number_of_nodes = IntType(deserialize_from="NumberOfNodes")
    publicly_accessible = BooleanType(deserialize_from="PubliclyAccessible")
    encrypted = BooleanType(deserialize_from="Encrypted")
    restore_status = ModelType(RestoreStatus, deserialize_from="RestoreStatus")
    data_transfer_progress = ModelType(DataTransferProgress, deserialize_from="DataTransferProgress")
    hsm_status = ModelType(HsmStatus, deserialize_from="HsmStatus")
    cluster_snapshot_copy_status = ModelType(ClusterSnapshotCopyStatus, deserialize_from="ClusterSnapshotCopyStatus")
    cluster_public_key = StringType(deserialize_from="ClusterPublicKey")
    cluster_nodes = ListType(ModelType(ClusterNodes), deserialize_from="ClusterNodes", default=[])
    elastic_ip_status = ModelType(ElasticIpStatus, deserialize_from="ElasticIpStatus")
    cluster_revision_number = StringType(deserialize_from="ClusterRevisionNumber")
    tags = ListType(ModelType(Tags), deserialize_from="Tags", default=[])
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    enhanced_vpc_routing = BooleanType(deserialize_from="EnhancedVpcRouting")
    iam_roles = ListType(ModelType(ClusterIamRoles), deserialize_from="IamRoles")
    pending_actions = ListType(StringType, deserialize_from="PendingActions")
    maintenance_track_name = StringType(deserialize_from="MaintenanceTrackName")
    elastic_resize_number_of_node_options = StringType(deserialize_from="ElasticResizeNumberOfNodeOptions")
    deferred_maintenance_windows = ListType(ModelType(ClusterDeferredMaintenanceWindows),
                                            deserialize_from="DeferredMaintenanceWindows")
    snapshot_schedule_identifier = StringType(deserialize_from="SnapshotScheduleIdentifier")
    snapshot_schedule_state = StringType(deserialize_from="SnapshotScheduleState",
                                         choices=("MODIFYING", "ACTIVE", "FAILED"))
    expected_next_snapshot_schedule_time = DateTimeType(deserialize_from="ExpectedNextSnapshotScheduleTime")
    expected_next_snapshot_schedule_time_status = StringType(deserialize_from="ExpectedNextSnapshotScheduleTimeStatus")
    next_maintenance_window_start_time = DateTimeType(deserialize_from="NextMaintenanceWindowStartTime")
    resize_info = ModelType(ResizeInfo, deserialize_from="ResizeInfo")
    snapshots = ListType(ModelType(Snapshot), default=[])
    snapshot_schedules = ListType(ModelType(SnapshotSchedule))
    scheduled_actions = ListType(ModelType(ScheduledAction))
    account_id = StringType(default="")
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/redshiftv2/home?region={region_code}#cluster-details?cluster={self.cluster_identifier}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/Redshift",
            "dimensions": [CloudWatchDimensionModel({"Name": "ClusterIdentifier", "Value": self.cluster_identifier})],
            "region_name": region_code
        }
