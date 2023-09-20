import json
import logging
import datetime
from functools import partial
from typing import List
from boto3.session import Session
from spaceone.core import utils
from spaceone.core.connector import BaseConnector
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, ReferenceModel, CloudWatchModel, \
    ErrorResourceResponse, CloudTrailModel, CloudWatchDimension, CloudWatchMetricInfo

_LOGGER = logging.getLogger(__name__)

DEFAULT_REGION = 'us-east-1'
ARN_DEFAULT_PARTITION = 'aws'
REGIONS = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ap-south-1', 'ap-northeast-2',
           'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1',
           'eu-west-2', 'eu-west-3', 'eu-north-1', 'sa-east-1']


def get_session(secret_data, region_name):
    params = {
        'aws_access_key_id': secret_data['aws_access_key_id'],
        'aws_secret_access_key': secret_data['aws_secret_access_key'],
        'region_name': region_name
    }

    session = Session(**params)

    # ASSUME ROLE
    if role_arn := secret_data.get('role_arn'):
        sts = session.client('sts', verify=BOTO3_HTTPS_VERIFIED)

        _assume_role_request = {
            'RoleArn': role_arn,
            'RoleSessionName': utils.generate_id('AssumeRoleSession'),
        }

        if external_id := secret_data.get('external_id'):
            _assume_role_request.update({'ExternalId': external_id})

        assume_role_object = sts.assume_role(**_assume_role_request)
        credentials = assume_role_object['Credentials']

        assume_role_params = {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'region_name': region_name,
            'aws_session_token': credentials['SessionToken']
        }
        session = Session(**assume_role_params)
    return session


class AWSConnector(BaseConnector):
    service_name = ''
    _session = None
    _client = None
    _init_client = None
    account_id = None
    region_name = DEFAULT_REGION
    region_names = []

    def init_property(self, name: str, init_data: callable):
        if self.__getattribute__(name) is None:
            self.__setattr__(name, init_data())
        return self.__getattribute__(name)

    def __init__(self, config={}, options={}, secret_data={}, region_id=None, zone_id=None, pool_id=None,
                 filter={}, **kwargs):

        super().__init__(config=config, **kwargs)
        self.options = options
        self.secret_data = secret_data
        self.region_id = region_id
        self.zone_id = zone_id
        self.pool_id = pool_id
        self.filter = filter
        self.account_id = kwargs.get('account_id')
        self.region_names = kwargs.get('regions', [])

    def reset_region(self, region_name):
        self.region_name = region_name
        self._client = None
        self._session = None

    def set_client(self, service_name):
        self.service_name = service_name
        self._client = self.session.client(self.service_name, verify=BOTO3_HTTPS_VERIFIED)
        return self._client

    @property
    def session(self):
        return self.init_property('_session', partial(get_session, self.secret_data, self.region_name))

    @property
    def init_client(self):
        if self._init_client is None:
            self._init_client = self.session.client('ec2', verify=BOTO3_HTTPS_VERIFIED)
        return self._init_client

    @property
    def client(self):
        if self._client is None:
            self._client = self.session.client(self.service_name, verify=BOTO3_HTTPS_VERIFIED)
        return self._client

    @staticmethod
    def generate_arn(partition=ARN_DEFAULT_PARTITION, service="", region="", account_id="", resource_type="", resource_id=""):
        return f'arn:{partition}:{service}:{region}:{account_id}:{resource_type}/{resource_id}'

    @staticmethod
    def divide_to_chunks(resources, n):
        """
         For some API parameters, there is a limit to the number that can be described at one time.
         This method divides the list value of a resource by a certain number and divides it.
         The "resources" argument is a list value of resources, and divides it into a list of "n" arguments.
        """
        for i in range(0, len(resources), n):
            yield resources[i:i + n]


