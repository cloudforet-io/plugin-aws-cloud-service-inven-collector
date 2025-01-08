import logging
from enum import verify

import boto3
from spaceone.core.utils import *

from spaceone.inventory.conf.cloud_service_conf import BOTO3_HTTPS_VERIFIED
from spaceone.inventory.connector.aws_cloud_watch_connector.schema.data import Alarms
from spaceone.inventory.connector.aws_cloud_watch_connector.schema.resource import AlarmsResource, AlarmsResponse
from spaceone.inventory.connector.aws_cloud_watch_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)

class CloudWatchConnector(SchematicAWSConnector):
    service_name = 'cloudwatch'
    cloud_service_group = 'CloudWatch'
    cloud_service_types = CLOUD_SERVICE_TYPES
    ComparisonOperator = {
        "GreaterThanOrEqualToThreshold": ">=",
        "GreaterThanThreshold": ">",
        "LessThanThreshold": "<",
        "LessThanOrEqualToThreshold": "<=",
        "LessThanLowerOrGreaterThanUpperThreshold": "<>",
        "LessThanLowerThreshold": "<",
        "GreaterThanUpperThreshold": ">"
    }

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: CloudWatch")
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

    def request_alarms_data(self, region_name):
        self.cloud_service_type = "Alarm"
        cloudwatch_resource_type = "AWS::CloudWatch::Alarm"

        try:
            raw_alarms = self.get_alarms()

            for raw_alarm in raw_alarms:

                self.set_alarm_conditions(raw_alarm)
                self._set_alarm_actions(raw_alarm)

                alarms_vo = Alarms(raw_alarm, strict=False)
                self.alarms.append(alarms_vo)

                yield {
                    "data": alarms_vo,
                    "name": alarms_vo.name,
                    "account": self.account_id,
                }

        except Exception as e:
            error_resource_response = self.generate_error(
                region_name, "alarms", e
            )
            yield {"data": error_resource_response}

    def get_alarms(self):
        response = self.client.describe_alarms()
        # Only MetricAlarms are returned temporarily, CompositeAlarms must be applied later.
        return response["MetricAlarms"]

    def set_alarm_conditions(self, raw_alarm):
        metric_name = raw_alarm.get("MetricName", "?")
        period = raw_alarm["Period"]
        evaluation_periods = self._convert_int_type(raw_alarm.get("EvaluationPeriods", "?"))
        threshold = self._convert_int_type(raw_alarm.get("Threshold", "?"))
        comparison_operator = raw_alarm.get("ComparisonOperator", "?")

        period_minutes = period // 60 if isinstance(period, int) else "?"
        operator = self.ComparisonOperator.get(comparison_operator, "?")

        raw_alarm["conditions"] = f"{metric_name} {operator} {threshold} for {evaluation_periods} datapoionts within {period_minutes} minutes"

    @staticmethod
    def _set_alarm_actions(raw_alarm):
        raw_alarm["actions"] = []
        actions = raw_alarm["actions"]
        alarm_actions = raw_alarm.get("AlarmActions", [])

        if alarm_actions:
            raw_alarm["actions_enabled"] = "Actions enabled"

            for action in alarm_actions:
                action_type = None
                action_description = None
                action_config = None

                if "sns" in action.lower():
                    action_type = "Notification"
                    action_description = action.split(":")[-1]
                    action_config = ""
                elif "lambda" in action.lower():
                    # lambda_client = boto3.client("lambda", region_name=self.region_name, verify=BOTO3_HTTPS_VERIFIED)
                    # lambda_response = lambda_client.get_function(FunctionName=action.split(':')[-1])
                    pass
                elif "ec2" in action.lower():
                    # ec2_client = boto3.client("ec2", region_name=self.region_name, verify=BOTO3_HTTPS_VERIFIED)
                    # ec2_response = ec2_client.describe_instances(InstanceIds=action.split(':')[-1])
                    pass

                actions.append({"type": action_type, "description": action_description, "config": action_config})
        else:
            raw_alarm["actions_enabled"] = "No Actions"


    @staticmethod
    def _convert_int_type(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
