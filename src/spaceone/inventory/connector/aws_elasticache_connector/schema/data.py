import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)

'''
REPLICATION GROUP
'''
class SlotMigration(Model):
    progress_percentage = IntType(deserialize_from="ProgressPercentage")


class Resharding(Model):
    slot_migration = ModelType(SlotMigration,deserialize_from="SlotMigration")


class PendingModifiedValues(Model):
    primary_cluster_id = StringType(deserialize_from="PrimaryClusterId")
    automatic_failover_status = StringType(deserialize_from="AutomaticFailoverStatus",choices=("enabled","disabled"))
    resharding = ModelType(Resharding,deserialize_from="Resharding")
    auth_token_status = StringType(deserialize_from="AuthTokenStatus",choices=("SETTING","ROTATING"))


class PrimaryEndpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")


class ReaderEndpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")


class ConfigurationEndpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")


class NodeGroupMemeberReadEndpoint(Model):
    address = StringType(deserialize_from="Address")
    port = StringType(deserialize_from="Port")


class ReplicationGroupNodeGroupMembers(Model):
    cache_cluster_id = StringType(deserialize_from="CacheClusterId")
    cache_node_id = StringType(deserialize_from="CacheNodeId")
    read_endpoint = ModelType(NodeGroupMemeberReadEndpoint, deserialize_from="ReadEndpoint")
    preferred_availability_zone = StringType(deserialize_from="PreferredAvailabilityZone")
    current_role = StringType(deserialize_from="CurrentRole")


class ReplicationGroupNodeGroups(Model):
    node_group_id = StringType(deserialize_from="NodeGroupId")
    status = StringType(deserialize_from="Status")
    primary_endpoint = ModelType(PrimaryEndpoint, deserialize_from="PrimaryEndpoint")
    reader_endpoint = ModelType(ReaderEndpoint, deserialize_from="ReaderEndpoint")
    slots = StringType(deserialize_from="Slots")
    node_group_members = ListType(ModelType(ReplicationGroupNodeGroupMembers, deserialize_from="NodeGroupMembers"))


class ReplicationGroup(Model):
    replication_group_id = StringType(deserialize_from="ReplicationGroupId")
    description = StringType(deserialize_from="Description")
    status = StringType(deserialize_from="Status")
    pending_modified_values = ModelType(PendingModifiedValues, deserialize_from="PendingModifiedValues")
    member_clusters = ListType(StringType, deserialize_from="MemberClusters")
    node_groups = ListType(ModelType(ReplicationGroupNodeGroups, deserialize_from="NodeGroups"))
    snapshotting_cluster_id = StringType(deserialize_from="SnapshottingClusterId")
    automatic_failover = StringType(deserialize_from="AutomaticFailover",
                                    choices=("enabled", "disabled", "enabling", "disabling"))
    configuration_endpoint = ModelType(ConfigurationEndpoint, deserialize_from="ConfigurationEndpoint")
    snapshot_retention_limit = IntType(deserialize_from="SnapshotRetentionLimit")
    snapshot_window = StringType(deserialize_from="SnapshotWindow")
    cluster_enabled = BooleanType(deserialize_from="ClusterEnabled")
    cache_node_type = StringType(deserialize_from="CacheNodeType")
    auth_token_enabled = BooleanType(deserialize_from="AuthTokenEnabled")
    auth_token_last_modified_date = DateTimeType(deserialize_from="AuthTokenLastModifiedDate")
    transit_encryption_enabled = BooleanType(deserialize_from="TransitEncryptionEnabled")
    at_rest_encryption_enabled = BooleanType(deserialize_from="AtRestEncryptionEnabled")
    kms_key_id = StringType(deserialize_from="KmsKeyId")


'''
CLUSTER
'''
class ConfigurationEndpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")


class PendingModifiedValues(Model):
    num_cache_nodes = IntType(deserialize_from="NumCacheNodes")
    cache_node_ids_to_remove = ListType(StringType,deserialize_from="CacheNodeIdsToRemove")
    engine_version = StringType(deserialize_from="EngineVersion")
    cache_node_type = StringType(deserialize_from="CacheNodeType")
    auth_token_status = StringType(deserialize_from="AuthTokenStatus",choices=("SETTING","ROTATING"))


class NotificationConfiguration(Model):
    topic_arn = StringType(deserialize_from="TopicArn")
    topic_status = StringType(deserialize_from="TopicStatus")


class CacheParameterGroup(Model):
    cache_parameter_group_name = StringType(deserialize_from="CacheParameterGroupName")
    parameter_apply_status = StringType(deserialize_from="ParameterApplyStatus")
    cache_node_ids_to_reboot = ListType(StringType,deserialize_from="CacheNodeIdsToReboot")


class Endpoint(Model):
    address = StringType(deserialize_from="Address")
    port = IntType(deserialize_from="Port")


class ClusterCacheSecurityGroups(Model):
    cache_security_group_name = StringType(deserialize_from="CacheSecurityGroupName")
    status = StringType(deserialize_from="Status")


