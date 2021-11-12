import logging
import traceback

from spaceone.api.inventory.plugin import collector_pb2_grpc, collector_pb2
from spaceone.core.pygrpc import BaseAPI
from spaceone.core.pygrpc.message_type import *
from spaceone.inventory.service import CollectorService

_LOGGER = logging.getLogger(__name__)


class Collector(BaseAPI, collector_pb2_grpc.CollectorServicer):
    pb2 = collector_pb2
    pb2_grpc = collector_pb2_grpc

    def init(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('CollectorService', metadata) as collector_svc:
            data = collector_svc.init(params)
            return self.locator.get_info('PluginInfo', data)

    def verify(self, request, context):
        params, metadata = self.parse_request(request, context)

        collector_svc: CollectorService = self.locator.get_service('CollectorService', metadata)

        with collector_svc:
            collector_svc.verify(params)
            return self.locator.get_info('EmptyInfo')

    def collect(self, request, context):
        params, metadata = self.parse_request(request, context)
        collector_svc: CollectorService = self.locator.get_service('CollectorService', metadata)

        params = collector_svc.add_account_region_params(params)

        with collector_svc:
            try:
                for resource in collector_svc.collect(params):
                    res = {
                        'state': (resource['state']),
                        'message': '',
                        'resource_type': (resource['resource_type']),
                        'match_rules': change_struct_type(resource['match_rules']),
                        'resource': change_struct_type(resource['resource'])
                    }

                    yield self.locator.get_info('ResourceInfo', res)

            except Exception as e:
                _LOGGER.error(f'[ERROR: ResourceInfo]: {e}')




