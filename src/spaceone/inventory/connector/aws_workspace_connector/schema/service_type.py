from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeItemDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_distribution = CloudServiceTypeResource()
cst_distribution.name = 'Distribution'
cst_distribution.provider = 'aws'
cst_distribution.group = 'CloudFront'
cst_distribution.tags = {
    'spaceone:icon': '',
    'spaceone:is_major': 'true',
}
cst_distribution_meta = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Id', 'data.id'),
    TextDyField.data_source('Domain Name', 'data.domain_name'),
    TextDyField.data_source('Status', 'data.status'),
    ListDyField.data_source('CNAME', 'data.alias_icp_recordals', options={
        'item': BadgeItemDyField.set({'background_color': 'gray.200'}),
        'sub_key': 'network_interface_id',
        'delimiter': '  '
    }),
])
cst_distribution.cloud_service_type_meta = cst_distribution_meta


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_distribution}),
]
