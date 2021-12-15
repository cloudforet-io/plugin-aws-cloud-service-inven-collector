import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, \
    BooleanType, FloatType

_LOGGER = logging.getLogger(__name__)


# list_tags_for_delivery_stream()
class Tags(Model):
    key = StringType(deserialize_from='Key')
    value = StringType(deserialize_from='Value')
    has_more_tags = BooleanType(deserialize_from='HasMoreTags')


# describe_delivery_stream()
class FailureDescription(Model):
    type = StringType(deserialize_from='Type', choices=(
        'RETIRE_KMS_GRANT_FAILED', 'CREATE_KMS_GRANT_FAILED', 'KMS_ACCESS_DENIED', 'DISABLED_KMS_KEY',
        'INVALID_KMS_KEY',
        'KMS_KEY_NOT_FOUND', 'KMS_OPT_IN_REQUIRED', 'CREATE_ENI_FAILED', 'DELETE_ENI_FAILED', 'SUBNET_NOT_FOUND',
        'SECURITY_GROUP_NOT_FOUND', 'ENI_ACCESS_DENIED', 'SUBNET_ACCESS_DENIED', 'SECURITY_GROUP_ACCESS_DENIED',
        'UNKNOWN_ERROR'), serialize_when_none=False)
    details = StringType(deserialize_from='Details', serialize_when_none=False)


class DeliveryStreamEncryptionConfiguration(Model):
    key_arn = StringType(deserialize_from='KeyARN', serialize_when_none=False)
    key_type = StringType(deserialize_from='KeyType', choices=('AWS_OWNED_CMK', 'CUSTOMER_MANAGED_CMK'),
                          serialize_when_none=False)
    status = StringType(deserialize_from='Status',
                        choices=('ENABLED', 'ENABLING', 'ENABLING_FAILED', 'DISABLED', 'DISABLING', 'DISABLING_FAILED'))
    failure_description = ModelType(FailureDescription, deserialize_from="FailureDescription",
                                    serialize_when_none=False)


class KinesisStreamSourceDescription(Model):
    kinesis_stream_arn = StringType(deserialize_from='KinesisStreamARN', serialize_when_none=False)
    role_arn = StringType(deserialize_from='RoleARN', serialize_when_none=False)
    delivery_start_timestamp = DateTimeType(deserialize_from='DeliveryStartTimestamp', serialize_when_none=False)


class KMSEncryptionConfig(Model):
    aws_kms_key_arn = StringType(deserialize_from="AWSKMSKeyARN", serialize_when_none=False)


class EncryptionConfiguration(Model):
    no_encryption_config = StringType(deserialize_from="NoEncryptionConfig", serialize_when_none=False)
    kms_encryption_config = ModelType(KMSEncryptionConfig, deserialize_from="KMSEncryptionConfig",
                                      serialize_when_none=False)


class CloudWatchLoggingOptions(Model):
    enabled = BooleanType(deserialize_from='Enabled', serialize_when_none=False)
    log_group_name = StringType(deserialize_from='LogGroupName', serialize_when_none=False)
    log_stream_name = StringType(deserialize_from='LogStreamName', serialize_when_none=False)


class BufferingHints(Model):
    size_in_mbs = IntType(deserialize_from='SizeInMBs', serialize_when_none=False)
    interval_in_seconds = IntType(deserialize_from='IntervalInSeconds', serialize_when_none=False)


class Parameters(Model):
    parameter_name = StringType(deserialize_from='ParameterName', choices=(
        'LambdaArn', 'NumberOfRetries', 'RoleArn', 'BufferSizeInMBs', 'BufferIntervalInSeconds'),
                                serialize_when_none=False)
    parameter_value = StringType(deserialize_from='ParameterValue', serialize_when_none=False)


class Processors(Model):
    type = StringType(deserialize_from='Type', serialize_when_none=False)
    parameters = ListType(ModelType(Parameters), deserialize_from='Parameters', serialize_when_none=False)


class ProcessingConfiguration(Model):
    enabled = BooleanType(deserialize_from='Enabled', serialize_when_none=False)
    processors = ListType(ModelType(Processors), deserialize_from='Processors', serialize_when_none=False)


# class S3BackupDescription(Model):
#     role_arn = StringType(deserialize_from='RoleARN')
#     bucket_arn = StringType(deserialize_from='BucketARN')
#     prefix = StringType(deserialize_from='Prefix')
#     error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
#     buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
#     compression_format = StringType(deserialize_from='CompressionFormat',
#                                     choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
#     encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration',
#                                          serialize_when_none=False)
#     cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


