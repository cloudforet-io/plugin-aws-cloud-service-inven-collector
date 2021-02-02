import logging
import time
from typing import List

from spaceone.inventory.connector.aws_kinesis_data_streams_connector.schema.data import StreamDescription
from spaceone.inventory.connector.aws_kinesis_data_streams_connector.schema.resource import StreamResource, KDSResponse
from spaceone.inventory.connector.aws_kinesis_data_streams_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class KinesisFirehoseConnector(SchematicAWSConnector):
    service_name = 'kinesis'

    def get_resources(self):
        print("** KinesisDataStream Manager Start **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_data,
                'resource': StreamResource,
                'response_schema': KDSResponse
            }
        ]

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' KinesisDataStream Manager Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self, region_name) -> List[StreamDescription]:
        paginator = self.client.get_paginator('list_delivery_streams')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('StreamDescription', []):
                stream_response = self.client.describe_stream(
                    StreamName=raw.get('StreamName'))
                stream_info = stream_response.get('StreamDescription', {})
                stream_info.update({
                    'delivery_stream_status_display': self.get_delivery_stream_status_display(stream_info.get('StreamStatus')),
                    'source_display': self.get_retention_period_days(stream_info.get('RetentionPeriodHours')),
                    'data_transformation': self.get_retention_period_display_days(
                        stream_info.get('RetentionPeriodHours')),
                    'destination_display': self.get_retention_period_display_details(
                        stream_info.get('RetentionPeriodHours')),
                    'tags': self.get_tags(stream_info.get(raw)),
                    'account_id': self.account_id
                })
                res = StreamDescription(stream_info, strict=False)
                yield res

    @staticmethod
    def get_stream_status_display(raw_status):
        return raw_status[0] + raw_status[1:].lower()

    @staticmethod
    def get_consumers_status_display(raw_status):
        return raw_status[0] + raw_status[1:].lower()

    @staticmethod
    def get_retention_period_days(retention_period_hours):
        return int(retention_period_hours / 24) + ' day' if retention_period_hours <= 24 else ' days'

    @staticmethod
    def get_retention_period_display_days(retention_period_hours):
        return f'{retention_period_hours} hours' if retention_period_hours < 24 else retention_period_hours.get_retention_period_days

    @staticmethod
    def get_retention_period_display_details(retention_period_hours):
        return f'{retention_period_hours} hours' + f'({retention_period_hours.get_retention_period_days})' \
            if retention_period_hours < 24 else retention_period_hours.get_retention_period_days

    @staticmethod
    def get_encryption_display(raw_encryption):
        return 'Disabled' if raw_encryption == 'NONE' else 'Enabled'

    @staticmethod
    def get_open_shards_num(shards_list):
        # print([shard for shard in shards_list if shard.ending_sequence_number is None])
        return len([shard for shard in shards_list if shard.ending_sequence_number is None])

    # @staticmethod
    # def get_closed_shards_num(shards_list):
    #     # print([shard for shard in shards_list if shard.ending_sequence_number is not None])
    #     return len([shard for shard in shards_list if shard.ending_sequence_number is not None])

    @staticmethod
    def get_tags(self, name):
        tag_response = self.client.list_tags_for_stream(StreamName=name)
        return tag_response.get('Tags', [])

    @staticmethod
    def get_consumers(self, arn):
        consumer_response = self.client.list_stream_consumers(StreamARN=arn)
        return consumer_response.get('Consumers', [])
