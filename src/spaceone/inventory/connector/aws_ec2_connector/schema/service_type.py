from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_sg = CloudServiceTypeResource()
cst_sg.name = 'SecurityGroup'
cst_sg.provider = 'aws'
cst_sg.group = 'EC2'
cst_sg.labels = ['Compute', 'Security']
cst_sg.service_code = 'AmazonEC2'
cst_sg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-VPC_VPN-Gateway_dark-bg.svg',
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

cst_ami = CloudServiceTypeResource()
cst_ami.name = 'AMI'
cst_ami.provider = 'aws'
cst_ami.group = 'EC2'
cst_ami.labels = ['Compute']
cst_ami.service_code = 'AmazonEC2'
cst_ami.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-AMI.svg',
}

cst_ami._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.image_id'),
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Source', 'data.image_location'),
        TextDyField.data_source('Owner', 'data.owner_id'),
        EnumDyField.data_source('Is Public', 'data.public', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['available'],
            'warning': ['pending', 'transient', 'deregistered', 'invalid'],
            'alert': ['error', 'failed']
        }),
        DateTimeDyField.data_source('Creation Date', 'data.creation_date'),
        TextDyField.data_source('Platform', 'data.platform'),
        TextDyField.data_source('Root Device Type', 'data.root_device_type'),
        TextDyField.data_source('Virtualization', 'data.virtualization_type'),
        TextDyField.data_source('Architecture', 'data.architecture', options={
            'is_optional': True
        }),
        TextDyField.data_source('Virtualization Type', 'data.virtualization_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Root Device Name', 'data.root_device_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Root Device Type', 'data.root_device_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('SR-IOV Net Support ', 'data.sriov_net_support', options={
            'is_optional': True
        }),
        TextDyField.data_source('Hypervisor ', 'data.hypervisor', options={
            'is_optional': True
        }),
        TextDyField.data_source('Platform Details ', 'data.platform_details', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='AMI ID', key='data.image_id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Status', key='data.state'),
        SearchField.set(name='Source', key='data.image_location'),
        SearchField.set(name='Owner', key='data.owner_id'),
        SearchField.set(name='Is Public', key='data.public', data_type='boolean'),
        SearchField.set(name='Platform', key='data.platform'),
        SearchField.set(name='Root Device Type', key='data.root_device_type'),
        SearchField.set(name='Virtualization', key='data.virtualization_type'),
        SearchField.set(name='Creation Date', key='data.creation_date', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sg}),
    CloudServiceTypeResponse({'resource': cst_ami}),
]
