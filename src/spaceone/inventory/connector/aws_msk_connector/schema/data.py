import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, FloatType, DateTimeType, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType()
    value = StringType()


class EbsStorageInfo(Model):
    volume_size = IntType(deserialize_from="VolumeSize")


class StateInfo(Model):
    ebs_storage_info = ModelType(EbsStorageInfo, deserialize_from="EbsStorageInfo")


class BrokerNodeGroupInfo(Model):
    broker_az_distribution = StringType(deserialize_from="BrokerNodeGroupInfo", default="DEFAULT")
    client_subnets = ListType(StringType, deserialize_from="ClientSubnets")
    instance_type = StringType(deserialize_from="InstanceType")
    security_group = ListType(StringType, deserialize_from="SecurityGroups")
    storage_info = ModelType(StateInfo, deserialize_from="StorageInfo")


class Scram(Model):
    enabled = BooleanType(deserialize_from="Enabled")


class Sasl(Model):
    scram = ModelType(Scram, deserialize_from="Sasl")


class Tls(Model):
    certificate_authority_arn_list = ListType(StringType, deserialize_from="CertificateAuthorityArnList")


class ClientAuthentication(Model):
    sasl = ModelType(Sasl, deserialize_from="Sasl")
    tls = ModelType(Tls, deserialize_from="Tls")


class CurrentBrokerSoftwareInfo(Model):
    configuration_arn = StringType(deserialize_from="ConfigurationArn")
    configuration_revision = IntType(deserialize_from="ConfigurationRevision")
    kafka_version = StringType(deserialize_from="KafkaVersion")


class EncryptionInTransit(Model):
    client_broker = StringType(deserialize_from="ClientBroker", choices=('TLS','TLS_PLAINTEXT','PLAINTEXT'))
    in_cluster = BooleanType(deserialize_from="InCluster")


class EncryptionAtRest(Model):
    data_volume_kms_key_id = StringType(deserialize_from="DataVolumeKMSKeyId")


class EncryptionInfo(Model):
    encryption_at_rest = ModelType(EncryptionAtRest, deserialize_from="EncryptionAtRest")
    encryption_in_transit = ModelType(EncryptionInTransit, deserialize_from="EncryptionInTransit")


class JmxExporter(Model):
    enabled_in_broker = BooleanType(deserialize_from="EnabledInBroker")


class NodeExporter(Model):
    enabled_in_broker = BooleanType(deserialize_from="EnabledInBroker")


class Prometheus(Model):
    jmx_exporter = ModelType(JmxExporter, deserialize_from="EnabledInBroker")
    node_exporter = ModelType(NodeExporter, deserialize_from="EnabledInBroker")


class OpenMonitoring(Model):
    prometheus = ModelType(Prometheus, deserialize_from="Prometheus")


