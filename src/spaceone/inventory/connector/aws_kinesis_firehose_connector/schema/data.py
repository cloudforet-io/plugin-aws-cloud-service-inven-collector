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
    key_arn = StringType(deserialize_from='KeyARN', serialize_when_none=False)
    key_type = StringType(deserialize_from='KeyType', choices=('AWS_OWNED_CMK', 'CUSTOMER_MANAGED_CMK'),
                          serialize_when_none=False)
    status = StringType(deserialize_from='Status',
                        choices=('ENABLED', 'ENABLING', 'ENABLING_FAILED', 'DISABLED', 'DISABLING', 'DISABLING_FAILED'))
    failure_description = ModelType(FailureDescription, deserialize_from="FailureDescription",
                                    serialize_when_none=False)


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
    no_encryption_config = StringType(deserialize_from="NoEncryptionConfig", serialize_when_none=False)
    no_encryption = StringType(deserialize_from="NoEncryption", serialize_when_none=False)
    kms_encryption_config = ModelType(KMSEncryptionConfig, deserialize_from="KMSEncryptionConfig",
                                      serialize_when_none=False)


class CloudWatchLoggingOptions(Model):
    enabled = BooleanType(deserialize_from='Enabled')
    log_group_name = StringType(deserialize_from='LogGroupName')
    log_stream_name = StringType(deserialize_from='LogStreamName')


class BufferingHints(Model):
    size_in_mbs = IntType(deserialize_from='SizeInMBs')
    interval_in_seconds = IntType(deserialize_from='IntervalInSeconds')


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
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration',
                                         serialize_when_none=False)
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
    database_name = StringType(deserialize_from='DatabaseName', serialize_when_none=False)
    table_name = StringType(deserialize_from='TableName', serialize_when_none=False)
    region = StringType(deserialize_from='Region', serialize_when_none=False)
    version_id = StringType(deserialize_from='VersionId', serialize_when_none=False)


class DataFormatConversionConfiguration(Model):
    enabled = BooleanType(deserialize_from='Enabled')
    schema_configuration = ModelType(SchemaConfiguration, deserialize_from="SchemaConfiguration")
    input_format_configuration = ModelType(InputFormatConfiguration, deserialize_from='InputFormatConfiguration')
    output_format_configuration = ModelType(OutputFormatConfiguration, deserialize_from='OutputFormatConfiguration')
    input_format = StringType(serialize_when_none=False)
    output_format = StringType(serialize_when_none=False)
    record_format_conversion = StringType(choices=('Enabled', 'Disabled'))


class CopyCommand(Model):
    data_table_name = StringType(deserialize_from='DataTableName')
    data_table_columns = StringType(deserialize_from='DataTableColumns', serialize_when_none=False)
    copy_options = StringType(deserialize_from='CopyOptions', serialize_when_none=False)


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


class VpcConfigurationDescription(Model):
    subnet_ids = ListType(StringType(), deserialize_from='SubnetIds')
    role_arn = StringType(deserialize_from='RoleARN')
    security_group_ids = ListType(StringType(), deserialize_from='SecurityGroupIds')
    vpc_id = StringType(deserialize_from='VpcId')


class EndpointConfiguration(Model):
    url = StringType(deserialize_from='Url')
    name = StringType(deserialize_from='Name')


class CommonAttributes(Model):
    attribute_name = StringType(deserialize_from='AttributeName')
    attribute_value = StringType(deserialize_from='AttributeValue')


class RequestConfiguration(Model):
    content_encoding = StringType(deserialize_from='ContentEncoding', choices=('NONE', 'GZIP'))
    common_attributes = ListType(ModelType(CommonAttributes, deserialize_from='CommonAttributes'))


class S3DestinationDescription(Model):
    role_arn = StringType(deserialize_from='RoleARN')
    bucket_arn = StringType(deserialize_from='BucketARN')
    prefix = StringType(deserialize_from='Prefix')
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
    cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


# class ExtendedS3DestinationDescription(Model):
#     role_arn = StringType(deserialize_from='RoleARN')
#     bucket_arn = StringType(deserialize_from='BucketARN')
#     prefix = StringType(deserialize_from='Prefix')
#     error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix')
#     buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
#     compression_format = StringType(deserialize_from='CompressionFormat',
#                                     choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'))
#     encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration')
#     cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')
#
#     processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
#     s3_backup_mode = StringType(deserialize_from='S3Bac`kupMode', choices=('Disabled', 'Enabled'))
#     s3_backup_description = ModelType(S3BackupDescription, deserialize_from='S3BackupDescription')
#     data_format_conversion_configuration = ModelType(DataFormatConversionConfiguration,
#                                                      deserialize_from='DataFormatConversionConfiguration')


