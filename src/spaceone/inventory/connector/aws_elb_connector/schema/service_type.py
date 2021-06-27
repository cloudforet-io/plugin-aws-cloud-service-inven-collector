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
cst_elb.service_code = 'AWSELB'
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
        ListDyField.data_source('Availability Zones', 'data.availability_zones', options={
            'sub_key': 'zone_name',
            'delimiter': '<br>'
        }),
        DateTimeDyField.data_source('Created At', 'data.created_time'),
        TextDyField.data_source('ARN', 'data.load_balancer_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Scheme', 'data.scheme', options={
            'is_optional': True
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Subnet ID', 'data.availability_zones', options={
            'delimiter': '<br>',
            'sub_key': 'subnet_id',
            'is_optional': True
        }),
        ListDyField.data_source('Availability Zone', 'data.availability_zones', options={
            'delimiter': '<br>',
            'sub_key': 'zone_name',
            'is_optional': True
        }),
        TextDyField.data_source('Hosted Zone ID', 'data.canonical_hosted_zone_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Security Groups', 'data.security_group', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Listener IDs', 'data.listeners', options={
            'delimiter': '<br>',
            'sub_key': 'listener_arn',
            'is_optional': True
        }),
        ListDyField.data_source('Protocols', 'data.listeners', options={
            'delimiter': '<br>',
            'sub_key': 'protocol',
            'is_optional': True
        }),
        ListDyField.data_source('Ports', 'data.listeners', options={
            'delimiter': '<br>',
            'sub_key': 'port',
            'is_optional': True
        }),
        TextDyField.data_source('IP Address Type', 'data.ip_address_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Log S3 Bucket', 'data.attributes.access_logs_s3_bucket', options={
            'is_optional': True
        }),
        TextDyField.data_source('Routing HTTP2 Enabled', 'data.attributes.routing_http2_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Idel Timeout Seconds', 'data.attributes.idle_timeout_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Routing HTTP Drop Invalid Header Fields Enabled',
                                'data.attributes.routing_http_drop_invalid_header_fields_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('WAF Fail Open Enabled',
                                'data.attributes.waf_fail_open_enabled', options={
                'is_optional': True
        }),
        TextDyField.data_source('Deletion Protection Enabled',
                                'data.attributes.deletion_protection_enabled', options={
                'is_optional': True
        }),
        TextDyField.data_source('Routing HTTP Desync Mitigation Mode',
                                'data.attributes.routing_http_desync_mitigation_mode', options={
                'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Cross Zone Enabled',
                                'data.attributes.load_balancing_cross_zone_enabled', options={
                'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        })
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
        SearchField.set(name='Target Group ARN', key='data.target_groups.target_group_arn'),
        SearchField.set(name='Target Group Name', key='data.target_groups.target_group_name'),
        SearchField.set(name='Instance ID', key='data.instances.instance_id'),
        SearchField.set(name='Instance Name', key='data.instances.instance_name'),
        SearchField.set(name='Instance State', key='data.instances.state'),
        SearchField.set(name='Created Time', key='data.created_time', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_tg = CloudServiceTypeResource()
cst_tg.name = 'TargetGroup'
cst_tg.provider = 'aws'
cst_tg.group = 'ELB'
cst_tg.labels = ['Networking']
cst_tg.service_code = 'AWSELB'
cst_tg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Elastic-Load-Balancing.svg',
}

cst_tg._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.target_group_name'),
        TextDyField.data_source('Port', 'data.port'),
        TextDyField.data_source('Protocol', 'data.protocol'),
        TextDyField.data_source('Target Type', 'data.target_type'),
        ListDyField.data_source('Load Balancers', 'data.load_balancer_arns', options={
            'delimiter': '<br>'
        }),
        EnumDyField.data_source('Health Check', 'data.health_check_enabled', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        TextDyField.data_source('ARN', 'data.target_group_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('VPC ID', 'data.vpc_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Healthy Threshold Count', 'data.healthy_threshold_count', options={
            'is_optional': True
        }),
        TextDyField.data_source('Unhealthy Threshold Count', 'data.unhealthy_threshold_count', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Check Enabled', 'data.health_check_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Check Timeout Seconds', 'data.health_check_timeout_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Check Interval Seconds', 'data.health_check_interval_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Deregistration Delay Timeout Seconds', 'data.deregistration_delay_timeout_seconds',
                                options={'is_optional': True}),
        TextDyField.data_source('Slow Start Duration Seconds', 'data.slow_start_duration_seconds', options={
            'is_optional': True
        }),
        TextDyField.data_source('Stickiness Enabled', 'data.stickiness_enabled', options={
            'is_optional': True
        }),
        TextDyField.data_source('Stickiness Type', 'data.stickiness_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Load Balancing Algorithm Type', 'data.load_balancing_algorithm_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Stickiness LB Cookie Duration Seconds', 'data.stickiness_lb_cookie_duration_seconds',
                                options={'is_optional': True}),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        })
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
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_elb}),
    CloudServiceTypeResponse({'resource': cst_tg}),
]