class CloudWatchLogs(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    log_group = StringType(deserialize_from="LogGroup")


class BrokerLogs(Model):
    cloud_watch_logs = ModelType(CloudWatchLogs, deserialize_from="CloudWatchLogs")


class Firehose(Model):
    delivery_stream = StringType(deserialize_from="DeliveryStream")
    enabled = BooleanType(deserialize_from="Enabled")

class S3(Model):
    bucket = StringType(deserialize_from="Bucket")
    enabled = BooleanType(deserialize_from="Enabled")
    prefix = StringType(deserialize_from="Prefix")

class LoggingInfo(Model):
    broker_logs = ModelType(BrokerLogs, deserialize_from="BrokerLogs")
    firehose = ModelType(Firehose, deserialize_from="Firehose")
    s3 = ModelType(S3, deserialize_from="S3")

class StateInfo(Model):
    code = StringType(deserialize_from="Code")
    message = StringType(deserialize_from="Message")

'''
    LIST_CLUSTER_OPERATIONS()
'''


class MskCluster(Model):
    active_operation_arn = StringType(deserialize_from="ActiveOperationArn")
    broker_node_group_info = ModelType(BrokerNodeGroupInfo, deserialize_from="BrokerNodeGroupInfo")
    client_authentication = ModelType(ClientAuthentication, deserialize_from="ClientAuthentication")
    cluster_arn = StringType(deserialize_from='ClusterArn')
    cluster_name = StringType(deserialize_from='ClusterName')
    creation_time = DateTimeType(deserialize_from='CreationTime')
    current_broker_software_info = ModelType(CurrentBrokerSoftwareInfo, deserialize_from='CurrentBrokerSoftwareInfo')
    current_version = StringType(deserialize_from='CurrentVersion')
    encryption_info = ModelType(EncryptionInfo, deserialize_from='EncryptionInfo')
    enhanced_monitoring = StringType(deserialize_from='EnhancedMonitoring',
                                     choices=('DEFAULT','PER_BROKER','PER_TOPIC_PER_BROKER','PER_TOPIC_PER_PARTITION'))
    open_monitoring = ModelType(OpenMonitoring, deserialize_from='OpenMonitoring')
    logging_info = ModelType(LoggingInfo, deserialize_from='LoggingInfo')
    number_of_broker_nodes = IntType(deserialize_from='NumberOfBrokerNodes')
    state = StringType(deserialize_from='State',
                       choices=('ACTIVE','CREATING','DELETING','FAILED',
                                'HEALING','MAINTENANCE','REBOOTING_BROKER','UPDATING'))
    state_info = ModelType(StateInfo, deserialize_from='StateInfo')
    tags = ListType(ModelType(Tags), deserialize_from='Tags', default=[])
    zookeeper_connect_string = StringType(deserialize_from='ZookeeperConnectString')
    zookeeper_connect_string_tls = StringType(deserialize_from='ZookeeperConnectStringTls')


class BrokerNodeInfo(Model):
    attached_eni_id = StringType(deserialize_from='AttachedENIId')
    broker_id = FloatType(deserialize_from='BrokerId')
    client_subnet = StringType(deserialize_from='ClientSubnet')
    client_vpc_ip_address = StringType(deserialize_from='ClientVpcIpAddress')
    current_broker_software_info = ModelType(CurrentBrokerSoftwareInfo, deserialize_from='CurrentBrokerSoftwareInfo')
    endpoints = ListType(StringType, deserialize_from='Endpoints')


class ZookeeperNodeInfo(Model):
    attached_eni_id = StringType(deserialize_from='AttachedENIId')
    client_vpc_ip_address = StringType(deserialize_from='ClientVpcIpAddress')
    endpoints = ListType(StringType, deserialize_from='Endpoints')
    zookeeper_id = FloatType(deserialize_from='ZookeeperId')
    zookeeper_version = StringType(deserialize_from='ZookeeperVersion')


class NodeInfo(Model):
    added_to_cluster_time = StringType(deserialize_from='AddedToClusterTime')
    broker_node_info = ModelType(BrokerNodeInfo, deserialize_from='BrokerNodeInfo')
    instance_type = StringType(deserialize_from='InstanceType')
    node_arn = StringType(deserialize_from='NodeARN')
    node_type = StringType(deserialize_from='NodeType')
    zookeeper_node_info = ModelType(ZookeeperNodeInfo, deserialize_from='ZookeeperNodeInfo')


class ClusterInfoList(Model):
    cluster_info_list = ListType(ModelType(MskCluster), deserialize_from='ClusterInfoList', default= [])


class LatestRevision(Model):
    creation_time = DateTimeType(deserialize_from='CreationTime')
    description = StringType(deserialize_from='Description')
    revision = IntType(deserialize_from='Revision')


class Configurations(Model):
    arn = StringType(deserialize_from='Arn')
    creation_time = DateTimeType(deserialize_from='CreationTime')
    description = StringType('Description')
    kafka_versions = ListType(StringType, deserialize_from='KafkaVersions')
    latest_revision = ModelType(LatestRevision, deserialize_from='LatestRevision')
    name = StringType(deserialize_from='Name')
    state = StringType(deserialize_from='State', choices=('ACTIVE','DELETING','DELETE_FAILED'))


class ListConfigurations(Model):
    configurations = ListType(ModelType(Configurations), deserialize_from='Configurations', default=[])


class GetBootStrapBrokers(Model):
    bootstrap_broker_string = StringType(deserialize_from='BootstrapBrokerString')
    bootstrap_broker_tls = StringType(deserialize_from='BootstrapBrokerStringTls')
    bootstrap_broker_string_sasl_scram = StringType(deserialize_from='BootstrapBrokerStringSaslScram')


class ListConfigurationRevisions(Model):
    revisions = ListType(ModelType(LatestRevision), deserialize_from='Revisions')


class DescribeConfigurationRevision(Model):
    arn = StringType(deserialize_from='Arn')
    creation_time = DateTimeType(deserialize_from='CreationTime')
    description = StringType(deserialize_from='Description')
    revision = IntType(deserialize_from='Revision')
    server_properties = ListType(StringType())


class ErrorInfo(Model):
    error_code = StringType(deserialize_from='ErrorCode')
    error_string = StringType(deserialize_from='ErrorString')


class ClusterOperation(Model):
    cluster_arn = StringType(deserialize_from='ClusterArn')
    creation_time = DateTimeType(deserialize_from='CreationTime')
    end_time = DateTimeType(deserialize_from='EndTime')
    error_info = ModelType(ErrorInfo, deserialize_from='ErrorInfo')
    operation_arn = StringType(deserialize_from='OperationArn')
    operation_type = StringType(deserialize_from='OperationType')


class Cluster(Model):
    active_operation_arn = StringType(deserialize_from="ActiveOperationArn", serialize_when_none=False)
    broker_node_group_info = ModelType(BrokerNodeGroupInfo, deserialize_from="BrokerNodeGroupInfo")
    client_authentication = ModelType(ClientAuthentication, deserialize_from="ClientAuthentication")
    cluster_arn = StringType(deserialize_from='ClusterArn')
    cluster_name = StringType(deserialize_from='ClusterName')
    creation_time = DateTimeType(deserialize_from='CreationTime')
    current_broker_software_info = ModelType(CurrentBrokerSoftwareInfo, deserialize_from='CurrentBrokerSoftwareInfo')
    current_version = StringType(deserialize_from='CurrentVersion')
    encryption_info = ModelType(EncryptionInfo, deserialize_from='EncryptionInfo')
    enhanced_monitoring = StringType(deserialize_from='EnhancedMonitoring',
                                     choices=(
                                     'DEFAULT', 'PER_BROKER', 'PER_TOPIC_PER_BROKER', 'PER_TOPIC_PER_PARTITION'))
    open_monitoring = ModelType(OpenMonitoring, deserialize_from='OpenMonitoring')
    logging_info = ModelType(LoggingInfo, deserialize_from='LoggingInfo')
    number_of_broker_nodes = IntType(deserialize_from='NumberOfBrokerNodes')
    state = StringType(deserialize_from='State',
                       choices=('ACTIVE', 'CREATING', 'DELETING', 'FAILED',
                                'HEALING', 'MAINTENANCE', 'REBOOTING_BROKER', 'UPDATING'))
    state_info = ModelType(StateInfo, deserialize_from='StateInfo')
    tags = ListType(ModelType(Tags), deserialize_from='Tags', default=[])
    zookeeper_connect_string = StringType(deserialize_from='ZookeeperConnectString')
    zookeeper_connect_string_tls = StringType(deserialize_from='ZookeeperConnectStringTls')
    # Broker Node Infomation
    node_info_list = ListType(ModelType(NodeInfo), default=[])
    # Cluster Operation Info List
    cluster_operation_info = ListType(ModelType(ClusterOperation), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.cluster_arn,
            "external_link": f"https://console.aws.amazon.com/msk/home?region={region_code}#/cluster/{self.cluster_arn}/view?tabId=details"
        }


class Configuration(Model):
    arn = StringType(deserialize_from='Arn')
    creation_time = DateTimeType(deserialize_from='CreationTime')
    description = StringType(deserialize_from='Description')
    kafka_versions = ListType(StringType, deserialize_from='KafkaVersions')
    latest_revision = ModelType(LatestRevision, deserialize_from='LatestRevision')
    name = StringType(deserialize_from='Name')
    state = StringType(deserialize_from='State', choices=('ACTIVE', 'DELETING', 'DELETE_FAILED'))
    revisions_configurations = ListType(ModelType(DescribeConfigurationRevision))

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/msk/home?region={region_code}#/configuration/{self.arn}/view"
        }