class ColumnToJsonKeyMappings(Model):
    key = StringType()
    value = StringType()


class OpenXJsonSerDe(Model):
    convert_dots_in_json_keys_to_underscores = BooleanType(deserialize_from='ConvertDotsInJsonKeysToUnderscores',
                                                           serialize_when_none=False)
    case_insensitive = BooleanType(deserialize_from='CaseInsensitive',
                                   serialize_when_none=False)
    column_to_json_key_mappings = ModelType(ColumnToJsonKeyMappings,
                                            deserialize_from='ColumnToJsonKeyMappings',
                                            serialize_when_none=False)


class HiveJsonSerDe(Model):
    timestamp_formats = ListType(StringType(),
                                 deserialize_from='TimestampFormats',
                                 serialize_when_none=False)


class Deserializer(Model):
    openx_json_ser_de = ModelType(OpenXJsonSerDe,
                                  deserialize_from="OpenXJsonSerDe",
                                  serialize_when_none=False)
    hive_json_ser_de = ModelType(HiveJsonSerDe,
                                 deserialize_from='HiveJsonSerDe',
                                 serialize_when_none=False)


class InputFormatConfiguration(Model):
    deserializer = ModelType(Deserializer, deserialize_from="Deserializer", serialize_when_none=False)


class OrcSerDe(Model):
    stripe_size_bytes = IntType(deserialize_from='StripeSizeBytes', serialize_when_none=False)
    block_size_bytes = IntType(deserialize_from='BlockSizeBytes', serialize_when_none=False)
    row_index_stride = IntType(deserialize_from='RowIndexStride', serialize_when_none=False)
    enable_padding = BooleanType(deserialize_from='EnablePadding', serialize_when_none=False)
    padding_tolerance = FloatType(deserialize_from='PaddingTolerance', serialize_when_none=False)
    compression = StringType(deserialize_from='Compression', choices=('NONE', 'ZLIB', 'SNAPPY'),
                             serialize_when_none=False)
    bloom_filter_columns = ListType(StringType(),
                                    deserialize_from='BloomFilterColumns',
                                    serialize_when_none=False)
    bloom_filter_false_positive_probability = FloatType(deserialize_from='BloomFilterFalsePositiveProbability',
                                                        serialize_when_none=False)
    dictionary_key_threshold = FloatType(deserialize_from='DictionaryKeyThreshold',
                                         serialize_when_none=False)
    format_version = StringType(deserialize_from='FormatVersion', choices=('V0_11', 'V0_12'),
                                serialize_when_none=False)


class ParquetSerDe(Model):
    block_size_bytes = IntType(deserialize_from='BlockSizeBytes',
                               serialize_when_none=False)
    page_size_bytes = IntType(deserialize_from='PageSizeBytes',
                              serialize_when_none=False)
    compression = StringType(deserialize_from='Compression', choices=('UNCOMPRESSED', 'GZIP', 'SNAPPY'),
                             serialize_when_none=False)
    enable_dictionary_compression = BooleanType(deserialize_from='EnableDictionaryCompression',
                                                serialize_when_none=False)
    max_padding_bytes = IntType(deserialize_from='MaxPaddingBytes',
                                serialize_when_none=False)
    writer_version = StringType(deserialize_from='WriterVersion',
                                choices=('V1', 'V2'),
                                serialize_when_none=False)


class Serializer(Model):
    parquet_ser_de = ModelType(ParquetSerDe, deserialize_from="ParquetSerDe", serialize_when_none=False)


class OutputFormatConfiguration(Model):
    serializer = ModelType(Serializer, deserialize_from="Serializer", serialize_when_none=False)
    orc_ser_de = ModelType(OrcSerDe, deserialize_from='OrcSerDe', serialize_when_none=False)


class SchemaConfiguration(Model):
    role_arn = StringType(deserialize_from='RoleARN', serialize_when_none=False)
    catalog_id = StringType(deserialize_from='CatalogId', serialize_when_none=False)
    database_name = StringType(deserialize_from='DatabaseName', serialize_when_none=False)
    table_name = StringType(deserialize_from='TableName', serialize_when_none=False)
    region = StringType(deserialize_from='Region', serialize_when_none=False)
    version_id = StringType(deserialize_from='VersionId', serialize_when_none=False)


