import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, FloatType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


class Endpoint(Model):
    address = StringType(deserialize_from='Address', serialize_when_none=False)
    port = IntType(deserialize_from='Port', serialize_when_none=False)


class NotificationConfiguration(Model):
    topic_arn = StringType(deserialize_from='TopicArn', serialize_when_none=False)
    topic_status = StringType(deserialize_from='TopicStatus', serialize_when_none=False)


class CacheParameterGroup(Model):
    cache_parameter_group_name = StringType(deserialize_from='CacheParameterGroupName', serialize_when_none=False)
    parameter_apply_status = StringType(deserialize_from='ParameterApplyStatus', serialize_when_none=False)
    cache_node_ids_to_reboot = ListType(StringType, deserialize_from='CacheNodeIdsToReboot', default=[])


class NodeGroupMembers(Model):
    cache_cluster_id = StringType(deserialize_from='CacheClusterId', serialize_when_none=False)
    cache_node_id = StringType(deserialize_from='CacheNodeId', serialize_when_none=False)
    read_endpoint = ModelType(Endpoint, deserialize_from='ReadEndpoint', serialize_when_none=False)
    preferred_availability_zone = StringType(deserialize_from='PreferredAvailabilityZone', serialize_when_none=False)
    preferred_outpost_arn = StringType(deserialize_from='PreferredOutpostArn', serialize_when_none=False)
    current_role = StringType(deserialize_from='CurrentRole', serialize_when_none=False)


class NodeGroups(Model):
    node_group_id = StringType(deserialize_from='NodeGroupId', serialize_when_none=False)
    status = StringType(deserialize_from='Status', serialize_when_none=False)
    primary_endpoint = ModelType(Endpoint, deserialize_from='PrimaryEndpoint', serialize_when_none=False)
    reader_endpoint = ModelType(Endpoint, deserialize_from='ReaderEndpoint', serialize_when_none=False)
    slots = StringType(deserialize_from='Slots', serialize_when_none=False)
    node_group_members = ListType(ModelType(NodeGroupMembers), deserialize_from='NodeGroupMembers', default=[])


class UserGroups(Model):
    user_group_ids_to_add = ListType(StringType, deserialize_from='UserGroupIdsToAdd', default=[])
    user_group_ids_to_remove = ListType(StringType, deserialize_from='UserGroupIdsToRemove', default=[])


class ReshardingSlotMigration(Model):
    progress_percentage = FloatType(deserialize_from='ProgressPercentage', serialize_when_none=False)


class Resharding(Model):
    slot_migration = ModelType(ReshardingSlotMigration, deserialize_from='SlotMigration', serialize_when_none=False)


class PendingModifiedValues(Model):
    primary_cluster_id = StringType(deserialize_from='PrimaryClusterId', serialize_when_none=False)
    automatic_failover_status = StringType(deserialize_from='AutomaticFailoverStatus', choices=('enabled', 'disabled'),
                                           serialize_when_none=False)
    resharding = ModelType(Resharding, deserialize_from='Resharding', serialize_when_none=False)
    auth_token_status = StringType(deserialize_from='AuthTokenStatus', choices=('SETTING', 'ROTATING'),
                                   serialize_when_none=False)
    user_groups = ModelType(UserGroups, deserialize_from='UserGroups', serialize_when_none=False)


class GlobalReplicationGroupInfo(Model):
    global_replication_group_id = StringType(deserialize_from='GlobalReplicationGroupId', serialize_when_none=False)
    global_replication_group_member_role = StringType(deserialize_from='GlobalReplicationGroupMemberRole',
                                                      serialize_when_none=False)


class CacheSecurityGroups(Model):
    cache_security_group_name = StringType(deserialize_from="CacheSecurityGroupName")
    status = StringType(deserialize_from="Status")


class SecurityGroups(Model):
    security_group_id = StringType(deserialize_from="SecurityGroupId")
    status = StringType(deserialize_from="Status")


class MemcachedNode(Model):
    node_name = StringType()
    status = StringType()
    port = IntType()
    endpoint = StringType()
    parameter_group_status = StringType()
    # availability_zone = StringType()
    created_on = DateTimeType()


class MemcachedPendingModifiedValues(Model):
    num_cache_nodes = IntType(deserialize_from='NumCacheNodes', serialize_when_none=False)
    cache_node_ids_to_remove = ListType(StringType, deserialize_from='CacheNodeIdsToRemove', default=[])
    engine_version = StringType(deserialize_from='EngineVersion', serialize_when_none=False)
    cache_node_type = StringType(deserialize_from='CacheNodeType', serialize_when_none=False)
    auth_token_status = StringType(deserialize_from='AuthTokenStatus', choices=('SETTING', 'ROTATING'),
                                   serialize_when_none=False)


class Shard(Model):
    shard_name = StringType()
    nodes = IntType()
    status = StringType()
    slots = StringType()


class Node(Model):
    node_name = StringType()
    status = StringType()
    current_role = StringType(serialize_when_none=False)
    port = IntType()
    endpoint = StringType()
    arn = StringType()
    parameter_group_status = StringType()
    zone = StringType()
    created_on = DateTimeType()


