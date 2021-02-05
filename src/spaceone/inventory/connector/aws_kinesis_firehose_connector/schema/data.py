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
        'UNKNOWN_ERROR'))
    details = StringType(deserialize_from='Details')


class DeliveryStreamEncryptionConfiguration(Model):
    key_arn = StringType(deserialize_from='KeyARN')
    key_type = StringType(deserialize_from='KeyType', choices=('AWS_OWNED_CMK', 'CUSTOMER_MANAGED_CMK'))
    status = StringType(deserialize_from='Status',
                        choices=('ENABLED', 'ENABLING', 'ENABLING_FAILED', 'DISABLED', 'DISABLING', 'DISABLING_FAILED'))
    failure_description = ModelType(FailureDescription, deserialize_from="FailureDescription")


class KinesisStreamSourceDescription(Model):
    kinesis_stream_arn = StringType(deserialize_from='KinesisStreamARN')
    role_arn = StringType(deserialize_from='RoleARN')
    delivery_start_timestamp = DateTimeType(deserialize_from='DeliveryStartTimestamp')


class Source(Model):
    source_name = StringType()
    source_details = StringType()
    kinesis_stream_source_description = ModelType(KinesisStreamSourceDescription,
                                                  deserialize_from="KinesisStreamSourceDescription")


class KMSEncryptionConfig(Model):
    aws_kms_key_arn = StringType(deserialize_from="AWSKMSKeyARN")


class EncryptionConfiguration(Model):
    no_encryption_config = StringType(deserialize_from="NoEncryptionConfig")
    no_encryption = StringType(deserialize_from="NoEncryption")
    kms_encryption_config = ModelType(KMSEncryptionConfig, deserialize_from="KMSEncryptionConfig")


class CloudWatchLoggingOptions(Model):
    enabled = BooleanType(deserialize_from='Enabled')
    log_group_name = StringType(deserialize_from='LogGroupName')
    log_stream_name = StringType(deserialize_from='LogStreamName')


class BufferingHints(Model):
    size_in_mbs = IntType(deserialize_from='SizeInMBs')
    interval_in_seconds = IntType(deserialize_from='IntervalInSeconds')


class S3DestinationDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    bucket_arn = StringType(deserialize_from='BucketARN')
    prefix = StringType(deserialize_from='Prefix')
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
    CloudWatchLoggingOptions = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


class Parameters(Model):
    parameter_name = StringType(deserialize_from='ParameterName', choices=(
        'LambdaArn', 'NumberOfRetries', 'RoleArn', 'BufferSizeInMBs', 'BufferIntervalInSeconds'))
    parameter_value = StringType(deserialize_from='ParameterValue')


class Processors(Model):
    type = StringType(deserialize_from='Type')
    parameters = ListType(ModelType(Parameters), deserialize_from='Parameters')


class ProcessingConfiguration(Model):
    enabled = BooleanType(deserialize_from='Enabled')
    processors = ListType(ModelType(Processors), deserialize_from='Processors')


class S3BackupDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    bucket_arn = StringType(deserialize_from='BucketARN')
    prefix = StringType(deserialize_from='Prefix')
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


class ColumnToJsonKeyMappings(Model):  # SimpleTableLayout
    key = StringType()
    value = StringType()


class OpenXJsonSerDe(Model):
    convert_dots_in_json_keys_to_underscores = BooleanType(deserialize_from='ConvertDotsInJsonKeysToUnderscores')
    case_insensitive = BooleanType(deserialize_from='CaseInsensitive')
    column_to_json_key_mappings = ModelType(ColumnToJsonKeyMappings, deserialize_from='ColumnToJsonKeyMappings')


class HiveJsonSerDe(Model):
    timestamp_formats = ListType(StringType(), deserialize_from='TimestampFormats')


class Deserializer(Model):
    openx_json_ser_de = ModelType(OpenXJsonSerDe, deserialize_from="OpenXJsonSerDe")
    hive_json_ser_de = ModelType(HiveJsonSerDe, deserialize_from='HiveJsonSerDe')


class InputFormatConfiguration(Model):
    deserializer = ModelType(Deserializer, deserialize_from="Deserializer")


