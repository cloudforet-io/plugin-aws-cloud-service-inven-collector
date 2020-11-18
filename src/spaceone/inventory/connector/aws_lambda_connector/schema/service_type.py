from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, ListDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

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
        TextDyField.data_source('Name', 'data.name'),
        BadgeDyField.data_source('Runtime', 'data.runtime'),
        TextDyField.data_source('Memory Size', 'data.memory_size'),
        TextDyField.data_source('Description', 'data.description'),
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
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
        SearchField.set(name='Code Size', key='data.code_size', data_type='integer'),
        SearchField.set(name='Memory Size', key='data.memory_size', data_type='integer'),
        SearchField.set(name='Timeout', key='data.time_out', data_type='integer'),
        SearchField.set(name='VPC ID', key='data.vpc_config.vpc.id'),
        SearchField.set(name='VPC Name', key='data.vpc_config.vpc.name'),
        SearchField.set(name='Subnet Id', key='data.vpc_config.subnets.id'),
        SearchField.set(name='Last Modified Time', key='data.last_modified', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
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
        TextDyField.data_source('Name', 'data.layer_name'),
        TextDyField.data_source('Version', 'data.latest_matching_version.version'),
        TextDyField.data_source('Description', 'data.latest_matching_version.description'),
        ListDyField.data_source('Compatible Runtimes', 'data.latest_matching_version.compatible_runtimes', default_badge={
            'type': 'outline',
        }),
    ],
    search=[
        SearchField.set(name='Name', key='data.layer_name'),
        SearchField.set(name='ARN', key='data.layer_arn'),
        SearchField.set(name='Compatible Runtimes', key='data.latest_matching_version.compatible_runtimes'),
        SearchField.set(name='Version', key='data.version', data_type='integer'),
        SearchField.set(name='Created Time', key='data.latest_matching_version.created_date', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_function}),
    CloudServiceTypeResponse({'resource': cst_layer})
]
