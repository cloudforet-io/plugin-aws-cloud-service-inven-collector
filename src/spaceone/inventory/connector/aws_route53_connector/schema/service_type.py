from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_hostedzone = CloudServiceTypeResource()
cst_hostedzone.name = 'HostedZone'
cst_hostedzone.provider = 'aws'
cst_hostedzone.group = 'Route53'
cst_hostedzone.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Route-53.svg',
    'spaceone:is_major': 'true',
}

cst_hostedzone._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Domain Name', 'data.name'),
    EnumDyField.data_source('Type', 'data.type', default_badge={
        'indigo.500': ['Public'], 'coral.600': ['Private']
    }),
    TextDyField.data_source('Record Set Count', 'data.resource_record_set_count'),
    TextDyField.data_source('Comment', 'data.config.comment'),
    TextDyField.data_source('Host Zone ID', 'data.id'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_hostedzone}),
]