class Valkey(AWSCloudService):
    arn = StringType(deserialize_from='ARN', serialize_when_none=False)
    replication_group_id = StringType(deserialize_from="ReplicationGroupId", serialize_when_none=False)
    mode = StringType(choices=('Clustered Valkey', 'Valkey'))
    engine = StringType(deserialize_from="Engine", serialize_when_none=False)
    engine_version = StringType(deserialize_from="EngineVersion", serialize_when_none=False)
    shard_count = IntType()
    node_count = IntType()
    cache_node_type = StringType(deserialize_from="CacheNodeType", serialize_when_none=False)
    description = StringType(deserialize_from="Description", serialize_when_none=False)
    global_replication_group_info = ModelType(GlobalReplicationGroupInfo,
                                              deserialize_from="GlobalReplicationGroupInfo", serialize_when_none=False)
    status = StringType(deserialize_from='Status')
    pending_modified_values = ModelType(PendingModifiedValues, deserialize_from='PendingModifiedValues',
                                        serialize_when_none=False)
    member_clusters = ListType(StringType, deserialize_from='MemberClusters', default=[])
    node_groups = ListType(ModelType(NodeGroups), deserialize_from='NodeGroups', default=[])
    availability_zones = ListType(StringType, default=[])
    snapshotting_cluster_id = StringType(deserialize_from='SnapshottingClusterId', serialize_when_none=False)
    automatic_failover = StringType(deserialize_from='AutomaticFailover',
                                    choices=('enabled', 'disabled', 'enabling', 'disabling'),
                                    serialize_when_none=False)
    parameter_group_name = StringType(serialize_when_none=False)
    subnet_group_name = StringType(serialize_when_none=False)
    multi_az = StringType(deserialize_from='MultiAZ', choices=('enabled', 'disabled'), serialize_when_none=False)
    configuration_endpoint = ModelType(Endpoint, deserialize_from='ConfigurationEndpoint', serialize_when_none=False)
    primary_endpoint = StringType(serialize_when_none=False)
    reader_endpoint = StringType(serialize_when_none=False)
    snapshot_retention_limit = IntType(deserialize_from='SnapshotRetentionLimit', serialize_when_none=False)
    snapshot_window = StringType(deserialize_from='SnapshotWindow', serialize_when_none=False)
    cluster_enabled = BooleanType(deserialize_from='ClusterEnabled', serialize_when_none=False)
    cluster_node_type = StringType(deserialize_from='CacheNodeType', serialize_when_none=False)
    auth_token_enabled = BooleanType(deserialize_from='AuthTokenEnabled', serialize_when_none=False)
    auth_token_last_modified_date = DateTimeType(deserialize_from='AuthTokenLastModifiedDate', serialize_when_none=False)
    transit_encryption_enabled = BooleanType(deserialize_from='TransitEncryptionEnabled', serialize_when_none=False)
    at_rest_encryption_enabled = BooleanType(deserialize_from='AtRestEncryptionEnabled', serialize_when_none=False)
    member_clusters_outpost_arns = ListType(StringType, deserialize_from='MemberClustersOutpostArns', default=[])
    kms_key_id = StringType(deserialize_from='KmsKeyId', serialize_when_none=False)
    user_group_ids = ListType(StringType, deserialize_from='UserGroupIds', default=[])
    shards = ListType(ModelType(Shard), default=[])
    nodes = ListType(ModelType(Node), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/elasticache/home?region={region_code}#redis-group-detail:id={self.replication_group_id}"
        }


