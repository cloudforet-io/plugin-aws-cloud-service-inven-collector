from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_elb_connector.schema.data import LoadBalancer, TargetGroup
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout

'''
LOAD BALANCER
'''
lb_base = ItemDynamicLayout.set_fields('Load Balancers', fields=[
    TextDyField.data_source('Name', 'data.load_balancer_name'),
    TextDyField.data_source('ARN', 'data.load_balancer_arn'),
    TextDyField.data_source('DNS Name', 'data.dns_name'),
    EnumDyField.data_source('State', 'data.state.code', default_state={
        'safe': ['active'],
        'warning': ['provisioning'],
        'alert': ['active_impaired', 'failed']
    }),
    EnumDyField.data_source('Type', 'data.type', default_badge={
        'indigo.500': ['network'], 'coral.600': ['application']
    }),
    EnumDyField.data_source('Scheme', 'data.scheme', default_badge={
        'indigo.500': ['internet-facing'], 'coral.600': ['internal']
    }),
    EnumDyField.data_source('IP address type', 'data.ip_address_type', default_outline_badge=['ipv4', 'dualstack']),
    TextDyField.data_source('VPC ID', 'data.vpc_id'),
    ListDyField.data_source('Availability Zones', 'data.availability_zones', default_badge={
        'type': 'outline',
        'sub_key': 'zone_name',
    }),
    TextDyField.data_source('Hosted Zone', 'data.canonical_hosted_zone_id'),
    DateTimeDyField.data_source('Creation time', 'data.created_time'),
])

lb_listener = TableDynamicLayout.set_fields('Listeners', 'data.listeners', fields=[
    EnumDyField.data_source('Protocol', 'protocol', default_outline_badge=['HTTP', 'HTTPS', 'TCP', 'TLS',
                                                                           'UDP', 'TCP_UDP']),
    TextDyField.data_source('Port', 'port'),
    ListDyField.data_source('Default Actions Target', 'default_actions', default_badge={
        'type': 'outline',
        'sub_key': 'target_group_arn'
    }),
    TextDyField.data_source('Security Policy', 'ssl_policy'),
    ListDyField.data_source('Certificates', 'certificates', default_badge={
        'type': 'outline',
        'sub_key': 'certificate_arn'
    })
])

lb_attr = ItemDynamicLayout.set_fields('Attributes', fields=[
    EnumDyField.data_source('Deletion protection', 'data.attributes.deletion_protection_enabled', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    }),
    EnumDyField.data_source('Cross-Zone Load Balancing', 'data.attributes.load_balancing_cross_zone_enabled', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    }),
    EnumDyField.data_source('Access logs', 'data.attributes.access_logs_s3_enabled', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    }),
    TextDyField.data_source('Access logs S3 Prefix', 'data.attributes.access_logs_s3_prefix'),
    TextDyField.data_source('Access logs S3 Bucket', 'data.attributes.access_logs_s3_bucket'),
])

lb_tags = SimpleTableDynamicLayout.set_tags()
lb_metadata = CloudServiceMeta.set_layouts(layouts=[lb_base, lb_listener, lb_attr, lb_tags])

'''
TARGET GROUP
'''
tg_base = ItemDynamicLayout.set_fields('Target Group', fields=[
    TextDyField.data_source('Name', 'data.target_group_name'),
    TextDyField.data_source('ARN', 'data.target_group_arn'),
    EnumDyField.data_source('Protocol', 'data.protocol',
                            default_outline_badge=['HTTP', 'HTTPS', 'TCP', 'TLS', 'UDP', 'TCP_UDP']),
    TextDyField.data_source('Port', 'data.port'),
    EnumDyField.data_source('Target Type', 'data.target_type',
                            default_outline_badge=['instance', 'ip', 'lambda']),
    TextDyField.data_source('VPC', 'data.vpc_id'),
    ListDyField.data_source('Load Balancer ARN', 'data.load_balancer_arns'),
])

tg_attr = ItemDynamicLayout.set_fields('Attributes', fields=[
    TextDyField.data_source('Deregistration Delay', 'data.attributes.deregistration_delay_timeout_seconds'),
    TextDyField.data_source('Slow start duration', 'data.attributes.slow_start_duration_seconds'),
    EnumDyField.data_source('Load balancing algorithm', 'data.attributes.load_balancing_algorithm_type',
                            default_outline_badge=['round_robin', 'least_outstanding_requests']),
    EnumDyField.data_source('Stickiness', 'data.attributes.stickiness_enabled', default_badge={
        'indigo.500': ['Enabled'], 'coral.600': ['Disabled']
    }),
    EnumDyField.data_source('Stickiness Type', 'data.attributes.stickiness_type',
                            default_outline_badge=['lb_cookie', 'source_ip']),
])

health_check = ItemDynamicLayout.set_fields('Health Check', fields=[
    EnumDyField.data_source('Health Check Protocol', 'data.health_check_protocol',
                            default_outline_badge=['HTTP', 'HTTPS', 'TCP', 'TLS', 'UDP', 'TCP_UDP']),
    TextDyField.data_source('Health Check Port', 'data.health_check_port'),
    EnumDyField.data_source('Health Check Enabled', 'data.health_check_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Health Check Interval Seconds', 'data.health_check_interval_seconds'),
    TextDyField.data_source('Health Check Timeout Seconds', 'data.health_check_timeout_seconds'),
    TextDyField.data_source('Health Check Threshold Count', 'data.healthy_threshold_count'),
    TextDyField.data_source('Unhealthy Threshold Count', 'data.unhealthy_threshold_count'),
    TextDyField.data_source('Health Check Path', 'data.health_check_path'),
])

tg_tags = SimpleTableDynamicLayout.set_tags()
tg_metadata = CloudServiceMeta.set_layouts(layouts=[tg_base, tg_attr, health_check, tg_tags])


class ELBResource(CloudServiceResource):
    cloud_service_group = StringType(default='ELB')


class LoadBalancerResource(ELBResource):
    cloud_service_type = StringType(default='LoadBalancer')
    data = ModelType(LoadBalancer)
    _metadata = ModelType(CloudServiceMeta, default=lb_metadata, serialized_name='metadata')


class TargetGroupResource(ELBResource):
    cloud_service_type = StringType(default='TargetGroup')
    data = ModelType(TargetGroup)
    _metadata = ModelType(CloudServiceMeta, default=tg_metadata, serialized_name='metadata')


class LoadBalancerResponse(CloudServiceResponse):
    resource = PolyModelType(LoadBalancerResource)


class TargetGroupResponse(CloudServiceResponse):
    resource = PolyModelType(TargetGroupResource)