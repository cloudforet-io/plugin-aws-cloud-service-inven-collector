import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_widget_conf = os.path.join(current_dir, 'widget/total_count.yaml')
origin_total_widget_conf = os.path.join(current_dir, 'widget/origin_total_count.yaml')
count_by_account_widget_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')
count_by_region_widget_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_distribution_status_widget_conf = os.path.join(current_dir, 'widget/count_by_distribution_status.yaml')

cst_distribution = CloudServiceTypeResource()
cst_distribution.name = 'Distribution'
cst_distribution.provider = 'aws'
cst_distribution.group = 'CloudFront'
cst_distribution.labels = ['Networking']
cst_distribution.is_primary = True
cst_distribution.is_major = True
cst_distribution.service_code = 'AmazonCloudFront'
cst_distribution.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-CloudFront.svg',
}

cst_distribution._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Distribution Status', 'data.status', default_state={
            'safe': ['Deployed']
        }),
        ListDyField.data_source('CNAME', 'data.alias_icp_recordals', options={
            'sub_key': 'cname', 'delimiter': '<br>'
        }),
        EnumDyField.data_source('Status', 'data.state_display', default_state={
            'safe': ['Enabled'],
            'alert': ['Disabled'],
        }),
        # For Dynamic Table
        TextDyField.data_source('Id', 'data.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Comment', 'data.comment', options={
            'is_optional': True
        }),
        TextDyField.data_source('Price Class', 'data.price_class', options={
            'is_optional': True
        }),
        TextDyField.data_source('HTTP Version', 'data.http_version', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Distribution ID', key='data.id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Status', key='data.status',
                        enums={'Deployed': {'label': 'Deployed', 'icon': {'color': 'green.500'}}}),
        SearchField.set(name='CNAME', key='data.alias_icp_recordals.cname'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_widget_conf)),
        CardWidget.set(**get_data_from_yaml(origin_total_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_account_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_distribution_status_widget_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_widget_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_distribution}),
]