class OrcSerDe(Model):
    stripe_size_bytes = IntType(deserialize_from='StripeSizeBytes')
    block_size_bytes = IntType(deserialize_from='BlockSizeBytes')
    row_index_stride = IntType(deserialize_from='RowIndexStride')
    enable_padding = BooleanType(deserialize_from='EnablePadding')
    padding_tolerance = FloatType(deserialize_from='PaddingTolerance')
    compression = StringType(deserialize_from='Compression', choices=('NONE', 'ZLIB', 'SNAPPY'))
    bloom_filter_columns = ListType(StringType(), deserialize_from='BloomFilterColumns')
    bloom_filter_false_positive_probability = FloatType(deserialize_from='BloomFilterFalsePositiveProbability')
    dictionary_key_threshold = FloatType(deserialize_from='DictionaryKeyThreshold')
    format_version = StringType(deserialize_from='FormatVersion', choices=('V0_11', 'V0_12'))


class ParquetSerDe(Model):
    block_size_bytes = IntType(deserialize_from='BlockSizeBytes')
    page_size_bytes = IntType(deserialize_from='PageSizeBytes')
    compression = StringType(deserialize_from='Compression', choices=('UNCOMPRESSED', 'GZIP', 'SNAPPY'))
    enable_dictionary_compression = BooleanType(deserialize_from='EnableDictionaryCompression')
    max_padding_bytes = IntType(deserialize_from='MaxPaddingBytes')
    writer_version = StringType(deserialize_from='WriterVersion', choices=('V1', 'V2'))


class Serializer(Model):
    parquet_ser_de = ModelType(ParquetSerDe, deserialize_from="ParquetSerDe")


class OutputFormatConfiguration(Model):
    serializer = ModelType(Serializer, deserialize_from="Serializer")
    orc_ser_de = ModelType(OrcSerDe, deserialize_from='OrcSerDe')


