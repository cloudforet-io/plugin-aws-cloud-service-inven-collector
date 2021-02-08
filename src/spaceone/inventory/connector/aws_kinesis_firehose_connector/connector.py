import logging
import time
from typing import List
from pprint import pprint
from spaceone.inventory.connector.aws_kinesis_data_stream_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.data import DeliveryStreamDescription
from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.resource import DeliveryStreamResource, \
    FirehoseResponse
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KinesisFirehoseConnector(SchematicAWSConnector):
    service_name = "firehose"

    def get_resources(self):
        print("** kinesis Firehose Manager Start **")
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

        print(f" kinesis Firehose Manager Finished {time.time() - start_time} Seconds")
        return resources
    def list_delivery_streams(self):

        response = self.client.list_delivery_streams()

        return response.get("DeliveryStreamNames", [])

    def request_data(self, region_name) -> List[DeliveryStreamDescription]:
        delivery_streams = self.list_delivery_streams()

        for stream_name in delivery_streams:
            stream_response = self.client.describe_delivery_stream(DeliveryStreamName=stream_name)

            delivery_stream_info = stream_response.get("DeliveryStreamDescription", {})
            # num_of_con, consumers = self.get_consumers(stream_info.get("StreamARN"))
            delivery_stream_info.update(
                {
                    "source": self.get_source(delivery_stream_info.get("Source"), {}),
                    "delivery_stream_status_display": self.get_delivery_stream_status_display(
                        (delivery_stream_info.get("delivery_stream_status"))),
                    "destinations": self.get_destinations(delivery_stream_info.get("Destinations"), {})
                    #     stream_info.get("RetentionPeriodHours")
                    # ),
                    # "destination_display": f"{stream_info.get('RetentionPeriodHours')} hours",
                    # "encryption_display": self.get_encryption_display(
                    #     stream_info.get("EncryptionType")
                    # ),
                    # "shard_level_metrics_display": self.get_shard_level_metrics_display(
                    #     stream_info.get("EnhancedMonitoring")
                    # ),
                    # "open_shards_num": self.get_open_shards_num(
                    #     stream_info.get("Shards")
                    # ),
                    # "closed_shards_num": self.get_closed_shards_num(
                    #     stream_info.get("Shards")
                    # ),
                    # "consumers_vo": {
                    #     "num_of_consumers": num_of_con,
                    #     "consumers": consumers,
                    # },
                    # "tags": self.get_tags(stream_info.get("StreamName")),
                    # "account_id": self.account_id,
                }
            )
            print(delivery_stream_info)
            res = DeliveryStreamDescription(delivery_stream_info, strict=False)
            yield res

    def get_tags(self, name):
        tag_response = self.client.list_tags_for_delivery_stream(DeliveryStreamName=name)
        return tag_response.get("Tags", [])

    @staticmethod
    def get_source(source):
        if not source:
            source_details = source_name = "Direct PUT and other sources"
        else:
            info = source.get("KinesisStreamSourceDescription", [])
            source_name = info.get("KinesisStreamARN").split('/')[1]
            source_details = f"{source_name} (Kinesis Data Stream)"
        source.update({
            "source_details": source_details,
            "source_name": source_name
        })
        return source

    @staticmethod
    def get_delivery_stream_status_display(raw_status):
        return raw_status[0] + raw_status[1:].lower()

    @staticmethod
    def get_destinations(destinations):
        _fitered_idx = []
        _fitered_vo = []

        extended_s3_destination_description = destinations.get("ExtendedS3DestinationDescription", {})
        if extended_s3_destination_description != {}:
            destination_type = "Amazon S3"
            destination_name = extended_s3_destination_description["BucketARN"].split("::")[1]

        redshift_destination_description = destinations.get("RedshiftDestinationDescription", {})
        if redshift_destination_description != {}:
            destination_type = "Amazon Redshift"
            destination_name = redshift_destination_description["ClusterJDBCURL"].split("://")[1].split('.')[0]

        elasticsearch_destination_description = destinations.get("ElasticsearchDestinationDescription", {})
        splunk_destination_description = destinations.get("SplunkDestinationDescription", {})

        http_endpoint_destination_description = destinations.get("HttpEndpointDestinationDescription", {})
        if http_endpoint_destination_description != {}:
            destination_type = "HTTP endpoint"
            destination_name = http_endpoint_destination_description["Url"]

        destinations.update({
            "destination_display": f"{destination_type} {destination_name}"
        })

    # 데스티네이션 리스트로 해서 돌리기..?
    # 파람에 info 줘서 update하기
    # textdyfield 없는 경우는...? 괜찮겟지?

    @staticmethod
    def get_destination_display(destination):
        return destination["Url"]

    @staticmethod
    def get_role_arn(role_arn):
        return role_arn.split("/")[-1]

    @staticmethod
    def get_lambda_info(processing_configuration):
        lambda_info = dict()
        for processor in processing_configuration.get("Processors", []):
            if processor["Type"] == 'Lambda':
                for parameter in processor.get("Parameters", []):
                    if parameter["ParameterName"] == "LambdaArn":
                        lambda_info["lambda_func"] = parameter["ParameterValue"].split(":")[6]
                        lambda_info["lambda_func_ver"] = parameter["ParameterValue"].split(":")[7]
                    elif parameter["ParameterName"] == "NumberOfRetries":
                        lambda_info["timeout"] = f"{parameter['ParameterValue']} seconds"
                    elif parameter["ParameterName"] == "BufferSizeInMBs":
                        lambda_info["buffer_conditions"] = f"{parameter['ParameterValue']} MiB"
                    elif parameter["ParameterName"] == "BufferIntervalInSeconds":
                        lambda_info["buffer_conditions"] += f" or {parameter['ParameterValue']} seconds"

        lambda_info["source_record_transformation"] = "Enabled" if processing_configuration["Enabled"] else "Disabled"
        lambda_info["data_transformation"] = lambda_info["lambda_func"] if processing_configuration[
            "Enabled"] else "Disabled"

        return lambda_info
