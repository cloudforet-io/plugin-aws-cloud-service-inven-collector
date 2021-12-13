import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

record_set_total_count_conf = os.path.join(current_dir, 'widget/record_set_total_count.yaml')
hosted_zone_count_per_account_conf = os.path.join(current_dir, 'widget/hosted_zone_count_per_account.yaml')
hosted_zone_count_per_type_conf = os.path.join(current_dir, 'widget/hosted_zone_count_per_type.yaml')
record_set_per_account_conf = os.path.join(current_dir, 'widget/record_set_per_account.yaml')

cst_hostedzone = CloudServiceTypeResource()
cst_hostedzone.name = 'HostedZone'
cst_hostedzone.provider = 'aws'
cst_hostedzone.group = 'Route53'
cst_hostedzone.labels = ['Networking']
cst_hostedzone.is_primary = True
cst_hostedzone.service_code = 'AmazonRoute53'
cst_hostedzone.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Route-53.svg',
}

cst_hostedzone._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Domain Name', 'name'),
        EnumDyField.data_source('Type', 'instance_type', default_badge={
            'indigo.500': ['Public'], 'coral.600': ['Private']
        }),
        TextDyField.data_source('Record Set Count', 'data.resource_record_set_count'),
        TextDyField.data_source('Comment', 'data.config.comment'),
        TextDyField.data_source('Host Zone ID', 'data.id'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Private Zone', 'data.config.private_zone', options={
            'is_optional': True
        }),
        TextDyField.data_source('Caller Reference', 'data.caller_reference', options={
            'is_optional': True
        }),
        ListDyField.data_source('Record Set Names', 'data.record_sets', options={
            'sub_key': 'name',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Record Set TTLs', 'data.record_sets', options={
            'sub_key': 'ttl',
            'delimiter': '<br>',
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Name', key='name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Type', key='instance_type'),
        SearchField.set(name='Host Zone ID', key='data.hosted_zone_id'),
        SearchField.set(name='Record Set Count', key='data.resource_record_set_count', data_type='integer'),
        SearchField.set(name='Record Name', key='data.record_sets.name')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(record_set_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(hosted_zone_count_per_account_conf)),
        ChartWidget.set(**get_data_from_yaml(hosted_zone_count_per_type_conf)),
        ChartWidget.set(**get_data_from_yaml(record_set_per_account_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_hostedzone}),
]
