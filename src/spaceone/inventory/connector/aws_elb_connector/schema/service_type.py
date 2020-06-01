from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, \
    DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_elb = CloudServiceTypeResource()
cst_elb.name = 'LoadBalancer'
cst_elb.provider = 'aws'
cst_elb.group = 'ELB'
cst_elb.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Elastic-Load-Balancing.svg',
    'spaceone:is_major': 'true',
}

cst_elb._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.load_balancer_name'),
    TextDyField.data_source('DNS Name', 'data.dns_name'),
    EnumDyField.data_source('State', 'data.state.code', default_state={
        'safe': ['active'],
        'warning': ['provisioning'],
        'alert': ['active_impaired', 'failed']
    }),
    EnumDyField.data_source('Type', 'data.type', default_badge={
        'indigo.500': ['network'], 'coral.600': ['application']
    }),
    ListDyField.data_source('Availability Zones', 'data.availability_zones', default_badge={
        'type': 'outline',
        'sub_key': 'zone_name',
    }),
    DateTimeDyField.data_source('Created At', 'data.created_time'),
])

cst_tg = CloudServiceTypeResource()
cst_tg.name = 'TargetGroup'
cst_tg.provider = 'aws'
cst_tg.group = 'ELB'
cst_tg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Elastic-Load-Balancing.svg',
    'spaceone:is_major': 'false',
}

cst_tg._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.target_group_name'),
    TextDyField.data_source('Port', 'data.port'),
    EnumDyField.data_source('Protocol', 'data.protocol',
                            default_outline_badge=['HTTP', 'HTTPS', 'TCP', 'TLS', 'UDP', 'TCP_UDP']),
    EnumDyField.data_source('Target Type', 'data.target_type',
                            default_outline_badge=['instance', 'ip', 'lambda']),
    ListDyField.data_source('Load Balancer', 'data.load_balancer_arns', default_badge={'type': 'outline'}),
    EnumDyField.data_source('Health Check', 'data.health_check_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),

])

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_elb}),
    CloudServiceTypeResponse({'resource': cst_tg}),
]
