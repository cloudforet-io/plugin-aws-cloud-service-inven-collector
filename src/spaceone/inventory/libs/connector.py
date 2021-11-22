import json
import logging
from functools import partial
from typing import List
from boto3.session import Session
from spaceone.core import utils
from spaceone.core.connector import BaseConnector
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, ReferenceModel, CloudWatchModel, \
    CloudServiceResourceTags, ErrorResourceResponse

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
        sts = session.client('sts')
        assume_role_object = sts.assume_role(RoleArn=role_arn, RoleSessionName=utils.generate_id('AssumeRoleSession'))
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

    def __init__(self, transaction, config={}, options={}, secret_data={}, region_id=None, zone_id=None, pool_id=None,
                 filter={}, **kwargs):
        super().__init__(transaction, config)
        self.options = options
        self.secret_data = secret_data
        self.region_id = region_id
        self.zone_id = zone_id
        self.pool_id = pool_id
        self.filter = filter
        self.account_id = kwargs.get('account_id')
        self.region_names = kwargs.get('regions', [])

    @property
    def session(self):
        return self.init_property('_session', partial(get_session, self.secret_data, self.region_name))

    def reset_region(self, region_name):
        self.region_name = region_name
        self._client = None
        self._session = None

    @property
    def init_client(self):
        if self._init_client is None:
            self._init_client = self.session.client('ec2')
        return self._init_client

    @property
    def client(self):
        if self._client is None:
            self._client = self.session.client(self.service_name)
        return self._client

    @staticmethod
    def generate_arn(partition=ARN_DEFAULT_PARTITION, service="", region="", account_id="", resource_type="", resource_id=""):
        return f'arn:{partition}:{service}:{region}:{account_id}:{resource_type}/{resource_id}'

    def set_client(self, service_name):
        self.service_name = service_name
        self._client = self.session.client(self.service_name)
        return self._client


class SchematicAWSConnector(AWSConnector):
    function_response_schema = CloudServiceResponse
    
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
        additional_data = ['name', 'type', 'size', 'avaiablity_zone', 'launched_at']

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
                        'tags': self.get_resource_tags(getattr(data, 'tags', [])),
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

    def get_resource_tags(self, tags_obj):
        return [CloudServiceResourceTags({'key': tag.key, 'value': tag.value}, strict=False) for tag in tags_obj]

    def generate_error(self, region_name, resource_id, error_message):
        _LOGGER.error(f'[generate_error] [{self.service_name}] [{region_name}] {error_message}')

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

    @staticmethod
    def convert_tags(tags):
        return [{'key': tag, 'value': tags[tag]} for tag in tags]
