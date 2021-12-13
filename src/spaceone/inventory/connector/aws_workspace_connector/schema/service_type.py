from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeItemDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_distribution = CloudServiceTypeResource()
cst_distribution.name = 'Distribution'
cst_distribution.provider = 'aws'
cst_distribution.group = 'CloudFront'
cst_distribution.labels = ['Networking']
cst_distribution.tags = {
    'spaceone:icon': '',
    'spaceone:is_major': 'true',
}
cst_distribution._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.id'),
        TextDyField.data_source('Domain Name', 'data.domain_name'),
        TextDyField.data_source('Status', 'data.status'),
        ListDyField.data_source('CNAME', 'data.alias_icp_recordals', options={
            'item': BadgeItemDyField.set({'background_color': 'gray.200'}),
            'sub_key': 'network_interface_id',
            'delimiter': '  '
        }),
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Domain Name', key='data.domain_name'),
        SearchField.set(name='Status', key='data.status'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_distribution}),
]
