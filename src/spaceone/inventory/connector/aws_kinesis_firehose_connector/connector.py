import logging
import re
import time
from typing import List

from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.data import DeliveryStreamDescription
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.resource import DeliveryStreamResource, \
    FirehoseResponse
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KinesisFirehoseConnector(SchematicAWSConnector):
    service_name = "firehose"

    def get_resources(self):
        print("** Kinesis Firehose Manager Start **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                "request_method": self.request_data,
                "resource": DeliveryStreamResource,
                "response_schema": FirehoseResponse,
            }

        ]

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(
                    self.collect_data_by_region(
                        self.service_name, region_name, collect_resource
                    )
                )

        print(f" Kinesis Firehose Manager Finished {time.time() - start_time} Seconds")
        return resources

    def list_delivery_streams(self):
        response = self.client.list_delivery_streams()
        return response.get("DeliveryStreamNames", [])

    def request_data(self, region_name) -> List[DeliveryStreamDescription]:
        for stream_name in self.list_delivery_streams():
            stream_response = self.client.describe_delivery_stream(DeliveryStreamName=stream_name)
            delivery_stream_info = stream_response.get("DeliveryStreamDescription", {})
            destinations, additional_tabs = self.get_destinations(delivery_stream_info["Destinations"])
            delivery_stream_info.update(
                {
                    "source": self.get_source(delivery_stream_info.get("Source", {})),
                    "delivery_stream_status_display": self.get_delivery_stream_status_display(
                        (delivery_stream_info["DeliveryStreamStatus"])),
                    "destinations": destinations,
                    "additional_tabs": additional_tabs
                }
            )
            res = DeliveryStreamDescription(delivery_stream_info, strict=False)
            yield res

    def get_tags(self, name):
        tag_response = self.client.list_tags_for_delivery_stream(DeliveryStreamName=name)
        return tag_response.get("Tags", [])

    def get_destinations(self, destinations):
        destination_types = ["RedshiftDestinationDescription", "HttpEndpointDestinationDescription",
                             "ExtendedS3DestinationDescription", "ElasticsearchDestinationDescription",
                             "SplunkDestinationDescription"]

        destination_types = {
            "RedshiftDestinationDescription": self.update_redshift_destination_description,
            "HttpEndpointDestinationDescription": self.update_http_endpoint_destination_description,
            "ExtendedS3DestinationDescription": self.update_extended_s3_destination_description,
            "RedshiftDestinationDescElasticsearchDestinationDescription": self.update_redshift_destination_description,
            "ElasticsearchDestinationDescription": self.update_elasticsearch_destination_description,
            "SplunkDestinationDescription": self.update_splunk_destination_description
        }

        for destination in destinations:
            for key, value in destination.items():
                if key in destination_types:
                    # TODO
                    # destination_name, refined_destination_description = destination_types.get(key)
                    destination_name, refined_destination_description = eval(
                        f"self.update_" + self.camel_to_snake(key) + "(value)")
                    value.update(refined_destination_description)
                    additional_tabs = {
                        "destination_name": destination_name,
                        "cloud_watch_info": self.get_cloud_watch_error_logging(value["CloudWatchLoggingOptions"]),
                        "lambda_tab": self.get_lambda_tab(value["ProcessingConfiguration"]),
                        "iam_role": self.get_iam_role(value["RoleARN"]),
                        "s3_backup_info": self.get_s3_backup_info(value["S3BackupMode"],
                                                                  value.get("S3DestinationDescription", {}))
                    }
        return destinations, additional_tabs

    @staticmethod
    def update_splunk_destination_description(splunk_destination_description):
        refined_destination_description = {
            "hec_endpoint_details": f"{splunk_destination_description['HECEndpoint']} ({splunk_destination_description['HECEndpointType']} type)"
        }
        destination_name = splunk_destination_description["HECEndpoint"]
        return destination_name, refined_destination_description

    def update_elasticsearch_destination_description(self, elasticsearch_destination_description):
        refined_destination_description = {
            "domain_name": elasticsearch_destination_description["DomainARN"].split(":::")[1],
            "buffer_conditions": self.get_buffer_conditions(elasticsearch_destination_description["BufferingHints"])
        }
        destination_name = elasticsearch_destination_description["ClusterEndpoint"]
        return destination_name, refined_destination_description

    def update_extended_s3_destination_description(self, extended_s3_destination_description):
        refined_destination_description = {
            "data_format_conversion_configuration": self.get_data_format_conversion_configuration(
                extended_s3_destination_description.get("DataFormatConversionConfiguration", {})),
            "bucket_name": extended_s3_destination_description["BucketARN"].split(":::")[1],
            "buffer_conditions": self.get_buffer_conditions(extended_s3_destination_description["BufferingHints"])
        }
        destination_name = extended_s3_destination_description["BucketARN"].split("::")[1]
        return destination_name, refined_destination_description

    def update_http_endpoint_destination_description(self, http_endpoint_destination_description):
        refined_destination_description = {
            "buffer_conditions": self.get_buffer_conditions(http_endpoint_destination_description["BufferingHints"]),
        }
        destination_name = http_endpoint_destination_description["EndpointConfiguration"]["Url"]
        return destination_name, refined_destination_description

    @staticmethod
    def update_redshift_destination_description(redshift_destination_description):
        destination_name = redshift_destination_description["ClusterJDBCURL"].split("://")[1].split('.')[0]
        refined_destination_description = {
            "cluster": destination_name,
            "db_name": redshift_destination_description["ClusterJDBCURL"].split("/")[-1].split('.')[0]
        }

        return destination_name, refined_destination_description

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
    def get_iam_role(role_arn):
        return role_arn.split("/")[-1]

    @staticmethod
    def get_cloud_watch_error_logging(cloud_watch_logging_options):
        return "Enabled" if cloud_watch_logging_options["Enabled"] else "Disabled"

    def get_s3_backup_info(self, s3_backup_mode, s3_destination_description):
        s3_destination_description.update({
            "backup_mode": s3_backup_mode
        })
        if s3_backup_mode != "Disabled":
            s3_destination_description.update({
                "bucket_name": s3_destination_description["BucketARN"].split(":::")[1],
                "buffer_conditions": self.get_buffer_conditions(s3_destination_description["BufferingHints"])
            })
        return s3_destination_description

    def get_lambda_tab(self, processing_configuration):
        lambda_tab = dict()
        if not processing_configuration["Enabled"]:
            lambda_tab["source_record_transformation"] = "Disabled"
            lambda_tab["data_transformation"] = "Disabled"
        else:
            for processor in processing_configuration.get("Processors", []):
                if processor.get("Type", "") == 'Lambda':
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
        return f"{buffering_hints['SizeInMBs']} MiB or {buffering_hints['IntervalInSeconds']} seconds"

    @staticmethod
    def get_destination_display(destination):
        return destination["Url"]

    @staticmethod
    def get_role_arn(role_arn):
        return role_arn.split("/")[-1]

    @staticmethod
    def camel_to_snake(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def get_source(source):
        if not source:
            source_details = "Direct PUT and other sources"
            source_name = "Direct PUT and other sources"
        else:
            info = source.get("KinesisStreamSourceDescription", [])
            source_name = info.get("KinesisStreamARN").split('/')[1]
            source_details = f"Kinesis Data Stream : {source_name}"

        source.update({
            "source_details": source_details,
            "source_name": source_name
        })
        return source

    @staticmethod
    def get_delivery_stream_status_display(raw_status):
        return raw_status[0] + raw_status[1:].lower()