class DataFormatConversionConfiguration(Model):
    enabled = BooleanType(deserialize_from='Enabled', serialize_when_none=False)
    schema_configuration = ModelType(SchemaConfiguration, deserialize_from="SchemaConfiguration",
                                     serialize_when_none=False)
    input_format_configuration = ModelType(InputFormatConfiguration, deserialize_from='InputFormatConfiguration',
                                           serialize_when_none=False)
    output_format_configuration = ModelType(OutputFormatConfiguration, deserialize_from='OutputFormatConfiguration',
                                            serialize_when_none=False)


class CopyCommand(Model):
    data_table_name = StringType(deserialize_from='DataTableName', serialize_when_none=False)
    data_table_columns = StringType(deserialize_from='DataTableColumns', serialize_when_none=False)
    copy_options = StringType(deserialize_from='CopyOptions', serialize_when_none=False)


class RetryOptions(Model):
    duration_in_seconds = IntType(deserialize_from='DurationInSeconds', serialize_when_none=False)


# class S3Configuration(Model):
#     role_arn = StringType(deserialize_from='RoleARN')
#     bucket_arn = StringType(deserialize_from='BucketARN')
#     prefix = StringType(deserialize_from='Prefix')
#     error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
#     buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
#     compression_format = StringType(deserialize_from='CompressionFormat',
#                                     choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
#     encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
#     cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


class VpcConfigurationDescription(Model):
    subnet_ids = ListType(StringType(), deserialize_from='SubnetIds', serialize_when_none=False)
    role_arn = StringType(deserialize_from='RoleARN', serialize_when_none=False)
    security_group_ids = ListType(StringType(), deserialize_from='SecurityGroupIds', serialize_when_none=False)
    vpc_id = StringType(deserialize_from='VpcId', serialize_when_none=False)


class EndpointConfiguration(Model):
    url = StringType(deserialize_from='Url', serialize_when_none=False)
    name = StringType(deserialize_from='Name', serialize_when_none=False)


class CommonAttributes(Model):
    attribute_name = StringType(deserialize_from='AttributeName', serialize_when_none=False)
    attribute_value = StringType(deserialize_from='AttributeValue', serialize_when_none=False)


class RequestConfiguration(Model):
    content_encoding = StringType(deserialize_from='ContentEncoding',
                                  choices=('NONE', 'GZIP'),
                                  serialize_when_none=False)
    common_attributes = ListType(ModelType(CommonAttributes, deserialize_from='CommonAttributes'),
                                 serialize_when_none=False)


class DynamicPartitioningConfiguration(Model):
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions', serialize_when_none=False)
    enabled = BooleanType(deserialize_from='Enabled', serialize_when_none=False)


class DestinationDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN', serialize_when_none=False)
    cloud_watch_logging_options = ModelType(BufferingHints, deserialize_from='CloudWatchLoggingOptions',
                                            serialize_when_none=False)
    processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration",
                                         serialize_when_none=False)


class S3DestinationDescription(DestinationDescription):
    bucket_arn = StringType(deserialize_from='BucketARN', serialize_when_none=False)
    prefix = StringType(deserialize_from='Prefix', serialize_when_none=False)
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix',
                                     serialize_when_none=False)
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints',
                                serialize_when_none=False)
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'),
                                    serialize_when_none=False)
    encryption_configuration = ModelType(EncryptionConfiguration,
                                         deserialize_from='EncryptionConfiguration',
                                         serialize_when_none=False)
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions,
                                            deserialize_from='CloudWatchLoggingOptions',
                                            serialize_when_none=False)


class ExtendedS3DestinationDescription(S3DestinationDescription):
    processing_configuration = ModelType(ProcessingConfiguration,
                                         deserialize_from="ProcessingConfiguration",
                                         serialize_when_none=False)
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'),
                                serialize_when_none=False)

    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription',
                                           serialize_when_none=False)
    data_format_conversion_configuration = ModelType(DataFormatConversionConfiguration,
                                                     deserialize_from='DataFormatConversionConfiguration',
                                                     serialize_when_none=False)
    dynamic_partitioning_configuration = ModelType(DynamicPartitioningConfiguration,
                                                   deserialize_from='DynamicPartitioningConfiguration',
                                                   serialize_when_none=False)


class RedshiftDestinationDescription(DestinationDescription):
    cluster_jdbc_url = StringType(deserialize_from='ClusterJDBCURL',
                                  serialize_when_none=False)
    copy_command = ModelType(CopyCommand, deserialize_from='CopyCommand',
                             serialize_when_none=False)
    username = StringType(deserialize_from='Username',
                          serialize_when_none=False)
    s3_destination_description = ModelType(S3DestinationDescription,
                                           deserialize_from="S3DestinationDescription",
                                           serialize_when_none=False)
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'),
                                serialize_when_none=False)
    s3_backup_description = ModelType(S3DestinationDescription, deserialize_from="S3BackupDescription",
                                      serialize_when_none=False)


