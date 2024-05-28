from spaceone.api.inventory.plugin import collector_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils

__all__ = ['PluginInfo', 'ResourceInfo']


def PluginInfo(result):
    result['metadata'] = change_struct_type(result['metadata'])
    return collector_pb2.PluginInfo(**result)


def ResourceInfo(resource_dict):
    if resource_dict['resource_type'] == 'inventory.CloudService':
        resource_dict['resource']['json_data'] = utils.dump_json(resource_dict['resource']['data'])
        resource_dict['resource']['json_metadata'] = utils.dump_json(resource_dict['resource']['metadata'])
        del resource_dict['resource']['data']
        del resource_dict['resource']['metadata']

    resource_dict.update({
        'resource': change_struct_type(resource_dict['resource'])
    })

    if 'match_rules' in resource_dict:
        resource_dict.update({
            'match_rules': change_struct_type(resource_dict['match_rules'])
        })

    return collector_pb2.ResourceInfo(**resource_dict)
