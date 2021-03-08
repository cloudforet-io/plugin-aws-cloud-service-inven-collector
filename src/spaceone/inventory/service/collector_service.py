import concurrent.futures
import logging
import time

from spaceone.core.service import *

from spaceone.inventory.libs.connector import *
from spaceone.inventory.libs.schema.resource import RegionResource, RegionResponse

_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
DEFAULT_REGION = 'ap-northeast-2'
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            # 'IAMConnectorManager',
            # 'DynamoDBConnectorManager',
            # 'LambdaConnectorManager',
            # 'CloudFrontConnectorManager',
            # 'RDSConnectorManager',
            # 'Route53ConnectorManager',
            # 'S3ConnectorManager',
            # 'AutoScalingConnectorManager',
            'ElastiCacheConnectorManager',
            # 'APIGatewayConnectorManager',
            # 'DirectConnectConnectorManager',
            # # 'WorkSpaceConnectorManager',
            # 'EFSConnectorManager',
            # 'DocumentDBConnectorManager',
            # 'ECSConnectorManager',
            # 'RedshiftConnectorManager',
            # 'EKSConnectorManager',
            # 'SQSConnectorManager',
            # 'KMSConnectorManager',
            # 'ECRConnectorManager',
            # 'CloudTrailConnectorManager',
            # 'SNSConnectorManager',
            # 'SecretsManagerConnectorManager',
            # 'ELBConnectorManager',
            # 'EIPConnectorManager',
            # 'EBSConnectorManager',
            # 'VPCConnectorManager',
            # 'EC2ConnectorManager',
            # 'ACMConnectorManager',
            # 'KinesisDataStreamConnectorManager',
            # 'MSKConnectorManager',
            # 'KinesisFirehoseConnectorManager'
        ]

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

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

        return {}

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
        resource_regions = []
        collected_region_code = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            print("[ EXECUTOR START ]")
            future_executors = []

            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, **params))

            for future in concurrent.futures.as_completed(future_executors):
                try:
                    for result in future.result():
                        collected_region = self.get_region_from_result(result.get('resource', {}))
                        if collected_region is not None and \
                                collected_region.get('resource', {}).get('region_code') not in collected_region_code:
                            resource_regions.append(collected_region)
                            collected_region_code.append(collected_region.get('resource', {}).get('region_code'))

                        yield result
                except Exception as e:
                    _LOGGER.error(f'failed to result {e}')

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')
        for resource_region in resource_regions:
            yield resource_region

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

    def get_region_from_result(self, resource):
        region_resource = self.match_region_info(resource.get('data', {}).get('region_name', None))

        if region_resource is not None:
            return RegionResponse({'resource': region_resource}).to_primitive(())

        return None

    @staticmethod
    def match_region_info(region_name):
        REGION_INFO = {
            'us-east-1': {'name': 'US East (N. Virginia)',
                          'tags': {'latitude': '39.028760', 'longitude': '-77.458263'}},
            'us-east-2': {'name': 'US East (Ohio)', 'tags': {'latitude': '40.103564', 'longitude': '-83.200092'}},
            'us-west-1': {'name': 'US West (N. California)',
                          'tags': {'latitude': '37.242183', 'longitude': '-121.783380'}},
            'us-west-2': {'name': 'US West (Oregon)', 'tags': {'latitude': '45.841046', 'longitude': '-119.658093'}},
            'af-south-1': {'name': 'Africa (Cape Town)', 'tags': {'latitude': '-33.932268', 'longitude': '18.424434'}},
            'ap-east-1': {'name': 'Asia Pacific (Hong Kong)',
                          'tags': {'latitude': '22.365560', 'longitude': '114.119420'}},
            'ap-south-1': {'name': 'Asia Pacific (Mumbai)',
                           'tags': {'latitude': '19.147428', 'longitude': '73.013805'}},
            'ap-northeast-3': {'name': 'Asia Pacific (Osaka-Local)',
                               'tags': {'latitude': '34.675638', 'longitude': '135.495706'}},
            'ap-northeast-2': {'name': 'Asia Pacific (Seoul)',
                               'tags': {'latitude': '37.528547', 'longitude': '126.871867'}},
            'ap-southeast-1': {'name': 'Asia Pacific (Singapore)',
                               'tags': {'latitude': '1.321259', 'longitude': '103.695942'}},
            'ap-southeast-2	': {'name': 'Asia Pacific (Sydney)',
                                   'tags': {'latitude': '-33.921423', 'longitude': '151.188076'}},
            'ap-northeast-1': {'name': 'Asia Pacific (Tokyo)',
                               'tags': {'latitude': '35.648411', 'longitude': '139.792566'}},
            'ca-central-1': {'name': 'Canada (Central)', 'tags': {'latitude': '43.650803', 'longitude': '-79.361824'}},
            'cn-north-1': {'name': 'China (Beijing)', 'tags': {'latitude': '39.919635', 'longitude': '116.307237'}},
            'cn-northwest-1': {'name': 'China (Ningxia)', 'tags': {'latitude': '37.354511', 'longitude': '106.106147'}},
            'eu-central-1': {'name': 'Europe (Frankfurt)', 'tags': {'latitude': '50.098645', 'longitude': '8.632262'}},
            'eu-west-1': {'name': 'Europe (Ireland)', 'tags': {'latitude': '53.330893', 'longitude': '-6.362217'}},
            'eu-west-2': {'name': 'Europe (London)', 'tags': {'latitude': '51.519749', 'longitude': '-0.087804'}},
            'eu-south-1': {'name': 'Europe (Milan)', 'tags': {'latitude': '45.448648', 'longitude': '9.147316'}},
            'eu-west-3': {'name': 'Europe (Paris)', 'tags': {'latitude': '48.905302', 'longitude': '2.369778'}},
            'eu-north-1': {'name': 'Europe (Stockholm)', 'tags': {'latitude': '59.263542', 'longitude': '18.104861'}},
            'me-south-1': {'name': 'Middle East (Bahrain)',
                           'tags': {'latitude': '26.240945', 'longitude': '50.586321'}},
            'sa-east-1': {'name': 'South America (São Paulo)',
                          'tags': {'latitude': '-23.493549', 'longitude': '-46.809319'}},
            'us-gov-east-1': {'name': 'AWS GovCloud (US-East)'},
            'us-gov-west-1': {'name': 'AWS GovCloud (US)'},
            'global': {'name': 'Global'}
        }

        match_region_info = REGION_INFO.get(region_name, None)
        if match_region_info is not None:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': region_name
            })

            return RegionResource(region_info, strict=False)

        return None
