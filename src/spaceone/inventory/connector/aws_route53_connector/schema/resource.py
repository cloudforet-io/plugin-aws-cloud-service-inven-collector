from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_route53_connector.schema.data import HostedZone
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout

hosted_zone = ItemDynamicLayout.set_fields('Hosted Zones', fields=[
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('Type', 'data.type', default_badge={
        'indigo.500': ['Public'], 'coral.600': ['Private']
    }),
    TextDyField.data_source('Host Zone ID', 'data.id'),
    TextDyField.data_source('Record Set Count', 'data.resource_record_set_count'),
    TextDyField.data_source('Comment', 'data.config.comment'),
])

record_set = TableDynamicLayout.set_fields('Record Sets', 'data.record_sets', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Type', 'type', default_outline_badge=['SOA', 'A', 'TXT', 'NS', 'CNAME', 'MX', 'NAPTR',
                                                                   'PTR', 'SRV', 'SPF', 'AAAA', 'CAA']),
    ListDyField.data_source('Value', 'display_values', default_badge={
        'type': 'outline',
        'delimiter': '<br>'
    }),
    EnumDyField.data_source('Evaluate Target Health', 'alias_target.evaluate_target_health', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Health Check ID', 'health_check_id'),
    TextDyField.data_source('TTL', 'ttl'),
    TextDyField.data_source('Region', 'region'),
    TextDyField.data_source('Weight', 'weight'),
    TextDyField.data_source('Geolocation', 'geo_location'),
    EnumDyField.data_source('Multivalue Answer', 'multi_value_answer', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Set ID', 'set_identifier'),
])

metadata = CloudServiceMeta.set_layouts(layouts=[hosted_zone, record_set])


class Route53Resource(CloudServiceResource):
    cloud_service_group = StringType(default='Route53')


class HostedZoneResource(Route53Resource):
    cloud_service_type = StringType(default='HostedZone')
    data = ModelType(HostedZone)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class HostedZoneResponse(CloudServiceResponse):
    resource = PolyModelType(HostedZoneResource)
