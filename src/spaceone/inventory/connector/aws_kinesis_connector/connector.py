import logging
import time
from typing import List

from spaceone.inventory.connector.aws_kinesis_connector.schema.data import (
    StreamDescription,
    Consumers,
)
from spaceone.inventory.connector.aws_kinesis_connector.schema.resource import (
    StreamResource,
    KDSResponse,
)
from spaceone.inventory.connector.aws_kinesis_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KinesisConnector(SchematicAWSConnector):
    service_name = "kinesis"

    def get_resources(self):
        print("** kinesis Manager Start **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                "request_method": self.request_data,
                "resource": StreamResource,
                "response_schema": KDSResponse,
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

        print(f" kinesis Manager Finished {time.time() - start_time} Seconds")
        return resources

    def request_data(self, region_name) -> List[StreamDescription]:
        paginator = self.client.get_paginator("list_streams")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )
        for data in response_iterator:
            for stream_name in data.get("StreamNames", []):
                stream_response = self.client.describe_stream(
                    StreamName=stream_name
                )

                stream_info = stream_response.get("StreamDescription", {})
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
                        "open_shards_num": self.get_open_shards_num(
                            stream_info.get("Shards")
                        ),
                        "closed_shards_num": self.get_closed_shards_num(
                            stream_info.get("Shards")
                        ),
                        "consumers": self.get_consumers(stream_info.get("StreamARN")),
                        "tags": self.get_tags(stream_info.get("StreamName")),
                        "account_id": self.account_id,
                    }
                )
                res = StreamDescription(stream_info, strict=False)
                yield res

    def get_tags(self, name):
        tag_response = self.client.list_tags_for_stream(StreamName=name)
        return tag_response.get("Tags", [])

    def get_consumers(self, arn):
        consumer_response = self.client.list_stream_consumers(StreamARN=arn)
        consumers_info = consumer_response.get("Consumers", [])

        consumers = []
        for consumer_info in consumers_info:
            consumer_info.update({
                "consumer_status_display": self.get_consumers_status_display(consumer_info.get("ConsumerStatus")),
                "consumers_num": self.get_consumers_num(consumer_info.get("Consumers", []))
            })
            consumers.append(Consumers(consumer_info, strict=False))

        return consumers

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
        if not day:
            return f"{hour} hours"
        else:
            if not hour:
                return day + "day" if not day else "days"
            else:
                return f"{hour} hours {day}" + "day" if not day else "days"

    @staticmethod
    def get_retention_period_display_details(retention_period_hours):
        return (
            f"{retention_period_hours} hours"
            + f"({retention_period_hours.get_retention_period_days})"
            if retention_period_hours < 24
            else retention_period_hours.get_retention_period_days
        )

    @staticmethod
    def get_encryption_display(raw_encryption):
        return "Disabled" if raw_encryption == "NONE" else "Enabled"

    @staticmethod
    def get_open_shards_num(shards_list):
        return len(
            [shard for shard in shards_list if shard.get("SequenceNumberRange", {}).get("EndingSequenceNumber") is None]
        )

    @staticmethod
    def get_closed_shards_num(shards_list):
        return len(
            [shard for shard in shards_list if
             shard.get("SequenceNumberRange", {}).get("EndingSequenceNumber") is not None]
        )