class ClusterCacheNodes(Model):
    cache_node_id = StringType(deserialize_from="CacheNodeId")
    cache_node_status = StringType(deserialize_from="CacheNodeStatus")
    cache_node_create_time = DateTimeType(deserialize_from="CacheNodeCreateTime")
    endpoint = ModelType(Endpoint,deserialize_from="Endpoint")
    parameter_group_status = StringType(deserialize_from="ParameterGroupStatus")
    source_cache_node_id = StringType(deserialize_from="SourceCacheNodeId")
    customer_availability_zone = StringType(deserialize_from="CustomerAvailabilityZone")


class ClusterSecurityGroups(Model):
    security_group_id = StringType(deserialize_from="SecurityGroupId")
    status = StringType(deserialize_from="Status")


class Cluster(Model):
    cache_cluster_id = StringType(deserialize_from="CacheClusterId")
    configuration_endpoint = ModelType(ConfigurationEndpoint,deserialize_from="ConfigurationEndpoint")
    client_download_landing_page = StringType(deserialize_from="ClientDownloadLandingPage")
    cache_node_type = StringType(deserialize_from="CacheNodeType")
    engine = StringType(deserialize_from="Engine")
    engine_version = StringType(deserialize_from="EngineVersion")
    cache_cluster_status = StringType(deserialize_from="CacheClusterStatus")
    num_cache_nodes = IntType(deserialize_from="NumCacheNodes")
    preferred_availability_zone = StringType(deserialize_from="PreferredAvailabilityZone")
    cache_cluster_create_time = DateTimeType(deserialize_from="CacheClusterCreateTime")
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow")
    pending_modified_values = ModelType(PendingModifiedValues,deserialize_from="PendingModifiedValues")
    notification_configuration = ModelType(NotificationConfiguration,deserialize_from="NotificationConfiguration")
    cache_security_groups = ListType(ModelType(ClusterCacheSecurityGroups,deserialize_from="CacheSecurityGroups"))
    cache_parameter_group = ModelType(CacheParameterGroup,deserialize_from="CacheParameterGroup")
    cache_subnet_group_name = StringType(deserialize_from="CacheSubnetGroupName")
    cache_nodes = ListType(ModelType(ClusterCacheNodes,deserialize_from="CacheNodes"))
    auto_minor_version_upgrade = BooleanType(deserialize_from="AutoMinorVersionUpgrade")
    security_groups = ListType(ModelType(ClusterSecurityGroups,deserialize_from="SecurityGroups"))
    replication_group_id = StringType(deserialize_from="ReplicationGroupId")
    snapshot_retention_limit = IntType(deserialize_from="SnapshotRetentionLimit")
    snapshot_window = StringType(deserialize_from="SnapshotWindow")
    auth_token_enabled = BooleanType(deserialize_from="AuthTokenEnabled")
    auth_token_last_modified_date = DateTimeType(deserialize_from="AuthTokenLastModifiedDate")
    transit_encryption_enabled = BooleanType(deserialize_from="TransitEncryptionEnabled")
    at_rest_encryption_enabled = BooleanType(deserialize_from="AtRestEncryptionEnabled")


class Redis(Model):
    arn = StringType()
    cluster_name = StringType()
    mode = StringType()
    shard_count = IntType()
    node_count = IntType()
    status = StringType()
    primary_endpoint = StringType()
    reader_endpoint = StringType()
    engine = StringType()
    engine_version_compatibility = StringType()
    configuration_endpoint = StringType()
    cluster = ModelType(ReplicationGroup)
    parameter_group = StringType()
    subnet_group = StringType()
    security_groups = ListType(StringType())
    maintenance_window = StringType()
    backup_retention_period = IntType()
    backup_window = StringType()
    backup_node_id = StringType()
    shards = ListType(ModelType(ReplicationGroupNodeGroups))
    nodes = ListType(ModelType(Cluster))
    update_action_status = StringType()
    encryption_in_transit = BooleanType()
    encryption_at_rest = BooleanType()
    auth_enabled = BooleanType()
    auth_token_last_modified_date = DateTimeType()
    availability_zones = ListType(StringType())
    creation_time = DateTimeType()
    region = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/elasticache/home?region={self.region_name}#redis-group-detail:id={self.cluster_name}"
        }


class Memcached(Model):
    arn = StringType()
    cluster_name = StringType()
    node_count = IntType()
    node_type = StringType()
    zone = StringType()
    configuration_endpoint = StringType()
    status = StringType()
    update_status = StringType()
    update_action_status = StringType()
    engine = StringType()
    engine_version_compatibility = StringType()
    availability_zones = ListType(StringType())
    node_pending_deletion = StringType()
    parameter_group = StringType()
    security_groups = ListType(StringType())
    maintenance_window = StringType()
    backup_window = StringType()
    creation_time = DateTimeType()
    number_of_nodes = IntType()
    number_of_nodes_pending_creation = StringType()
    subnet_group = StringType()
    notification_arn = StringType()
    backup_retention_period = StringType()
    cluster = ModelType(Cluster)
    nodes = ListType(ModelType(ClusterCacheNodes))
    region = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/elasticache/home?region={self.reigon}#memcached-nodes:id={self.cluster_name};nodes"
        }
