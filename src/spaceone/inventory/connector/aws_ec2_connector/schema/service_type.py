from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_sg = CloudServiceTypeResource()
cst_sg.name = 'SecurityGroup'
cst_sg.provider = 'aws'
cst_sg.group = 'EC2'
cst_sg.labels = ['Compute', 'Security']
cst_sg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Gateway_dark-bg.svg',
    'spaceone:is_major': 'true',
}

cst_sg._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.group_id'),
        TextDyField.data_source('Name', 'data.group_name'),
        TextDyField.data_source('VPC ID', 'data.vpc_id'),
        TextDyField.data_source('Description', 'data.description'),
        TextDyField.data_source('Account ID', 'data.owner_id')
    ],
    search=[
        SearchField.set(name='Security Group ID', key='data.group_id'),
        SearchField.set(name='Name', key='data.group_name'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Inbound Protocol', key='data.ip_permissions.protocol_display'),
        SearchField.set(name='Inbound Port Rage', key='data.ip_permissions.port_display'),
        SearchField.set(name='Inbound Source', key='data.ip_permissions.source_display'),
        SearchField.set(name='Outbound Protocol', key='data.ip_permissions_egress.protocol_display'),
        SearchField.set(name='Outbound Port Rage', key='data.ip_permissions_egress.port_display'),
        SearchField.set(name='Outbound Source', key='data.ip_permissions_egress.source_display'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sg}),
]
