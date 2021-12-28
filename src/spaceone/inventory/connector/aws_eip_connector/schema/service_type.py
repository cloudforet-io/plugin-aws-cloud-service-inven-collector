import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
EIP
"""
eip_total_count_per_region_conf = os.path.join(current_dir, 'widget/eip_total_count_per_region.yaml')
eip_total_count_per_account_conf = os.path.join(current_dir, 'widget/eip_total_count_per_account.yaml')
eip_use_count_per_status_conf = os.path.join(current_dir, 'widget/eip_use_count_per_status.yaml')

cst_eip = CloudServiceTypeResource()
cst_eip.name = 'EIP'
cst_eip.provider = 'aws'
cst_eip.group = 'EC2'
cst_eip.labels = ['Networking', 'Compute']
cst_eip.is_major = True
cst_eip.service_code = 'AmazonEC2'
cst_eip.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2_Elastic-IP-Address_light-bg.svg',
}

cst_eip._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Public IP', 'data.public_ip'),
        TextDyField.data_source('Private IP', 'data.private_ip_address'),
        TextDyField.data_source('Address Pool', 'data.public_ipv4_pool'),
        EnumDyField.data_source('Scope', 'data.domain', default_outline_badge=['vpc', 'standard']),
        TextDyField.data_source('Associate Instance ID', 'data.instance_id'),
        TextDyField.data_source('Public DNS', 'data.public_dns', options={
            'is_optional': True
        }),
        TextDyField.data_source('NAT Gateway ID', 'data.nat_gateway_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Association ID', 'data.association_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Allocation ID', 'data.allocation_id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='IP Address', key='data.public_ip'),
        SearchField.set(name='Associated Instance ID', key='data.instance_id'),
        SearchField.set(name='Public DNS', key='data.public_dns'),
        SearchField.set(name='Private IP', key='data.private_ip_address'),
        SearchField.set(name='NAT Gateway ID', key='data.nat_gateway_id'),
        SearchField.set(name='Scope', key='data.domain',
                        enums={
                            'vpc': {'label': 'VPC'},
                            'standard': {'label': 'Standard'},
                        })
    ],
    widget=[
        ChartWidget.set(**get_data_from_yaml(eip_total_count_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(eip_total_count_per_account_conf)),
        ChartWidget.set(**get_data_from_yaml(eip_use_count_per_status_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_eip}),
]
