import concurrent.futures
import logging
import time
import json
from spaceone.core.service import *
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.connector import *
from spaceone.inventory.libs.schema.resource import RegionResource, RegionResponse, ErrorResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

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

    def add_account_region_params(self, params):
        secret_data = params['secret_data']

        params.update({
            'account_id': self.get_account_id(secret_data),
            'regions': self.get_regions(secret_data)
        })

        return params

    def _get_target_execute_manger(self, options):
        if 'cloud_service_types' in options:
            execute_managers = self._match_execute_manager(options['cloud_service_types'])
        else:
            execute_managers = list(CLOUD_SERVICE_GROUP_MAP.values())

        return execute_managers

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def collect(self, params):
        """
        Args:
            params:
                - options
                - secret_data
                - filter
        """
        start_time = time.time()
        resource_regions = []
        collected_region_code = []
        target_execute_managers = self._get_target_execute_manger(params.get('options', {}))

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []

            for execute_manager in target_execute_managers:
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, **params))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    try:
                        if getattr(result, 'resource', None) and getattr(result.resource, 'region_code', None):
                            collected_region = self.get_region_from_result(result.resource.region_code)

                            if collected_region and collected_region.resource.region_code not in collected_region_code:
                                resource_regions.append(collected_region)
                                collected_region_code.append(collected_region.resource.region_code)

                    except Exception as e:
                        _LOGGER.error(f'[collect] {e}')

                        if type(e) is dict:
                            error_resource_response = ErrorResourceResponse(
                                {'message': json.dumps(e), 'resource': {'resource_type': 'inventory.Region'}})
                        else:
                            error_resource_response = ErrorResourceResponse(
                                {'message': str(e), 'resource': {'resource_type': 'inventory.Region'}})

                        yield error_resource_response

                    yield result

        # ## This code for test without async job
        # for execute_manager in self.execute_managers:
        #     print(f'@@@ {execute_manager} @@@')
        #     _manager = self.locator.get_manager(execute_manager)
        #     result = _manager.collect_resources(**params)

        _LOGGER.debug(f'[collect] TOTAL FINISHED TIME : {time.time() - start_time} Seconds')
        for resource_region in resource_regions:
            yield resource_region

    def get_region_from_result(self, region_code):
        region_resource = self.match_region_info(region_code)

        if region_resource:
            return RegionResponse({'resource': region_resource})

        return None

    @staticmethod
    def _match_execute_manager(cloud_service_groups):
        return [CLOUD_SERVICE_GROUP_MAP[_cloud_service_group] for _cloud_service_group in cloud_service_groups
                if _cloud_service_group in CLOUD_SERVICE_GROUP_MAP]

    @staticmethod
    def get_account_id(secret_data, region=DEFAULT_REGION):
        _session = get_session(secret_data, region)
        sts_client = _session.client('sts')
        return sts_client.get_caller_identity()['Account']

    @staticmethod
    def get_regions(secret_data):
        _session = get_session(secret_data, DEFAULT_REGION)
        ec2_client = _session.client('ec2')
        return list(map(lambda region_info: region_info.get('RegionName'),
                        ec2_client.describe_regions().get('Regions')))

    @staticmethod
    def match_region_info(region_name):
        match_region_info = REGION_INFO.get(region_name, None)
        if match_region_info is not None:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': region_name
            })

            return RegionResource(region_info, strict=False)

        return None
