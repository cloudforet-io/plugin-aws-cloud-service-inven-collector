from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_function = CloudServiceTypeResource()
cst_function.name = 'Function'
cst_function.provider = 'aws'
cst_function.group = 'Lambda'
cst_function.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Lambda.svg',
    'spaceone:is_major': 'true',
}

cst_function._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    BadgeDyField.data_source('Runtime', 'data.runtime'),
    TextDyField.data_source('Memory Size', 'data.memory_size'),
    TextDyField.data_source('Description', 'data.description'),

])

cst_layer = CloudServiceTypeResource()
cst_layer.name = 'Layer'
cst_layer.provider = 'aws'
cst_layer.group = 'Lambda'
cst_layer.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Lambda.svg',
    'spaceone:is_major': 'false',
}

cst_layer._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.layer_name'),
    TextDyField.data_source('Version', 'data.latest_matching_version.version'),
    TextDyField.data_source('Description', 'data.latest_matching_version.description'),
    ListDyField.data_source('Compatible Runtimes', 'data.latest_matching_version.compatible_runtimes', default_badge={
        'type': 'outline',
    }),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_function}),
    CloudServiceTypeResponse({'resource': cst_layer})
]
