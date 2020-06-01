from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_eip = CloudServiceTypeResource()
cst_eip.name = 'EIP'
cst_eip.provider = 'aws'
cst_eip.group = 'EIP'
cst_eip.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2_Elastic-IP-Address_light-bg.svg',
    'spaceone:is_major': 'true',
}

cst_eip._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Public IP', 'data.public_ip'),
    TextDyField.data_source('Private IP', 'data.private_ip_address'),
    TextDyField.data_source('Address Pool', 'data.public_ipv4_pool'),
    EnumDyField.data_source('Scope', 'data.domain', default_outline_badge=['vpc', 'standard']),
    TextDyField.data_source('Associate Instance ID', 'data.instance_id'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_eip}),
]
