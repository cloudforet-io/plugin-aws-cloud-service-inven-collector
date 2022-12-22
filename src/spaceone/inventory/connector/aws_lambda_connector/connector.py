import logging
from typing import List
from spaceone.core.utils import *
from spaceone.inventory.connector.aws_lambda_connector.schema.data import LambdaFunctionData, \
    EnvironmentVariable, LambdaState, LastUpdateStatus, Environment, Layer
from spaceone.inventory.connector.aws_lambda_connector.schema.resource import LambdaFunctionResponse, \
    LambdaFunctionResource, LambdaLayerResource, LambdaLayerResponse
from spaceone.inventory.connector.aws_lambda_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)


class LambdaConnector(SchematicAWSConnector):
    service_name = 'lambda'
    cloud_service_group = 'Lambda'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Lambda")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_functions_data,
                'resource': LambdaFunctionResource,
                'response_schema': LambdaFunctionResponse
            },
            {
                'request_method': self.request_layer_data,
                'resource': LambdaLayerResource,
                'response_schema': LambdaLayerResponse
            }
        ]

        resources.extend(self.set_cloud_service_types())

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Lambda ({time.time() - start_time} sec)')
        return resources

    @property
    def layers(self):
        return self.init_property('_lambda_layers', lambda: {})

    def request_functions_data(self, region_name) -> List[LambdaFunctionData]:
        cloud_service_group = 'Lambda'
        cloud_service_type = 'Function'
        cloudwatch_namespace = 'AWS/Lambda'
        cloudwatch_dimension_name = 'FunctionName'
        cloudtrail_resource_type = 'AWS::Lambda::Function'

        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('list_functions')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('Functions', []):
                try:
                    func = LambdaFunctionData(raw, strict=False)
                    func.region_name = region_name
                    func.cloudwatch = self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                          raw['FunctionName'], region_name)
                    func.cloudtrail = self.set_cloudtrail(region_name, cloudtrail_resource_type, func.name)

                    if raw.get('State'):
                        func.state = LambdaState({
                            'type': raw.get('State'),
                            'reason': raw.get('StateReason'),
                            'reason_code': raw.get('StateReasonCode'),
                        })
                    if raw.get('LastUpdateStatus'):
                        func.last_update = LastUpdateStatus({
                            'type': raw.get('LastUpdateStatus'),
                            'reason': raw.get('LastUpdateStatusReason'),
                            'reason_code': raw.get('LastUpdateStatusReasonCode'),
                        })

                    if env := raw.get('Environment'):
                        if not func.environment:
                            func.environment = Environment()
                        func.environment.variables = [
                            EnvironmentVariable({'key': k, 'value': v}) for k, v in env.get('Variables', {}).items()
                        ]

                    yield {
                        'data': func,
                        'name': func.name,
                        'instance_size': float(func.code_size),
                        'account': self.account_id,
                        'tags': self.list_tags(func.arn)
                    }
                    
                except Exception as e:
                    resource_id = raw.get('FunctionArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def request_layer_data(self, region_name) -> List[Layer]:
        cloud_service_group = 'Lambda'
        cloud_service_type = 'Layer'
        cloudtrail_resource_type = 'AWS::Lambda::Layer'

        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('list_layers')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data['Layers']:
                try:
                    latest_matching_version = raw.get('LatestMatchingVersion', {})
                    if 'Version' in latest_matching_version:
                        raw.update({
                            'version': latest_matching_version.get('Version')
                        })

                    raw.update({
                        'region_name': region_name,
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['LayerArn'])
                    })

                    layer_vo = Layer(raw, strict=False)
                    yield {
                        'data': layer_vo,
                        'name': layer_vo.layer_name,
                        'launched_at': self.datetime_to_iso8601(layer_vo.latest_matching_version.created_date),
                        'account': self.account_id
                    }
                    
                except Exception as e:
                    resource_id = raw.get('LayerArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    def list_tags(self, arn):
        response = self.client.list_tags(Resource=arn)
        return response.get('Tags', {})
