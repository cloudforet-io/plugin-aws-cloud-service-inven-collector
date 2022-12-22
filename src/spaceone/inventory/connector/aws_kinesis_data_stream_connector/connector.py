import logging
from typing import List

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_kinesis_data_stream_connector.schema.data import StreamDescription, Consumers
from spaceone.inventory.connector.aws_kinesis_data_stream_connector.schema.resource import StreamResource, KDSResponse
from spaceone.inventory.connector.aws_kinesis_data_stream_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KinesisDataStreamConnector(SchematicAWSConnector):
    service_name = "kinesis"
    cloud_service_group = 'KinesisDataStream'
    cloud_service_type = 'DataStream'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Kinesis Data Stream")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                "request_method": self.request_data,
                "resource": StreamResource,
                "response_schema": KDSResponse,
            }
        ]

        resources.extend(self.set_cloud_service_types())

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: '
                      f'{self.account_id}] FINISHED: Kinesis Data Stream ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[StreamDescription]:
        cloudwatch_namespace = 'AWS/Kinesis'
        cloudwatch_dimension_name = 'StreamName'
        cloudtrail_resource_type = 'AWS::Kinesis::Stream'

        paginator = self.client.get_paginator("list_streams")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )
        for data in response_iterator:
            for stream_name in data.get("StreamNames", []):
                try:
                    stream_response = self.client.describe_stream(StreamName=stream_name)

                    stream_info = stream_response.get("StreamDescription", {})
                    num_of_con, consumers = self.get_consumers(stream_info.get("StreamARN"))
                    stream_info.update(
                        {
                            "stream_status_display": self.get_stream_status_display(
                                stream_info.get("StreamStatus")
                            ),
                            "retention_period_days": self.get_retention_period_days(
                                stream_info.get("RetentionPeriodHours")
                            ),
                            "retention_period_display": self.get_retention_period_display(
                                stream_info.get("RetentionPeriodHours")
                            ),
                            "retention_period_display_hours": f"{stream_info.get('RetentionPeriodHours')} hours",
                            "encryption_display": self.get_encryption_display(
                                stream_info.get("EncryptionType")
                            ),
                            "shard_level_metrics_display": self.get_shard_level_metrics_display(
                                stream_info.get("EnhancedMonitoring")
                            ),
                            "open_shards_num": self.get_open_shards_num(
                                stream_info.get("Shards")
                            ),
                            "closed_shards_num": self.get_closed_shards_num(
                                stream_info.get("Shards")
                            ),
                            "consumers_vo": {
                                "num_of_consumers": num_of_con,
                                "consumers": consumers,
                            },
                            'cloudwatch': self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                              stream_info['StreamName'], region_name),
                            'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type,
                                                              stream_info['StreamARN'])
                        }
                    )
                    stream_vo = StreamDescription(stream_info, strict=False)
                    yield {
                        'data': stream_vo,
                        'instance_size': float(stream_vo.open_shards_num),
                        'launched_at': self.datetime_to_iso8601(stream_vo.stream_creation_timestamp),
                        'name': stream_vo.stream_name,
                        'account': self.account_id,
                        'tags': self.get_tags(stream_vo.stream_name)
                    }

                except Exception as e:
                    resource_id = stream_name
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def get_tags(self, name):
        tag_response = self.client.list_tags_for_stream(StreamName=name)
        return self.convert_tags_to_dict_type(tag_response.get('Tags', []))

    def get_consumers(self, arn):
        consumer_response = self.client.list_stream_consumers(StreamARN=arn)
        consumers_info = consumer_response.get("Consumers", [])
        consumers_num = len(consumers_info)

        consumers = []
        for consumer_info in consumers_info:
            consumer_info.update(
                {
                    "consumer_status_display": self.get_consumers_status_display(
                        consumer_info.get("ConsumerStatus")
                    ),
                }
            )
            consumers.append(Consumers(consumer_info, strict=False))

        return consumers_num, consumers

    @staticmethod
    def get_consumers_num(consumers):
        return len(consumers)

    @staticmethod
    def get_consumers_status_display(raw_status):
        return raw_status[0] + raw_status[1:].lower()

    @staticmethod
    def get_stream_status_display(raw_status):
        return raw_status[0] + raw_status[1:].lower()

    @staticmethod
    def get_retention_period_days(retention_period_hours):
        return int(retention_period_hours / 24)

    @staticmethod
    def get_retention_period_display(retention_period_hours):
        day = int(retention_period_hours / 24)
        hour = int(retention_period_hours % 24)

        day_postfix = f"{day} day" if day == 1 else ("" if not day else f"{day} days")
        hour_postfix = (
            f" {hour} hour" if hour == 1 else ("" if not hour else f" {hour} hours")
        )
        return day_postfix + hour_postfix

    @staticmethod
    def get_encryption_display(raw_encryption):
        return "Disabled" if raw_encryption == "NONE" else "Enabled"

    @staticmethod
    def get_shard_level_metrics_display(enhanced_monitoring):
        return (
            ["Disabled"]
            if not enhanced_monitoring[0]["ShardLevelMetrics"]
            else enhanced_monitoring[0]["ShardLevelMetrics"]
        )

    @staticmethod
    def get_open_shards_num(shards_list):
        return len(
            [
                shard
                for shard in shards_list
                if shard.get("SequenceNumberRange", {}).get("EndingSequenceNumber")
                   is None
            ]
        )

    @staticmethod
    def get_closed_shards_num(shards_list):
        return len(
            [
                shard
                for shard in shards_list
                if shard.get("SequenceNumberRange", {}).get("EndingSequenceNumber")
                   is not None
            ]
        )