class SchemaConfiguration(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    catalog_id = StringType(deserialize_from='CatalogId')
    database_name = StringType(deserialize_from='DatabaseName')
    table_name = StringType(deserialize_from='TableName')
    region = StringType(deserialize_from='Region')
    version_id = StringType(deserialize_from='VersionId')


class DataFormatConversionConfiguration(Model):
    schema_configuration = ModelType(SchemaConfiguration, deserialize_from="SchemaConfiguration")
    input_format_configuration = ModelType(InputFormatConfiguration, deserialize_from='InputFormatConfiguration')
    output_format_configuration = ModelType(OutputFormatConfiguration, deserialize_from='OutputFormatConfiguration')


class ExtendedS3DestinationDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    bucket_arn = StringType(deserialize_from='BucketARN')
    prefix = StringType(deserialize_from='Prefix')
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')
    processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'))
    s3_backup_description = ModelType(S3BackupDescription, deserialize_from='S3BackupDescription')
    data_format_conversion_configuration = ModelType(DataFormatConversionConfiguration,
                                                     deserialize_from='DataFormatConversionConfiguration')
    enabled = BooleanType(deserialize_from='Enabled')


class CopyCommand(Model):
    data_table_name = StringType(deserialize_from='DataTableName')
    data_table_columns = StringType(deserialize_from='DataTableColumns')
    copy_options = StringType(deserialize_from='CopyOptions')


class RetryOptions(Model):
    duration_in_seconds = IntType(deserialize_from='DurationInSeconds')


class S3Configuration(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    bucket_arn = StringType(deserialize_from='BucketARN')
    prefix = StringType(deserialize_from='Prefix')
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


class RedshiftDestinationDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    cluster_jdb_curl = StringType(deserialize_from='ClusterJDBCURL')
    copy_command = ModelType(CopyCommand, deserialize_from='CopyCommand')
    username = StringType(deserialize_from='Username')
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
    s3_configuration = ModelType(S3Configuration, deserialize_from='S3Configuration')
    processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")


class VpcConfigurationDescription(Model):
    subnet_ids = ListType(StringType(), deserialize_from='SubnetIds')
    role_arn = StringType(deserialize_from='RoleARN')
    security_group_ids = ListType(StringType(), deserialize_from='SecurityGroupIds')
    vpc_id = StringType(deserialize_from='VpcId')


class ElasticsearchDestinationDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    domain_arn = StringType(deserialize_from='DomainARN')
    cluster_endpoint = StringType(deserialize_from='ClusterEndpoint')
    index_name = StringType(deserialize_from='IndexName')
    type_name = StringType(deserialize_from='TypeName')
    index_rotation_period = StringType(deserialize_from='IndexRotationPeriod',
                                       choices=('NoRotation', 'OneHour', 'OneDay', 'OneWeek', 'OneMonth'))
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'))
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
    processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')
    vpc_configuration_description = ModelType(VpcConfigurationDescription,
                                              deserialize_from='VpcConfigurationDescription')


class SplunkDestinationDescription(Model):
    hec_endpoint = StringType(deserialize_from='HECEndpoint')
    hec_endpoint_type = StringType(deserialize_from='HECEndpointType', choices=('Raw', 'Event'))
    hec_token = StringType(deserialize_from='HECToken')
    hec_acknowledgment_timeout_in_seconds = IntType(deserialize_from='HECAcknowledgmentTimeoutInSeconds')
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'))
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
    processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


class EndpointConfiguration(Model):
    url = StringType(deserialize_from='Url')
    name = StringType(deserialize_from='Name')


class CommonAttributes(Model):
    attribute_name = StringType(deserialize_from='AttributeName')
    attribute_value = StringType(deserialize_from='AttributeValue')


class RequestConfiguration(Model):
    content_encoding = StringType(deserialize_from='ContentEncoding', choices=('NONE', 'GZIP'))
    common_attributes = ModelType(CommonAttributes, deserialize_from='CommonAttributes')


class HttpEndpointDestinationDescription(Model):
    endpoint_configuration = ModelType(EndpointConfiguration, deserialize_from='EndpointConfiguration')
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')
    request_configuration = ModelType(RequestConfiguration, deserialize_from='RequestConfiguration')


class Destinations(Model):
    destination_id = StringType(deserialize_from='DestinationId')
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
    extended_s3_destination_description = ModelType(ExtendedS3DestinationDescription,
                                                    deserialize_from='ExtendedS3DestinationDescription')
    redshift_destination_description = ModelType(RedshiftDestinationDescription,
                                                 deserialize_from='RedshiftDestinationDescription')
    elasticsearch_destination_description = ModelType(ElasticsearchDestinationDescription,
                                                      deserialize_from='ElasticsearchDestinationDescription')
    splunk_destination_description = ModelType(SplunkDestinationDescription,
                                               deserialize_from='SplunkDestinationDescription')
    http_endpoint_destination_description = ModelType(HttpEndpointDestinationDescription,
                                                      deserialize_from='HttpEndpointDestinationDescription')

class DeliveryStreamDescription(Model):
    delivery_stream_name = StringType(deserialize_from='DeliveryStreamName')
    delivery_stream_arn = StringType(deserialize_from='DeliveryStreamARN')
    delivery_stream_status = StringType(deserialize_from='DeliveryStreamStatus', choices=(
        'CREATING', 'CREATING_FAILED', 'DELETING', 'DELETING_FAILED', 'ACTIVE', 'SUSPENDED'))
    failure_description = ModelType(FailureDescription, deserialize_from='FailureDescription')
    delivery_stream_encryption_configuration = ModelType(DeliveryStreamEncryptionConfiguration,
                                                         deserialize_from='DeliveryStreamEncryptionConfiguration')
    delivery_stream_type = StringType(deserialize_from="DeliveryStreamType",
                                      choices=('DirectPut', 'KinesisStreamAsSource'))
    version_id = StringType(deserialize_from='VersionId')
    create_timestamp = DateTimeType(deserialize_from='CreateTimestamp')
    last_update_timestamp = DateTimeType(deserialize_from='LastUpdateTimestamp')
    source = ModelType(Source, default={}) #Source, deserialize_from="Source"
    destinations = ListType(ModelType(Destinations), deserialize_from='Destinations')
    HasMoreDestinations = BooleanType(deserialize_from='has_more_destinations')

    def reference(self, region_code):
        return {
            'resource_id': self.stream_arn,
            'external_link': f'https://console.aws.amazon.com/kinesis/home?region={region_code}#/streams/details/{self.stream_name}'
        }