class SchematicAWSConnector(AWSConnector):
    function_response_schema = CloudServiceResponse
    cloud_service_types = []

    cloud_service_group = ''
    cloud_service_type = ''

    def get_resources(self) -> List[CloudServiceResponse]:
        raise NotImplementedError()

    def collect_data(self):
        return self.get_resources()

    def collect_data_by_region(self, service_name, region_name, collect_resource_info):
        '''
        collect_resource_info = {
            'request_method': self.request_something_like_data,
            'resource': ResourceClass,
            'response_schema': ResponseClass,
            'kwargs': {}
        }
        '''
        resources = []
        additional_data = ['name', 'type', 'size', 'launched_at']

        try:
            for collected_dict in collect_resource_info['request_method'](region_name, **collect_resource_info.get('kwargs', {})):
                data = collected_dict['data']
    
                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:
                    # Cloud Service Resource
                    if getattr(data, 'set_cloudwatch', None):
                        data.cloudwatch = CloudWatchModel(data.set_cloudwatch(region_name))
    
                    resource_dict = {
                        'data': data,
                        'account': collected_dict.get('account'),
                        'instance_size': float(collected_dict.get('instance_size', 0)),
                        'instance_type': collected_dict.get('instance_type', ''),
                        'launched_at': str(collected_dict.get('launched_at', '')),
                        'tags': collected_dict.get('tags', {}),
                        'region_code': region_name,
                        'reference': ReferenceModel(data.reference(region_name))
                    }

                    for add_field in additional_data:
                        if add_field in collected_dict:
                            resource_dict.update({add_field: collected_dict[add_field]})
    
                    resources.append(collect_resource_info['response_schema'](
                        {'resource': collect_resource_info['resource'](resource_dict)}))
        except Exception as e:
            resource_id = ''
            error_resource_response = self.generate_error(region_name, resource_id, e)
            resources.append(error_resource_response)
            
        return resources

    def generate_error(self, region_name, resource_id, error_message):
        _LOGGER.error(f'[generate_error] [{self.service_name}] [{region_name}] {error_message}', exc_info=True)

        if type(error_message) is dict:
            error_resource_response = ErrorResourceResponse(
                {'message': json.dumps(error_message),
                 'resource': {'resource_id': resource_id,
                              'cloud_service_group': self.cloud_service_group,
                              'cloud_service_type': self.cloud_service_type}})
        else:
            error_resource_response = ErrorResourceResponse(
                {'message': str(error_message),
                 'resource': {'resource_id': resource_id,
                              'cloud_service_group': self.cloud_service_group,
                              'cloud_service_type': self.cloud_service_type}})

        return error_resource_response

    def set_cloud_service_types(self):
        if 'service_code_mappers' in self.options:
            svc_code_maps = self.options['service_code_mappers']

            for cst in self.cloud_service_types:
                if getattr(cst.resource, 'service_code') and cst.resource.service_code in svc_code_maps:
                    cst.resource.service_code = svc_code_maps[cst.resource.service_code]

        if 'custom_asset_url' in self.options:
            for cst in self.cloud_service_types:
                _tags = cst.resource.tags

                if 'spaceone:icon' in _tags:
                    _icon = _tags['spaceone:icon']
                    _tags['spaceone:icon'] = f'{self.options["custom_asset_url"]}/{_icon.split("/")[-1]}'

        return self.cloud_service_types

    @staticmethod
    def datetime_to_iso8601(value: datetime.datetime):
        if isinstance(value, datetime.datetime):
            value = value.replace(tzinfo=None)
            return f"{value.isoformat(timespec='seconds')}TZD"

        return None

    @staticmethod
    def set_cloudtrail(region_name, resource_type, resource_name):
        cloudtrail = {
            'LookupAttributes': [
                {
                    "AttributeKey": "ResourceName",
                    "AttributeValue": resource_name,
                }
            ],
            'region_name': region_name,
            'resource_type': resource_type
        }

        return CloudTrailModel(cloudtrail, strict=False)

    def set_cloudwatch(self, namespace, dimension_name, resource_id, region_name):
        '''
        data.cloudwatch: {
            "metrics_info": [
                {
                    "Namespace": "AWS/XXXX",
                    "Dimensions": [
                        {
                            "Name": "XXXXX",
                            "Value": "i-xxxxxx"
                        }
                    ]
                }
            ]
            "region_name": region_name
        }
        '''

        cloudwatch_data = {
            'region_name': region_name,
            'metrics_info': self.set_metrics_info(namespace, dimension_name, resource_id)
        }

        return CloudWatchModel(cloudwatch_data, strict=False)

    def set_metrics_info(self, namespace, dimension_name, resource_id):
        metric_info = {'Namespace': namespace}

        if dimension_name:
            metric_info.update({'Dimensions': self.set_dimensions(dimension_name, resource_id)})

        return [CloudWatchMetricInfo(metric_info, strict=False)]

    @staticmethod
    def set_dimensions(dimension_name, resource_id):
        dimension = {
            'Name': dimension_name,
            'Value': resource_id
        }

        return [CloudWatchDimension(dimension, strict=False)]

    @staticmethod
    def convert_tags_to_dict_type(tags, key='Key', value='Value'):
        dict_tags = {}

        for _tag in tags:
            dict_tags[_tag.get(key)] = _tag.get(value)

        return dict_tags