# class RedshiftDestinationDescription(Model):
#     cluster_jdb_curl = StringType(deserialize_from='ClusterJDBCURL')
#     copy_command = ModelType(CopyCommand, deserialize_from='CopyCommand')
#     username = StringType(deserialize_from='Username')

# role_arn = StringType(deserialize_from='RoleARN')
# retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
# s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
# processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
# s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'))
# s3_backup_description = ModelType(S3BackupDescription, deserialize_from='S3BackupDescription')
# cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


# class ElasticsearchDestinationDescription(Model):
#     domain_arn = StringType(deserialize_from='DomainARN')
#     cluster_endpoint = StringType(deserialize_from='ClusterEndpoint')
#     index_name = StringType(deserialize_from='IndexName')
#     type_name = StringType(deserialize_from='TypeName')
#     index_rotation_period = StringType(deserialize_from='IndexRotationPeriod',
#                                        choices=('NoRotation', 'OneHour', 'OneDay', 'OneWeek', 'OneMonth'))
#     vpc_configuration_description = ModelType(VpcConfigurationDescription,
#                                               deserialize_from='VpcConfigurationDescription')
#
#     role_arn = StringType(deserialize_from='RoleARN')
#     buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
#     retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
# s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'))
# s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
# processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
# cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


# class SplunkDestinationDescription(Model):
#     hec_endpoint = StringType(deserialize_from='HECEndpoint', serialize_when_none=False)
#     hec_endpoint_type = StringType(deserialize_from='HECEndpointType', choices=('Raw', 'Event'), serialize_when_none=False)
#     hec_token = StringType(deserialize_from='HECToken', serialize_when_none=False)
#     hec_acknowledgment_timeout_in_seconds = IntType(deserialize_from='HECAcknowledgmentTimeoutInSeconds', serialize_when_none=False)
#
#     retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
# s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('Disabled', 'Enabled'))
# s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
# processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
# cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')


# class HttpEndpointDestinationDescription(Model):
#     endpoint_configuration = ModelType(EndpointConfiguration, deserialize_from='EndpointConfiguration')
#     buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints')
#
#     request_configuration = ModelType(RequestConfiguration, deserialize_from='RequestConfiguration')
#     role_arn = StringType(deserialize_from='RoleARN')
#     retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions')
# s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('FailedDataOnly', 'AllData'))
# s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
# processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
# cloud_watch_logging_options = ModelType(CloudWatchLoggingOptions, deserialize_from='CloudWatchLoggingOptions')

class Destination(Model):
    cloud_watch_logging_options = ModelType(BufferingHints, deserialize_from='CloudWatchLoggingOptions')
    processing_configuration = ModelType(ProcessingConfiguration, deserialize_from="ProcessingConfiguration")
    s3_backup_mode = StringType(deserialize_from='S3BackupMode', choices=('FailedDataOnly', 'AllData'))

    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription',
                                           serialize_when_none=False)
    role_arn = StringType(deserialize_from='RoleARN', serialize_when_none=False)
    buffering_hints = ModelType(BufferingHints, deserialize_from='BufferingHints', serialize_when_none=False)
    request_configuration = ModelType(RequestConfiguration, deserialize_from='RequestConfiguration',
                                      serialize_when_none=False)
    retry_options = ModelType(RetryOptions, deserialize_from='RetryOptions', serialize_when_none=False)

    # ExtendedS3DestinationDescription
    bucket_name = StringType(serialize_when_none=False)
    buffer_conditions = StringType(serialize_when_none=False)
    bucket_arn = StringType(deserialize_from='BucketARN', serialize_when_none=False)
    prefix = StringType(deserialize_from='Prefix', serialize_when_none=False)
    error_output_prefix = StringType(deserialize_from='ErrorOutputPrefix', serialize_when_none=False)
    compression_format = StringType(deserialize_from='CompressionFormat',
                                    choices=('UNCOMPRESSED', 'GZIP', 'ZIP', 'Snappy', 'HADOOP_SNAPPY'),
                                    serialize_when_none=False)
    encryption_configuration = ModelType(EncryptionConfiguration, deserialize_from='EncryptionConfiguration',
                                         serialize_when_none=False)
    data_format_conversion_configuration = ModelType(DataFormatConversionConfiguration,
                                                     deserialize_from='DataFormatConversionConfiguration',
                                                     serialize_when_none=False)

    # RedshiftDestinationDescription
    cluster_jdb_curl = StringType(deserialize_from='ClusterJDBCURL', serialize_when_none=False)
    copy_command = ModelType(CopyCommand, deserialize_from='CopyCommand', serialize_when_none=False)
    username = StringType(deserialize_from='Username', serialize_when_none=False)

    # ElasticsearchDestinationDescription
    domain_arn = StringType(deserialize_from='DomainARN', serialize_when_none=False)
    cluster_endpoint = StringType(deserialize_from='ClusterEndpoint', serialize_when_none=False)
    index_name = StringType(deserialize_from='IndexName', serialize_when_none=False)
    type_name = StringType(deserialize_from='TypeName', serialize_when_none=False)
    index_rotation_period = StringType(deserialize_from='IndexRotationPeriod',
                                       choices=('NoRotation', 'OneHour', 'OneDay', 'OneWeek', 'OneMonth'),
                                       serialize_when_none=False)
    vpc_configuration_description = ModelType(VpcConfigurationDescription,
                                              deserialize_from='VpcConfigurationDescription', serialize_when_none=False)
    # HttpEndpointDestinationDescription
    endpoint_configuration = ModelType(EndpointConfiguration, deserialize_from='EndpointConfiguration',
                                       serialize_when_none=False)
    buffer_conditions = StringType(serialize_when_none=False)
    cluster = StringType(serialize_when_none=False)
    db_name = StringType(serialize_when_none=False)

    # SplunkDestinationDescription
    hec_endpoint = StringType(deserialize_from='HECEndpoint', serialize_when_none=False)
    hec_endpoint_type = StringType(deserialize_from='HECEndpointType', choices=('Raw', 'Event'),
                                   serialize_when_none=False)
    hec_token = StringType(deserialize_from='HECToken', serialize_when_none=False)
    hec_acknowledgment_timeout_in_seconds = IntType(deserialize_from='HECAcknowledgmentTimeoutInSeconds',
                                                    serialize_when_none=False)


