import logging
from typing import Generator, List

from dateutil.relativedelta import relativedelta
from spaceone.core.utils import *

from spaceone.inventory.connector.aws_cloud_watch_connector.schema.data import Alarms
from spaceone.inventory.connector.aws_cloud_watch_connector.schema.resource import (
    AlarmsResource,
    AlarmsResponse,
)
from spaceone.inventory.connector.aws_cloud_watch_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.connector.aws_dynamodb_connector.schema.data import Table
from spaceone.inventory.connector.aws_dynamodb_connector.schema.resource import (
    TableResource,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)


class CloudWatchConnector(SchematicAWSConnector):
    service_name = "cloudwatch"
    cloud_service_group = "CloudWatch"
    cloud_service_types = CLOUD_SERVICE_TYPES
    ComparisonOperator = {
        "GreaterThanOrEqualToThreshold": ">=",
        "GreaterThanThreshold": ">",
        "LessThanThreshold": "<",
        "LessThanOrEqualToThreshold": "<=",
        "LessThanLowerOrGreaterThanUpperThreshold": "<>",
        "LessThanLowerThreshold": "<",
        "GreaterThanUpperThreshold": ">",
    }

    def get_resources(self) -> List[TableResource]:
        _LOGGER.debug(
            f"[get_resources][account_id: {self.account_id}] START: CloudWatch"
        )
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        collect_resources = [
            {
                "request_method": self.request_alarms_data,
                "resource": AlarmsResource,
                "response_schema": AlarmsResponse,
            }
        ]

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)
                self.alarms = []

                for collect_resource in collect_resources:
                    resources.extend(
                        self.collect_data_by_region(
                            self.service_name, region_name, collect_resource
                        )
                    )
            except Exception as e:
                error_resource_response = self.generate_error(region_name, "", e)
                resources.append(error_resource_response)

        _LOGGER.debug(
            f"[get_resources][account_id: {self.account_id}] FINISHED: CloudWatch ({time.time() - start_time} sec)"
        )
        return resources

    def get_alarms(self):
        paginator = self.client.get_paginator("describe_alarms")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxRecords": 100,
            }
        )

        for data in response_iterator:
            # Only MetricAlarms are returned temporarily, CompositeAlarms must be applied later.
            for raw in data.get("MetricAlarms", []):
                yield raw

    def request_alarms_data(self, region_name: str) -> List[Table]:
        self.cloud_service_type = "Alarm"
        cloudwatch_resource_type = "AWS::CloudWatch::Alarm"

        try:
            raw_alarms = self.get_alarms()
            for raw_alarm in raw_alarms:
                self._set_alarm_conditions(raw_alarm)
                self._set_alarm_actions(raw_alarm)
                self._set_alarm_history(raw_alarm)
                tags = self._get_alarms_tags(raw_alarm.get("AlarmArn"))

                alarms_vo = Alarms(raw_alarm, strict=False)
                self.alarms.append(alarms_vo)

                yield {
                    "data": alarms_vo,
                    "name": alarms_vo.name,
                    "account": self.account_id,
                    "tags": self.convert_tags_to_dict_type(tags),
                }

        except Exception as e:
            error_resource_response = self.generate_error(region_name, "alarms", e)
            yield {"data": error_resource_response}

    def _set_alarm_conditions(self, raw_alarm: Alarms) -> None:
        metric_name = raw_alarm.get("MetricName", "?")
        period = raw_alarm.get("Period", None)
        evaluation_periods = self._convert_int_type(
            raw_alarm.get("EvaluationPeriods", "?")
        )
        threshold = self._convert_int_type(raw_alarm.get("Threshold", "?"))
        comparison_operator = raw_alarm.get("ComparisonOperator", "?")

        period_minutes = period // 60 if period and isinstance(period, int) else "?"
        operator = self.ComparisonOperator.get(comparison_operator, "?")

        raw_alarm["conditions"] = (
            f"{metric_name} {operator} {threshold} for {evaluation_periods} datapoionts within {period_minutes} minutes"
        )

    @staticmethod
    def _set_alarm_actions(raw_alarm: Alarms) -> None:
        raw_alarm["actions"] = []
        actions = raw_alarm["actions"]
        alarm_actions = raw_alarm.get("AlarmActions", [])
        ok_actions = raw_alarm.get("OKActions ", [])
        insufficient_data_actions = raw_alarm.get("InsufficientDataActions", [])

        raw_alarm["actions_enabled"] = (
            "Actions enabled"
            if raw_alarm.get("ActionsEnabled", False)
            else "No actions"
        )

        for action in alarm_actions:
            actions.append({"type": "AlarmAction", "arn": action})

        for action in ok_actions:
            actions.append({"type": "OKAction", "arn": action})

        for action in insufficient_data_actions:
            actions.append({"type": "InsufficientDataAction", "arn": action})

    def get_alarm_history(self, alarm_name: str) -> Generator[dict, None, None]:
        paginator = self.client.get_paginator("describe_alarm_history")

        end_date = datetime.datetime.now() - relativedelta(months=1)
        response_iterator = paginator.paginate(
            PaginationConfig={
                "AlarmName": alarm_name,
                "MaxItems": 100,
                "EndDate": end_date,
                "ScanBy": "TimestampDescending",
            }
        )

        for data in response_iterator:
            for raw in data.get("AlarmHistoryItems", []):
                yield raw

    def _set_alarm_history(self, raw_alarm: Alarms) -> None:
        raw_alarm["history"] = []
        history = raw_alarm["history"]

        alarm_histories = self.get_alarm_history(raw_alarm["AlarmName"])
        for alarm_history in alarm_histories:
            history.append(
                {
                    "date": alarm_history["Timestamp"],
                    "type": alarm_history["HistoryItemType"],
                    "description": alarm_history["HistorySummary"],
                }
            )

    def _get_alarms_tags(self, alarm_arn: str):
        response = self.client.list_tags_for_resource(ResourceARN=alarm_arn)
        return response["Tags"]

    @staticmethod
    def _convert_int_type(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
