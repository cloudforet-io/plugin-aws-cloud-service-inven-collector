# -*- coding: utf-8 -*-
import time
import logging
from spaceone.core.service import *
from spaceone.inventory.libs.connector import *
import concurrent.futures


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType']
DEFAULT_REGION = 'ap-northeast-2'


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            'DynamoDBConnectorManager',
            'LambdaConnectorManager',
            'CloudFrontConnectorManager',
            'RDSConnectorManager',
            'Route53ConnectorManager',
            'S3ConnectorManager',
            'AutoScalingConnectorManager',
            # 'ElastiCacheConnectorManager',
            'APIGatewayConnectorManager',
            'APIGatewayV2ConnectorManager',
            'DirectConnectConnectorManager',
            # 'WorkSpaceConnectorManager',
            'EFSConnectorManager',
            'DocumentDBConnectorManager',
            'ECSConnectorManager',
            'RedshiftConnectorManager',
            'EKSConnectorManager',
            'SQSConnectorManager',
            'KMSConnectorManager',
            'ECRConnectorManager',
            'CloudTrailConnectorManager',
            'SNSConnectorManager',
            'SecretsManagerConnectorManager',
            'ELBConnectorManager',
            'EIPConnectorManager',
            'EBSConnectorManager',
            'VPCConnectorManager',
            'EC2ConnectorManager'
        ]

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        if secret_data != {}:
            self.get_account_id(secret_data)

        return {'options': {
            # 'filter_format':FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE
        }}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - secret_data
                - filter
        """

        secret_data = params['secret_data']

        params.update({
            'account_id': self.get_account_id(secret_data),
            'regions': self.get_regions(secret_data)
        })

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            print("[ EXECUTOR START ]")
            future_executors = []
            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, **params))

            for future in concurrent.futures.as_completed(future_executors):
                yield future.result()

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')

    @staticmethod
    def get_account_id(secret_data, region=DEFAULT_REGION):
        _session = get_session(secret_data, region)
        sts_client = _session.client('sts')
        return sts_client.get_caller_identity()['Account']

    @staticmethod
    def get_regions(secret_data):
        if 'region_name' in secret_data:
            return [secret_data.get('region_name')]
        else:
            _session = get_session(secret_data, DEFAULT_REGION)
            ec2_client = _session.client('ec2')
            return list(map(lambda region_info: region_info.get('RegionName'),
                            ec2_client.describe_regions().get('Regions')))
