from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_hostedzone = CloudServiceTypeResource()
cst_hostedzone.name = 'HostedZone'
cst_hostedzone.provider = 'aws'
cst_hostedzone.group = 'Route53'
cst_hostedzone.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Route-53.svg',
    'spaceone:is_major': 'true',
}

cst_hostedzone._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Domain Name', 'data.name'),
        EnumDyField.data_source('Type', 'data.type', default_badge={
            'indigo.500': ['Public'], 'coral.600': ['Private']
        }),
        TextDyField.data_source('Record Set Count', 'data.resource_record_set_count'),
        TextDyField.data_source('Comment', 'data.config.comment'),
        TextDyField.data_source('Host Zone ID', 'data.id'),
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Type', key='data.type'),
        SearchField.set(name='Host Zone ID', key='data.hosted_zone_id'),
        SearchField.set(name='Record Set Count', key='data.resource_record_set_count', data_type='integer'),
        SearchField.set(name='Record Name', key='data.record_sets.name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_hostedzone}),
]
