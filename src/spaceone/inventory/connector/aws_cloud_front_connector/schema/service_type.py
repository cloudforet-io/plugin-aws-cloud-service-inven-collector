from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

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
        TextDyField.data_source('Id', 'data.id'),
        TextDyField.data_source('Domain Name', 'data.domain_name'),
        EnumDyField.data_source('Distribution Status', 'data.status', default_state={
            'safe': ['Deployed']
        }),
        ListDyField.data_source('CNAME', 'data.alias_icp_recordals', options={
            'sub_key': 'cname', 'delimiter': '<br>'
        }),
        EnumDyField.data_source('State', 'data.state_display', default_state={
            'safe': ['Enabled'],
            'alert': ['Disabled'],
        }),
    ],
    search=[
        SearchField.set(name='Distribution ID', key='data.id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Status', key='data.status',
                        enums={'Deployed': {'label': 'Deployed', 'icon': {'color': 'green.500'}}}),
        SearchField.set(name='Domain Name', key='data.domain_name'),
        SearchField.set(name='CNAME', key='data.alias_icp_recordals.cname'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_distribution}),
]