class ElasticsearchDestinationDescription(DestinationDescription):
    domain_arn = StringType(deserialize_from='DomainARN', serialize_when_none=False)
    cluster_endpoint = StringType(deserialize_from='ClusterEndpoint', serialize_when_none=False)
    index_name = StringType(deserialize_from='IndexName', serialize_when_none=False)
    type_name = StringType(deserialize_from='TypeName', serialize_when_none=False)
    index_rotation_period = StringType(deserialize_from='IndexRotationPeriod',
                                       choices=('NoRotation', 'OneHour', 'OneDay', 'OneWeek', 'OneMonth'),
                                       serialize_when_none=False)
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions', serialize_when_none=False)
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('FailedDataOnly', 'AllData'))
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from="S3DestinationDescription",
                                           serialize_when_none=False)
    vpc_configuration_description = ModelType(VpcConfigurationDescription,
                                              deserialize_from='VpcConfigurationDescription', serialize_when_none=False)


class AmazonopensearchserviceDestinationDescription(ElasticsearchDestinationDescription):
    pass


class SplunkDestinationDescription(DestinationDescription):
    hec_endpoint = StringType(deserialize_from='HECEndpoint', serialize_when_none=False)
    hec_endpoint_type = StringType(deserialize_from='HECEndpointType', choices=('Raw', 'Event'),
                                   serialize_when_none=False)
    hec_token = StringType(deserialize_from='HECToken', serialize_when_none=False)
    hec_acknowledgment_timeout_in_seconds = IntType(deserialize_from='HECAcknowledgmentTimeoutInSeconds',
                                                    serialize_when_none=False)
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions', serialize_when_none=False)
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('FailedDataOnly', 'AllData'))
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from="S3DestinationDescription",
                                           serialize_when_none=False)


class HttpEndpointDestinationDescription(DestinationDescription):
    endpoint_configuration = ModelType(EndpointConfiguration, deserialize_from='EndpointConfiguration',
                                       serialize_when_none=False)
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    request_configuration = ModelType(RequestConfiguration, deserialize_from='RequestConfiguration',
                                      serialize_when_none=False)
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions', serialize_when_none=False)
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('FailedDataOnly', 'AllData'))
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from="S3DestinationDescription",
                                           serialize_when_none=False)


# class DestinationsRef(Model):
#     destination_id = ListType(StringType())
#     extended_s3_destination_description = ListType(ModelType(Destination), serialize_when_none=False,
#                                                    deserialize_from='ExtendedS3DestinationDescription')
#     elasticsearch_destination_description = ListType(ModelType(Destination), serialize_when_none=False,
#                                                      deserialize_from='ElasticsearchDestinationDescription')
#     splunk_destination_description = ListType(ModelType(Destination), serialize_when_none=False,
#                                               deserialize_from='SplunkDestinationDescription')
#     redshift_destination_description = ListType(ModelType(Destination), serialize_when_none=False,
#                                                 deserialize_from='RedshiftDestinationDescription')
#     http_endpoint_destination_description = ListType(ModelType(Destination), serialize_when_none=False,
#                                                      deserialize_from='HttpEndpointDestinationDescription')


class Destinations(Model):
    destination_id = StringType(deserialize_from='DestinationId')
    s3_destination_description = ModelType(S3DestinationDescription,
                                           deserialize_from='S3DestinationDescription',
                                           serialize_when_none=False)
    extended_s3_destination_description = ModelType(ExtendedS3DestinationDescription,
                                                    deserialize_from='ExtendedS3DestinationDescription',
                                                    serialize_when_none=False)
    elasticsearch_destination_description = ModelType(ElasticsearchDestinationDescription,
                                                      deserialize_from='ElasticsearchDestinationDescription',
                                                      serialize_when_none=False)
    amazon_opensearch_service_destination_description = ModelType(AmazonopensearchserviceDestinationDescription,
                                                                  deserialize_from='ElasticsearchDestinationDescription',
                                                                  serialize_when_none=False)
    splunk_destination_description = ModelType(SplunkDestinationDescription,
                                               deserialize_from='SplunkDestinationDescription',
                                               serialize_when_none=False)
    redshift_destination_description = ModelType(RedshiftDestinationDescription,
                                                 deserialize_from='RedshiftDestinationDescription',
                                                 serialize_when_none=False)
    http_endpoint_destination_description = ModelType(HttpEndpointDestinationDescription,
                                                      deserialize_from='HttpEndpointDestinationDescription',
                                                      serialize_when_none=False)


