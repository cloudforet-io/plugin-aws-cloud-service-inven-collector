from spaceone.inventory.libs.schema.dynamic_field import TextDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_sg = CloudServiceTypeResource()
cst_sg.name = 'SecurityGroup'
cst_sg.provider = 'aws'
cst_sg.group = 'EC2'
cst_sg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Gateway_dark-bg.svg',
    'spaceone:is_major': 'true',
}

cst_sg._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('ID', 'data.group_id'),
    TextDyField.data_source('Name', 'data.group_name'),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Account ID', 'data.owner_id'),
])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sg}),
]
