import logging
from spaceone.core.utils import *
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.data import DeliveryStreamDescription
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.resource import DeliveryStreamResource, \
    FirehoseResponse
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KinesisFirehoseConnector(SchematicAWSConnector):
    service_name = "firehose"
    cloud_service_group = 'KinesisFirehose'
    cloud_service_type = 'DeliveryStream'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Kinesis Firehose")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                "request_method": self.request_data,
                "resource": DeliveryStreamResource,
                "response_schema": FirehoseResponse,
            }
        ]

        resources.extend(self.set_cloud_service_types())

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(
                    self.collect_data_by_region(
                        self.service_name, region_name, collect_resource
                    )
                )

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Kinesis Firehose ({time.time() - start_time} sec)')
        return resources

    def list_delivery_streams(self):
        response = self.client.list_delivery_streams()
        return response.get("DeliveryStreamNames", [])

    def request_data(self, region_name):
        cloudwatch_namespace = 'AWS/Firehose'
        cloudwatch_dimension_name = 'DeliveryStreamName'
        cloudtrail_resource_type = 'AWS::KinesisFirehose::DeliveryStream'

        for stream_name in self.list_delivery_streams():
            try:
                stream_response = self.client.describe_delivery_stream(DeliveryStreamName=stream_name)
                delivery_stream_info = stream_response.get("DeliveryStreamDescription", {})
                # destinations_ref, additional_tabs = self.get_destinations_ref(delivery_stream_info.get("Destinations", []))
                delivery_stream_info.update(
                    {
                        "Source": self.get_source(delivery_stream_info.get("Source", {})),
                        'cloudwatch': self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                          delivery_stream_info['DeliveryStreamName'], region_name),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                          delivery_stream_info['DeliveryStreamARN']),
                        # "destinations_ref": destinations_ref,
                        # "additional_tabs": additional_tabs
                    }
                )

                stream_vo = DeliveryStreamDescription(delivery_stream_info, strict=False)
                yield {
                    'data': stream_vo,
                    'name': stream_vo.delivery_stream_name,
                    'launched_at': self.datetime_to_iso8601(stream_vo.create_timestamp),
                    'account': self.account_id,
                    'tags': self.get_tags(stream_vo.delivery_stream_name)
                }

            except Exception as e:
                resource_id = stream_name
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def get_tags(self, name):
        tag_response = self.client.list_tags_for_delivery_stream(DeliveryStreamName=name)
        return self.convert_tags_to_dict_type(tag_response.get('Tags', []))

    def get_destinations_ref(self, destinations):
        destn_types = ["RedshiftDestinationDescription", "HttpEndpointDestinationDescription",
                       "ExtendedS3DestinationDescription", "ElasticsearchDestinationDescription",
                       "SplunkDestinationDescription"]

        destinations_ref = self.initiate_destinations_ref(destn_types, destinations)
        additional_tabs = dict()

        for key, values in destinations_ref.items():
            if values:
                values, additional_tabs = self.refine_destinations_ref(key, values)

        return destinations_ref, additional_tabs

    @staticmethod
    def initiate_destinations_ref(destn_types, destinations):
        destinations_ref = dict()
        for destn_type in destn_types:
            destinations_ref[destn_type] = list()

        for destination in destinations:
            for key, value in destination.items():
                if key in destn_types:
                    destinations_ref[key].append(value)
        return destinations_ref

    def refine_destinations_ref(self, key, values):
        destn_type_map = {
            "RedshiftDestinationDescription": self.update_redshift_destination_description,
            "HttpEndpointDestinationDescription": self.update_http_endpoint_destination_description,
            "ExtendedS3DestinationDescription": self.update_extended_s3_destination_description,
            "ElasticsearchDestinationDescription": self.update_elasticsearch_destination_description,
            "SplunkDestinationDescription": self.update_splunk_destination_description
        }

        additional_tabs = dict()

        for value in values:
            destn_name, refined_destn_des = destn_type_map[key](value)

            value.update(refined_destn_des)
            additional_tabs = {
                "destination_name": destn_name,
                "cloud_watch_info": self.get_cloud_watch_error_logging(value.get("CloudWatchLoggingOptions", {})),
                "lambda_tab": self.get_lambda_tab(value.get("ProcessingConfiguration", {})),
                "iam_role": value.get("RoleARN", ""),
                "s3_backup_info": self.get_s3_backup_info(value.get("S3BackupMode"),
                                                          value.get("S3DestinationDescription", {}))
            }

        return values, additional_tabs

    @staticmethod
    def update_splunk_destination_description(splunk_destination_description):
        refined_destn_des = {
            "hec_endpoint_details": f"{splunk_destination_description['HECEndpoint']} ({splunk_destination_description['HECEndpointType']} type)"
        }
        destn_name = splunk_destination_description["HECEndpoint"]
        return destn_name, refined_destn_des

    def update_elasticsearch_destination_description(self, elasticsearch_destination_description):
        refined_destn_des = {
            "domain_name": elasticsearch_destination_description["DomainARN"].split(":::")[1],
            "buffer_conditions": self.get_buffer_conditions(elasticsearch_destination_description["BufferingHints"])
        }
        destn_name = elasticsearch_destination_description["ClusterEndpoint"]
        return destn_name, refined_destn_des

    def update_extended_s3_destination_description(self, extended_s3_destination_description):
        refined_destn_des = {
            "data_format_conversion_configuration": self.get_data_format_conversion_configuration(
                extended_s3_destination_description.get("DataFormatConversionConfiguration", {})),
            "bucket_name": extended_s3_destination_description["BucketARN"].split(":::")[1],
            "buffer_conditions": self.get_buffer_conditions(extended_s3_destination_description["BufferingHints"])
        }
        destn_name = extended_s3_destination_description["BucketARN"].split(":::")[1]
        return destn_name, refined_destn_des

    def update_http_endpoint_destination_description(self, http_endpoint_destination_description):
        refined_destn_des = {
            "buffer_conditions": self.get_buffer_conditions(http_endpoint_destination_description["BufferingHints"]),
        }
        destn_name = http_endpoint_destination_description["EndpointConfiguration"]["Url"]
        return destn_name, refined_destn_des

    @staticmethod
    def update_redshift_destination_description(redshift_destination_description):
        destn_name = redshift_destination_description["ClusterJDBCURL"].split("://")[1].split('.')[0]
        refined_destn_des = {
            "cluster": destn_name,
            "db_name": redshift_destination_description["ClusterJDBCURL"].split("/")[-1].split('.')[0]
        }

        return destn_name, refined_destn_des

    @staticmethod
    def get_data_format_conversion_configuration(data_format_conversion_configuration):
        try:
            if data_format_conversion_configuration["Enabled"]:
                data_format_conversion_configuration.update({
                    "record_format_conversion": "Enabled",
                    "input_format": list(data_format_conversion_configuration["InputFormatConfiguration"]
                                         .get("Deserializer", {}).keys()),
                    "output_format": list(data_format_conversion_configuration["OutputFormatConfiguration"]
                                          .get("Serializer", {}).keys()),
                })
            else:
                data_format_conversion_configuration.update({
                    "record_format_conversion": "Disabled"})
        except:
            data_format_conversion_configuration.update({
                "record_format_conversion": "Disabled"})
        return data_format_conversion_configuration

    @staticmethod
    def get_cloud_watch_error_logging(cloud_watch_logging_options):
        return "Enabled" if cloud_watch_logging_options.get("Enabled") else "Disabled"

    def get_s3_backup_info(self, s3_backup_mode, s3_destination_description):
        s3_destination_description.update({
            "backup_mode": s3_backup_mode
        })
        if s3_backup_mode == "Enabled":
            s3_destination_description.update({
                "buffer_conditions": self.get_buffer_conditions(s3_destination_description.get("BufferingHints", {}))
            })
        return s3_destination_description

    def get_lambda_tab(self, processing_configuration):
        lambda_tab = dict()
        if not processing_configuration.get("Enabled"):
            lambda_tab["source_record_transformation"] = "Disabled"
            lambda_tab["data_transformation"] = "Disabled"
        else:
            for processor in processing_configuration.get("Processors", []):
                if processor.get("Type") == 'Lambda':
                    lambda_tab = self.get_lambda_processor_info(processor)
                    lambda_tab["source_record_transformation"] = "Enabled"
                    lambda_tab["data_transformation"] = lambda_tab["lambda_func"]
        return lambda_tab

    @staticmethod
    def get_lambda_processor_info(processor):
        lambda_tab = dict()
        for parameter in processor.get("Parameters", []):
            if parameter["ParameterName"] == "LambdaArn":
                lambda_tab["lambda_func"] = parameter["ParameterValue"].split(":")[6]
                lambda_tab["lambda_func_ver"] = parameter["ParameterValue"].split(":")[7]
            elif parameter["ParameterName"] == "NumberOfRetries":
                lambda_tab["timeout"] = f"{parameter['ParameterValue']} seconds"
            elif parameter["ParameterName"] == "BufferSizeInMBs":
                lambda_tab["buffer_conditions"] = f"{parameter['ParameterValue']} MiB"
            elif parameter["ParameterName"] == "BufferIntervalInSeconds":
                lambda_tab["buffer_conditions"] += f" or {parameter['ParameterValue']} seconds"
        return lambda_tab

    @staticmethod
    def get_buffer_conditions(buffering_hints):
        return f"{buffering_hints.get('SizeInMBs', 0)} MiB or {buffering_hints('IntervalInSeconds', 0)} seconds"

    @staticmethod
    def get_source(source):
        if source:
            kinesis_data_stream_arn = source.get('KinesisStreamSourceDescription', {}).get('KinesisStreamARN', '')

            source.update({
                'source_details': f"Kinesis Data Stream : {kinesis_data_stream_arn}",
                'source_name': kinesis_data_stream_arn
            })
        else:
            source = {
                'source_details': "Direct PUT and other sources",
                'source_name': "Direct PUT and other sources"
            }

        return source
