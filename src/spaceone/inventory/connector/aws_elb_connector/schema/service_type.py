from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, \
    DateTimeDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_elb = CloudServiceTypeResource()
cst_elb.name = 'LoadBalancer'
cst_elb.provider = 'aws'
cst_elb.group = 'ELB'
cst_elb.labels = ['Networking']
cst_elb.is_primary = True
cst_elb.is_major = True
cst_elb.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Elastic-Load-Balancing.svg',
}

cst_elb._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
    ],
    search=[
        SearchField.set(name='Name', key='data.load_balancer_name'),
        SearchField.set(name='ARN', key='data.load_balancer_arn'),
        SearchField.set(name='DNS Name', key='data.dns_name'),
        SearchField.set(name='State', key='data.state'),
        SearchField.set(name='Type', key='data.type',
                        enums={
                            'application': {'label': 'Application'},
                            'network': {'label': 'Network'},
                        }),
        SearchField.set(name='Scheme', key='data.scheme',
                        enums={
                            'internet-facing': {'label': 'Internet Facing'},
                            'internal': {'label': 'Internal'},
                        }),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Availability Zone', key='data.availability_zones.zone_name'),
        SearchField.set(name='Subnet ID', key='data.availability_zones.subnet_id'),
        SearchField.set(name='Hosted Zone', key='data.canonical_hosted_zone_id'),
        SearchField.set(name='Protocol', key='data.listeners.protocol',
                        enums={
                            'HTTP': {'label': 'HTTP'},
                            'HTTPS': {'label': 'HTTPS'},
                            'TCP': {'label': 'TCP'},
                            'UDP': {'label': 'UDP'},
                            'TLS': {'label': 'TLS'},
                            'TCP_UDP': {'label': 'TCP/UDP'},
                        }),
        SearchField.set(name='Port', key='data.listeners.port', data_type='integer'),
        SearchField.set(name='Deletion Protection', key='data.attributes.deletion_protection_enabled',
                        data_type='boolean'),
        SearchField.set(name='Cross-Zone Load Balancing', key='data.attributes.load_balancing_cross_zone_enabled',
                        data_type='boolean'),
        SearchField.set(name='Security Group ID', key='data.security_groups'),
        SearchField.set(name='Listener ARN', key='data.listeners.listener_arn'),
        SearchField.set(name='Created Time', key='data.created_time', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_tg = CloudServiceTypeResource()
cst_tg.name = 'TargetGroup'
cst_tg.provider = 'aws'
cst_tg.group = 'ELB'
cst_tg.labels = ['Networking']
cst_tg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Elastic-Load-Balancing.svg',
}

cst_tg._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
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
    ],
    search=[
        SearchField.set(name='Name', key='data.target_group_name'),
        SearchField.set(name='ARN', key='data.'),
        SearchField.set(name='Protocol', key='data.protocol',
                        enums={
                            'HTTP': {'label': 'HTTP'},
                            'HTTPS': {'label': 'HTTPS'},
                            'TCP': {'label': 'TCP'},
                            'UDP': {'label': 'UDP'},
                            'TLS': {'label': 'TLS'},
                            'TCP_UDP': {'label': 'TCP/UDP'},
                        }),
        SearchField.set(name='Port', key='data.port', data_type='integer'),
        SearchField.set(name='Target Type', key='data.target_type',
                        enums={
                            'instance': {'label': 'Instance'},
                            'ip': {'label': 'IP'},
                            'lambda': {'label': 'Lambda'},
                        }),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Stickiness', key='data.attributes.stickiness_enabled',
                        enums={
                            'Enabled': {'label': 'Enabled'},
                            'Disabled': {'label': 'Disabled'}
                        }),
        SearchField.set(name='Stickiness Type', key='data.attributes.stickiness_type',
                        enums={
                            'lb_cookie': {'label': 'LB Cookie'},
                            'source_ip': {'label': 'Source IP'}
                        }),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_elb}),
    CloudServiceTypeResponse({'resource': cst_tg}),
]