# class LambdaTab(Model):
#     source_record_transformation = StringType(choices=('Enabled', 'Disabled'))
#     buffer_conditions = StringType(serialize_when_none=False)
#     data_transformation = StringType(serialize_when_none=False)
#     lambda_func = StringType(serialize_when_none=False)
#     lambda_func_ver = StringType(serialize_when_none=False)
#     timeout = StringType(serialize_when_none=False)


# class S3BackupInfo(Model):
#     backup_mode = StringType(choices=('Enabled', 'Disabled'))
#     bucket_name = StringType(serialize_when_none=False)
#     buffer_conditions = StringType(serialize_when_none=False)
#     bucket_error_prefix = StringType(serialize_when_none=False)
#     compression = StringType(serialize_when_none=False)
#     encryption = StringType(serialize_when_none=False)


# class AdditionalTabs(Model):
#     cloud_watch_info = StringType(choices=('Enabled', 'Disabled'))
#     destination_name = StringType()
#     iam_role = StringType()
#     lambda_tab = ModelType(LambdaTab, serialize_when_none=False)
#     s3_backup_info = ModelType(S3BackupInfo)


class SourceKinesisStreamSourceDestination(Model):
    kinesis_stream_arn = StringType(deserialize_from='KinesisStreamARN')
    role_arn = StringType(deserialize_from='RoleARN')
    delivery_start_timestamp = DateTimeType(deserialize_from='DeliveryStartTimestamp')


class Source(Model):
    source_name = StringType()
    source_details = StringType()
    kinesis_stream_source_description = ModelType(SourceKinesisStreamSourceDestination, serialize_when_none=False,
                                                  deserialize_from='KinesisStreamSourceDescription')

# class LambdaTab(Model):
#     source_record_transformation = StringType(choices=('Enabled', 'Disabled'))
#     data_transformation = StringType(serialize_when_none=False)
#     buffer_conditions = StringType(serialize_when_none=False)
#     lambda_func = StringType(serialize_when_none=False)
#     lambda_func_ver = StringType(serialize_when_none=False)
#     timeout = StringType(serialize_when_none=False)


# class AdditionalTabs(Model):
#     destination_name = StringType()
#     cloud_watch_info = StringType(choices=('Enabled', 'Disabled'))
#     lambda_tab = ModelType(LambdaTab)
#     iam_role = StringType()
#     s3_backup_info = ModelType(S3BackupInfo)


class DeliveryStreamDescription(Model):
    delivery_stream_name = StringType(deserialize_from='DeliveryStreamName')
    delivery_stream_arn = StringType(deserialize_from='DeliveryStreamARN')
    delivery_stream_status = StringType(deserialize_from='DeliveryStreamStatus', choices=(
        'CREATING', 'CREATING_FAILED', 'DELETING', 'DELETING_FAILED', 'ACTIVE', 'SUSPENDED'))
    failure_description = ModelType(FailureDescription, deserialize_from='FailureDescription')
    delivery_stream_encryption_configuration = ModelType(DeliveryStreamEncryptionConfiguration,
                                                         deserialize_from='DeliveryStreamEncryptionConfiguration',
                                                         serialize_when_none=False)
    delivery_stream_type = StringType(deserialize_from="DeliveryStreamType",
                                      choices=('DirectPut', 'KinesisStreamAsSource'))
    version_id = StringType(deserialize_from='VersionId')
    create_timestamp = DateTimeType(deserialize_from='CreateTimestamp')
    last_update_timestamp = DateTimeType(deserialize_from='LastUpdateTimestamp')
    source = ModelType(Source, serialize_when_none=False, deserialize_from='Source')
    destinations = ListType(ModelType(Destinations), deserialize_from="Destinations")
    # destinations_ref = ModelType(DestinationsRef)
    # additional_tabs = ModelType(AdditionalTabs)
    HasMoreDestinations = BooleanType(deserialize_from='has_more_destinations')

    def reference(self, region_code):
        return {
            'resource_id': self.delivery_stream_arn,
            'external_link': f'https://console.aws.amazon.com/firehose/home?region={region_code}#/details/{self.delivery_stream_name}'
        }