class Redis(AWSCloudService):
    arn = StringType(deserialize_from='ARN', serialize_when_none=False)
    replication_group_id = StringType(deserialize_from="ReplicationGroupId", serialize_when_none=False)
    mode = StringType(choices=('Clustered Redis', 'Redis'))
    engine = StringType(deserialize_from="Engine", serialize_when_none=False)
    engine_version = StringType(deserialize_from="EngineVersion", serialize_when_none=False)
    shard_count = IntType()
    node_count = IntType()
    cache_node_type = StringType(deserialize_from="CacheNodeType", serialize_when_none=False)
    description = StringType(deserialize_from="Description", serialize_when_none=False)
    global_replication_group_info = ModelType(GlobalReplicationGroupInfo,
                                              deserialize_from="GlobalReplicationGroupInfo", serialize_when_none=False)
    status = StringType(deserialize_from='Status')
    pending_modified_values = ModelType(PendingModifiedValues, deserialize_from='PendingModifiedValues',
                                        serialize_when_none=False)
    member_clusters = ListType(StringType, deserialize_from='MemberClusters', default=[])
    node_groups = ListType(ModelType(NodeGroups), deserialize_from='NodeGroups', default=[])
    availability_zones = ListType(StringType, default=[])
    snapshotting_cluster_id = StringType(deserialize_from='SnapshottingClusterId', serialize_when_none=False)
    automatic_failover = StringType(deserialize_from='AutomaticFailover',
                                    choices=('enabled', 'disabled', 'enabling', 'disabling'),
                                    serialize_when_none=False)
    parameter_group_name = StringType(serialize_when_none=False)
    subnet_group_name = StringType(serialize_when_none=False)
    multi_az = StringType(deserialize_from='MultiAZ', choices=('enabled', 'disabled'), serialize_when_none=False)
    configuration_endpoint = ModelType(Endpoint, deserialize_from='ConfigurationEndpoint', serialize_when_none=False)
    primary_endpoint = StringType(serialize_when_none=False)
    reader_endpoint = StringType(serialize_when_none=False)
    snapshot_retention_limit = IntType(deserialize_from='SnapshotRetentionLimit', serialize_when_none=False)
    snapshot_window = StringType(deserialize_from='SnapshotWindow', serialize_when_none=False)
    cluster_enabled = BooleanType(deserialize_from='ClusterEnabled', serialize_when_none=False)
    cluster_node_type = StringType(deserialize_from='CacheNodeType', serialize_when_none=False)
    auth_token_enabled = BooleanType(deserialize_from='AuthTokenEnabled', serialize_when_none=False)
    auth_token_last_modified_date = DateTimeType(deserialize_from='AuthTokenLastModifiedDate', serialize_when_none=False)
    transit_encryption_enabled = BooleanType(deserialize_from='TransitEncryptionEnabled', serialize_when_none=False)
    at_rest_encryption_enabled = BooleanType(deserialize_from='AtRestEncryptionEnabled', serialize_when_none=False)
    member_clusters_outpost_arns = ListType(StringType, deserialize_from='MemberClustersOutpostArns', default=[])
    kms_key_id = StringType(deserialize_from='KmsKeyId', serialize_when_none=False)
    user_group_ids = ListType(StringType, deserialize_from='UserGroupIds', default=[])
    shards = ListType(ModelType(Shard), default=[])
    nodes = ListType(ModelType(Node), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/elasticache/home?region={region_code}#redis-group-detail:id={self.replication_group_id}"
        }


class Memcached(AWSCloudService):
    arn = StringType(deserialize_from='ARN')
    cache_cluster_id = StringType(deserialize_from="CacheClusterId", serialize_when_none=False)
    configuration_endpoint = ModelType(Endpoint, deserialize_from="ConfigurationEndpoint", serialize_when_none=False)
    configuration_endpoint_display = StringType(default='')
    client_download_landing_page = StringType(deserialize_from="ClientDownloadLandingPage",
                                              serialize_when_none=False)
    cache_node_type = StringType(deserialize_from="CacheNodeType", serialize_when_none=False)
    engine = StringType(deserialize_from="Engine", serialize_when_none=False)
    engine_version = StringType(deserialize_from="EngineVersion", serialize_when_none=False)
    cache_cluster_status = StringType(deserialize_from="CacheClusterStatus", serialize_when_none=False)
    num_cache_nodes = IntType(deserialize_from="NumCacheNodes", serialize_when_none=False)
    preferred_availability_zone = StringType(deserialize_from="PreferredAvailabilityZone", serialize_when_none=False)
    cache_cluster_create_time = DateTimeType(deserialize_from="CacheClusterCreateTime", serialize_when_none=False)
    preferred_maintenance_window = StringType(deserialize_from="PreferredMaintenanceWindow", serialize_when_none=False)
    pending_modified_values = ModelType(MemcachedPendingModifiedValues, deserialize_from="PendingModifiedValues",
                                        serialize_when_none=False)
    notification_configuration = ModelType(NotificationConfiguration, deserialize_from="NotificationConfiguration",
                                           serialize_when_none=False)
    cache_security_groups = ListType(ModelType(CacheSecurityGroups),
                                     deserialize_from="CacheSecurityGroups", default=[])
    cache_parameter_group = ModelType(CacheParameterGroup,
                                      deserialize_from="CacheParameterGroup", serialize_when_none=False)
    cache_subnet_group_name = StringType(deserialize_from="CacheSubnetGroupName", serialize_when_none=False)
    auto_minor_version_upgrade = BooleanType(deserialize_from="AutoMinorVersionUpgrade", serialize_when_none=False)
    security_groups = ListType(ModelType(SecurityGroups),
                               deserialize_from="SecurityGroups", default=[])
    replication_group_id = StringType(deserialize_from="ReplicationGroupId", serialize_when_none=False)
    snapshot_retention_limit = IntType(deserialize_from="SnapshotRetentionLimit", serialize_when_none=False)
    snapshot_window = StringType(deserialize_from="SnapshotWindow", serialize_when_none=False)
    auth_token_enabled = BooleanType(deserialize_from="AuthTokenEnabled", serialize_when_none=False)
    auth_token_last_modified_date = DateTimeType(deserialize_from="AuthTokenLastModifiedDate",
                                                 serialize_when_none=False)
    transit_encryption_enabled = BooleanType(deserialize_from="TransitEncryptionEnabled",
                                             serialize_when_none=False)
    at_rest_encryption_enabled = BooleanType(deserialize_from="AtRestEncryptionEnabled",
                                             serialize_when_none=False)
    nodes = ListType(ModelType(MemcachedNode), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/elasticache/home?region={region_code}#memcached-nodes:id={self.cache_cluster_id}"
        }
