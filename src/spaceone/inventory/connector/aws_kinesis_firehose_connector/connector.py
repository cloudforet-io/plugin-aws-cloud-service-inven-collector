import logging
import time
from typing import List

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

    def request_data(self, region_name) -> List[DeliveryStreamDescription]:
        if not self.client.can_paginate("list_delivery_streams"):
            print(region_name, self.client.can_paginate("list_delivery_streams"))
            return
        paginator = self.client.get_paginator("list_delivery_streams")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )
        for data in response_iterator:
            for stream_name in data.get("DeliveryStreamNames", []):
                stream_response = self.client.describe_delivery_stream(DeliveryStreamName=stream_name)

                delivery_stream_info = stream_response.get("DeliveryStreamDescription", {})
                # num_of_con, consumers = self.get_consumers(stream_info.get("StreamARN"))
                delivery_stream_info.update(
                    {
                        "source": self.get_source_info(delivery_stream_info.get("Source"), {}),
                        "delivery_stream_status_display": self.get_delivery_stream_status_display((delivery_stream_info.get("delivery_stream_status"))),
                        # "data_transformation": self.get_retention_period_display(
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
    def get_source_info(source):
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