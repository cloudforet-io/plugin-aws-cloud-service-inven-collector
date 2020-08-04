__all__ = ['PluginInfo', 'ResourceInfo']

import functools
from spaceone.api.inventory.plugin import collector_pb2
from spaceone.core.pygrpc.message_type import *


def PluginInfo(result):
    result['metadata'] = change_struct_type(result['metadata'])
    return collector_pb2.PluginInfo(**result)


def ResourceInfo(resource_dict):
    return collector_pb2.ResourceInfo(**resource_dict)
