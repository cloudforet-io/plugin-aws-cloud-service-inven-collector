import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)

'''
TAG
'''
class Tag(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")

'''
SNAPSHOT
'''
class Snapshot(Model):
    availability_zones = ListType(StringType, deserialize_from="AvailabilityZones")
    db_cluster_snapshot_identifier = StringType(deserialize_from="DBClusterSnapshotIdentifier")
    db_cluster_identifier = StringType(deserialize_from="DBClusterIdentifier")
    snapshot_create_time = DateTimeType(deserialize_from="SnapshotCreateTime")
    engine = StringType(deserialize_from="Engine")
    status = StringType(deserialize_from="Status")
    port = IntType(deserialize_from="Port")
    vpc_id = StringType(deserialize_from="VpcId")
    cluster_create_time = DateTimeType(deserialize_from="ClusterCreateTime")
    master_username = StringType(deserialize_from="MasterUsername")
    engine_version = StringType(deserialize_from="EngineVersion")
    snapshot_type = StringType(deserialize_from="SnapshotType")
    percent_progress = IntType(deserialize_from="PercentProgress")
    storage_encrypted = BooleanType(deserialize_from="StorageEncrypted")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    db_cluster_snapshot_arn = StringType(deserialize_from="DBClusterSnapshotArn")
    source_db_cluster_snapshot_arn = StringType(deserialize_from="SourceDBClusterSnapshotArn")
    tags = ListType(ModelType(Tag))

    def reference(self, region_code):
        return {
            "resource_id": self.source_db_cluster_snapshot_arn,
            "external_link": f"https://console.aws.amazon.com/docdb/home?region={region_code}#snapshot-details/{self.db_cluster_snapshot_identifier}"
        }


'''
PARAMETER
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
    apply_method = StringType(deserialize_from="ApplyMethod", choices=("immediate", "pending-reboot"))


'''
PARAMETER GROUP
'''
class ParameterGroup(Model):
    db_cluster_parameter_group_name = StringType(deserialize_from="DBClusterParameterGroupName")
    db_parameter_group_family = StringType(deserialize_from="DBParameterGroupFamily")
    description = StringType(deserialize_from="Description")
    db_cluster_parameter_group_arn = StringType(deserialize_from="DBClusterParameterGroupArn")
    parameters = ListType(ModelType(Parameter))
    account_id = StringType(default="")
    tags = ListType(ModelType(Tag))

    def reference(self, region_code):
        return {
            "resource_id": self.db_cluster_parameter_group_arn,
            "external_link": f"https://console.aws.amazon.com/docdb/home?region={region_code}#parameterGroup-details/{self.db_cluster_parameter_group_name}"
        }


'''
SUBNET GROUP
'''
class SubnetAvailabilityZone(Model):
    name = StringType(deserialize_from="Name")


class SubnetGroupSubnets(Model):
    subnet_identifier = StringType(deserialize_from="SubnetIdentifier")
    subnet_availability_zone = ModelType(SubnetAvailabilityZone, deserialize_from="SubnetAvailabilityZone")
    subnet_status = StringType(deserialize_from="SubnetStatus")


class SubnetGroup(Model):
    db_subnet_group_name = StringType(deserialize_from="DBSubnetGroupName")
    db_subnet_group_description = StringType(deserialize_from="DBSubnetGroupDescription")
    vpc_id = StringType(deserialize_from="VpcId")
    subnet_group_status = StringType(deserialize_from="SubnetGroupStatus")
    subnets = ListType(ModelType(SubnetGroupSubnets), deserialize_from="Subnets")
    db_subnet_group_arn = StringType(deserialize_from="DBSubnetGroupArn")
    account_id = StringType(default='')
    tags = ListType(ModelType(Tag))

    def reference(self, region_code):
        return {
            "resource_id": self.db_subnet_group_arn,
            "external_link": f"https://console.aws.amazon.com/docdb/home?region={region_code}#subnetGroup-details/{self.db_subnet_group_name}"
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
    pending_cloudwatch_logs_exports = ModelType(PendingCloudwatchLogsExports,deserialize_from="PendingCloudwatchLogsExports")


class InstanceVpcSecurityGroups(Model):
    vpc_security_group_id = StringType(deserialize_from="VpcSecurityGroupId")
    status = StringType(deserialize_from="Status")


class InstanceStatusInfos(Model):
    status_type = StringType(deserialize_from="StatusType")
    normal = BooleanType(deserialize_from="Normal")
    status = StringType(deserialize_from="Status")
    message = StringType(deserialize_from="Message")


class Instance(Model):
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier")
    db_instance_class = StringType(deserialize_from="DBInstanceClass")
    engine = StringType(deserialize_from="Engine")
    db_instance_status = StringType(deserialize_from="DBInstanceStatus")
    endpoint = ModelType(Endpoint,deserialize_from="Endpoint")
    instance_create_time = DateTimeType(deserialize_from="InstanceCreateTime")
    preferred_backup_window = StringType(deserialize_from="PreferredBackupWindow")
    backup_retention_period = IntType(deserialize_from="BackupRetentionPeriod")
    vpc_security_groups = ListType(ModelType(InstanceVpcSecurityGroups), deserialize_from="VpcSecurityGroups")
    availability_zone = StringType(deserialize_from="AvailabilityZone")
    db_subnet_group = ModelType(DBSubnetGroup,deserialize_from="DBSubnetGroup")
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow")
    pending_modified_values = ModelType(PendingModifiedValues,deserialize_from="PendingModifiedValues")
    latest_restorable_time = DateTimeType(deserialize_from="LatestRestorableTime")
    engine_version = StringType(deserialize_from="EngineVersion")
    auto_minor_version_upgrade = BooleanType(deserialize_from="AutoMinorVersionUpgrade")
    publicly_accessible = BooleanType(deserialize_from="PubliclyAccessible")
    status_infos = ListType(ModelType(InstanceStatusInfos), deserialize_from="StatusInfos")
    db_cluster_identifier = StringType(deserialize_from="DBClusterIdentifier")
    storage_encrypted = BooleanType(deserialize_from="StorageEncrypted")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    dbi_resource_id = StringType(deserialize_from="DbiResourceId")
    ca_certificate_identifier = StringType(deserialize_from="CACertificateIdentifier")
    promotion_tier = IntType(deserialize_from="PromotionTier")
    db_instance_arn = StringType(deserialize_from="DBInstanceArn")
    enabled_cloudwatch_logs_exports = ListType(StringType, deserialize_from="EnabledCloudwatchLogsExports")
    tags = ListType(ModelType(Tag))
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.db_instance_arn,
            "external_link": f"https://console.aws.amazon.com/docdb/home?region={region_code}#instance-details/{self.db_instance_identifier}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/DocDB",
            "dimensions": [CloudWatchDimensionModel({'Name': 'DBInstanceIdentifier', 'Value': self.db_instance_identifier})],
            "region_name": region_code
        }


'''
DB CLUSTER
'''
class ClusterDBClusterMembers(Model):
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier")
    is_cluster_writer = BooleanType(deserialize_from="IsClusterWriter")
    db_cluster_parameter_group_status = StringType(deserialize_from="DBClusterParameterGroupStatus")
    promotion_tier = IntType(deserialize_from="PromotionTier")


class ClusterVpcSecurityGroups(Model):
    vpc_security_group_id = StringType(deserialize_from="VpcSecurityGroupId")
    status = StringType(deserialize_from="Status")


class ClusterAssociatedRoles(Model):
    role_arn = StringType(deserialize_from="RoleArn")
    status = StringType(deserialize_from="Status")


class Cluster(Model):
    availability_zones = ListType(StringType, deserialize_from="AvailabilityZones")
    backup_retention_period = IntType(deserialize_from="BackupRetentionPeriod")
    db_cluster_identifier = StringType(deserialize_from="DBClusterIdentifier")
    db_cluster_parameter_group = StringType(deserialize_from="DBClusterParameterGroup")
    parameter_group = ModelType(ParameterGroup)
    db_subnet_group = StringType(deserialize_from="DBSubnetGroup")
    subnet_group = ModelType(SubnetGroup)
    status = StringType(deserialize_from="Status")
    percent_progress = StringType(deserialize_from="PercentProgress")
    earliest_restorable_time = DateTimeType(deserialize_from="EarliestRestorableTime")
    endpoint = StringType(deserialize_from="Endpoint")
    reader_endpoint = StringType(deserialize_from="ReaderEndpoint")
    multi_az = BooleanType(deserialize_from="MultiAZ")
    engine = StringType(deserialize_from="Engine")
    engine_version = StringType(deserialize_from="EngineVersion")
    latest_restorable_time = DateTimeType(deserialize_from="LatestRestorableTime")
    port = IntType(deserialize_from="Port")
    master_username = StringType(deserialize_from="MasterUsername")
    preferred_backup_window = StringType(deserialize_from="PreferredBackupWindow")
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow")
    db_cluster_members = ListType(ModelType(ClusterDBClusterMembers), deserialize_from="DBClusterMembers")
    instance_count = IntType(default=0)
    vpc_security_groups = ListType(ModelType(ClusterVpcSecurityGroups), deserialize_from="VpcSecurityGroups")
    hosted_zone_id = StringType(deserialize_from="HostedZoneId")
    storage_encrypted = BooleanType(deserialize_from="StorageEncrypted")
    kms_key_id = StringType(deserialize_from="KmsKeyId")
    db_cluster_resource_id = StringType(deserialize_from="DbClusterResourceId")
    db_cluster_arn = StringType(deserialize_from="DBClusterArn")
    associated_roles = ListType(ModelType(ClusterAssociatedRoles), deserialize_from="AssociatedRoles")
    cluster_create_time = DateTimeType(deserialize_from="ClusterCreateTime")
    enabled_cloudwatch_logs_exports = ListType(StringType, deserialize_from="EnabledCloudwatchLogsExports")
    deletion_protection = BooleanType(deserialize_from="DeletionProtection")
    instances = ListType(ModelType(Instance))
    snapshots = ListType(ModelType(Snapshot))
    account_id = StringType(default='')
    tags = ListType(ModelType(Tag))
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.db_cluster_arn,
            "external_link": f"https://console.aws.amazon.com/docdb/home?region={region_code}#cluster-details/{self.db_cluster_identifier}"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/DocDB",
            "dimensions": [CloudWatchDimensionModel({'Name': 'DBClusterIdentifier', 'Value': self.db_cluster_identifier})],
            "region_name": region_code
        }
