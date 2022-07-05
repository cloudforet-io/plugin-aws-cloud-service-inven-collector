import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, SearchField, SizeField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
FUNCTION
"""
total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
code_total_size_conf = os.path.join(current_dir, 'widget/code_total_size.yaml')
memory_total_size_conf = os.path.join(current_dir, 'widget/memory_total_size.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')
code_total_size_by_account_conf = os.path.join(current_dir, 'widget/code_total_size_by_account.yaml')
memory_total_size_by_account_conf = os.path.join(current_dir, 'widget/memory_total_size_by_account.yaml')
count_by_runtime_conf = os.path.join(current_dir, 'widget/count_by_runtime.yaml')

cst_function = CloudServiceTypeResource()
cst_function.name = 'Function'
cst_function.provider = 'aws'
cst_function.group = 'Lambda'
cst_function.labels = ['Compute']
cst_function.is_primary = True
cst_function.is_major = True
cst_function.service_code = 'AWSLambda'
cst_function.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Lambda.svg',
}

cst_function._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Runtime', 'data.runtime'),
        SizeField.data_source('Code Size', 'instance_size'),
        SizeField.data_source('Memory Size', 'data.memory_size', options={
            'source_unit': 'MB'
        }),
        TextDyField.data_source('Description', 'data.description'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Version', 'data.version', options={
            'is_optional': True
        }),
        TextDyField.data_source('Role ARN', 'data.role', options={
            'is_optional': True
        }),
        TextDyField.data_source('Handler', 'data.handler', options={
            'is_optional': True
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_config.vpc.id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Subnet IDs', 'data.vpc_config.subnets', options={
            'delimiter': '<br>',
            'sub_key': 'id',
            'is_optional': True
        }),
        ListDyField.data_source('Security Group IDs', 'data.vpc_config.security_groups', options={
            'delimiter': '<br>',
            'sub_key': 'id',
            'is_optional': True
        }),
        TextDyField.data_source('Code SHA256', 'data.code_sha256', options={
            'is_optional': True
        }),
        ListDyField.data_source('Layers ARN', 'data.layers', options={
            'delimiter': '<br>',
            'sub_key': 'arn',
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ARN', 'data.kms_key_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Dead Letter Target Name', 'data.dead_letter_config.target_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Dead Letter Target ARN', 'data.dead_letter_config.target_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Trace Config Mode', 'data.trace_config.mode', options={
            'is_optional': True
        }),
        TextDyField.data_source('Timeout', 'data.time_out', options={
            'is_optional': True
        }),
        TextDyField.data_source('Revision ID', 'data.revision_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Master ARN', 'data.master_arn', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Runtime', key='data.runtime'),
        SearchField.set(name='State', key='data.state.type',
                        enums={
                            "Active": {'label': 'Active', 'icon': {'color': 'green.500'}},
                            "Pending": {'label': 'Pending', 'icon': {'color': 'yellow.400'}},
                            "Inactive": {'label': 'Inactive', 'icon': {'color': 'gray.400'}},
                            "Failed": {'label': 'Failed', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Handler', key='data.handler'),
        SearchField.set(name='Memory Size (MB)', key='data.memory_size', data_type='integer'),
        SearchField.set(name='Timeout', key='data.time_out', data_type='integer'),
        SearchField.set(name='VPC ID', key='data.vpc_config.vpc.id'),
        SearchField.set(name='VPC Name', key='data.vpc_config.vpc.name'),
        SearchField.set(name='Subnet Id', key='data.vpc_config.subnets.id'),
        SearchField.set(name='Last Modified Time', key='data.last_modified', data_type='datetime'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(code_total_size_conf)),
        CardWidget.set(**get_data_from_yaml(memory_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_runtime_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(code_total_size_by_account_conf)),
        ChartWidget.set(**get_data_from_yaml(memory_total_size_by_account_conf)),
    ]
)

cst_layer = CloudServiceTypeResource()
cst_layer.name = 'Layer'
cst_layer.provider = 'aws'
cst_layer.group = 'Lambda'
cst_layer.labels = ['Compute']
cst_layer.service_code = 'AWSLambda'
cst_layer.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Lambda.svg',
}

cst_layer._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Version', 'data.latest_matching_version.version'),
        TextDyField.data_source('Description', 'data.latest_matching_version.description'),
        ListDyField.data_source('Compatible Runtimes', 'data.latest_matching_version.compatible_runtimes', options={
            'delimiter': '<br>'
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.layer_arn'),
        SearchField.set(name='Compatible Runtimes', key='data.latest_matching_version.compatible_runtimes'),
        SearchField.set(name='Version', key='data.version', data_type='integer')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_function}),
    CloudServiceTypeResponse({'resource': cst_layer})
]
