import time
import logging
from typing import List
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_lambda_connector.schema.data import LambdaFunctionData, \
    EnvironmentVariable, LambdaState, LastUpdateStatus, VPC, VPCConfig, Environment, Subnet, SecurityGroup, Layer
from spaceone.inventory.connector.aws_lambda_connector.schema.resource import LambdaFunctionResponse, \
    LambdaFunctionResource, LambdaLayerResource, LambdaLayerResponse
from spaceone.inventory.connector.aws_lambda_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.data_loader import DataLoader

_LOGGER = logging.getLogger(__name__)


class VpcDataLoader(DataLoader):

    @property
    def resource(self):
        return self.session.resource('ec2')

    def fetch_data(self, resource_id):
        data = {}
        try:
            vpc = self.resource.Vpc(resource_id)
            data['is_default'] = vpc.is_default
            for tag in vpc.tags:
                if tag['Key'] == 'Name':
                    data['name'] = tag['Value']
        except ClientError as e:
            _LOGGER.debug(e)
        return data


class LambdaConnector(SchematicAWSConnector):
    service_name = 'lambda'
    cloud_service_group = 'Lambda'

    def get_resources(self):
        _LOGGER.debug("[get_resources] START: Lambda")
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

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: Lambda ({time.time() - start_time} sec)')
        return resources

    @property
    def layers(self):
        return self.init_property('_lambda_layers', lambda: {})

    def get_vpc(self, vpc_config):
        vpc_data = None

        if vpc_id := vpc_config.get('VpcId'):
            vpc_data = VpcDataLoader(self.session).get(vpc_id)

            vpc = {
                'id': vpc_id,
                'name': vpc_data.get('name'),
                'is_default': vpc_data.get('is_default')
            }
            subnets = [Subnet({'id': subnet_id}) for subnet_id in vpc_config.get('SubnetIds', [])]
            security_groups = [
                SecurityGroup({'id': sg_id}) for sg_id in vpc_config.get('SecurityGroupIds', [])
            ]
            vpc_data = VPCConfig({'vpc': VPC(vpc), 'subnets': subnets, 'security_groups': security_groups, })

        return vpc_data

    def request_functions_data(self, region_name) -> List[LambdaFunctionData]:
        cloud_service_group = 'Lambda'
        cloud_service_type = 'Function'
        self.cloud_service_type = cloud_service_type

        paginator = self.client.get_paginator('list_functions')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data['Functions']:
                try:
                    func = LambdaFunctionData(raw, strict=False)
                    func.region_name = region_name
                    func.account_id = self.account_id

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
                    if vpc_config := raw.get('VpcConfig'):
                        if vpc_data := self.get_vpc(vpc_config):
                            func.vpc_config = vpc_data
                    if env := raw.get('Environment'):
                        if not func.environment:
                            func.environment = Environment()
                        func.environment.variables = [
                            EnvironmentVariable({'key': k, 'value': v}) for k, v in env.get('Variables', {}).items()
                        ]

                    yield func, func.name
                except Exception as e:
                    resource_id = raw.get('FunctionArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield error_resource_response, ''

    def request_layer_data(self, region_name) -> List[Layer]:
        cloud_service_group = 'Lambda'
        cloud_service_type = 'Layer'
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
                        'account_id': self.account_id
                    })

                    yield Layer(raw, strict=False), raw.get('LayerName', '')
                except Exception as e:
                    resource_id = raw.get('LayerArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield error_resource_response, ''