class Destinations(Model):
    destination_id = StringType(deserialize_from='DestinationId')
    s3_destination_description = ModelType(S3DestinationDescription, deserialize_from='S3DestinationDescription')
    extended_s3_destination_description = ModelType(Destination,
                                                    deserialize_from='ExtendedS3DestinationDescription')
    elasticsearch_destination_description = ModelType(Destination,
                                                      deserialize_from='ElasticsearchDestinationDescription')
    splunk_destination_description = ModelType(Destination,
                                               deserialize_from='SplunkDestinationDescription')
    redshift_destination_description = ModelType(Destination,
                                                 deserialize_from='RedshiftDestinationDescription')
    http_endpoint_destination_description = ModelType(Destination,
                                                      deserialize_from='HttpEndpointDestinationDescription')


class LambdaTab(Model):
    source_record_transformation = StringType(choices=('Enabled', 'Disabled'))
    buffer_conditions = StringType(serialize_when_none=False)
    data_transformation = StringType(serialize_when_none=False)
    lambda_func = StringType(serialize_when_none=False)
    lambda_func_ver = StringType(serialize_when_none=False)
    timeout = StringType(serialize_when_none=False)


class S3BackupInfo(Model):
    backup_mode = StringType(choices=('Enabled', 'Disabled'))
    bucket_name = StringType(serialize_when_none=False)
    buffer_conditions = StringType(serialize_when_none=False)
    bucket_error_prefix = StringType(serialize_when_none=False)
    compression = StringType(serialize_when_none=False)
    encryption = StringType(serialize_when_none=False)


class AdditionalTabs(Model):
    cloud_watch_info = StringType(choices=('Enabled', 'Disabled'))
    destination_name = StringType()
    iam_role = StringType()
    lambda_tab = ModelType(LambdaTab, serialize_when_none=False)
    s3_backup_info = ModelType(S3BackupInfo)


class Source(Model):
    source_details = StringType()
    source_name = StringType()


class LambdaTab(Model):
    source_record_transformation = StringType()
    data_transformation = StringType()
    buffer_conditions = StringType()
    lambda_func = StringType()
    lambda_func_ver = StringType()
    timeout = StringType()


class AdditionalTabs(Model):
    destination_name = StringType()
    cloud_watch_info = StringType()
    lambda_tab = ModelType(LambdaTab)
    iam_role = StringType()
    s3_backup_info = ModelType(S3BackupInfo)


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
    source = ModelType(Source)  # Source, deserialize_from="Source"
    # destinations = ListType(ModelType(Destinations), deserialize_from='Destinations')
    destinations = ListType(ModelType(Destinations))
    additional_tabs = ModelType(AdditionalTabs)
    HasMoreDestinations = BooleanType(deserialize_from='has_more_destinations')

    def reference(self, region_code):
        return {
            'resource_id': self.delivery_stream_arn,
            'external_link': f'https://console.aws.amazon.com/kinesis/home?region={region_code}#/streams/details/{self.delivery_stream_name}'
        }
