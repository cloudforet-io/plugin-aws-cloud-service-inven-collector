from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_asg = CloudServiceTypeResource()
cst_asg.name = 'AutoScalingGroup'
cst_asg.provider = 'aws'
cst_asg.group = 'AutoScaling'
cst_asg.labels = ['Compute']
cst_asg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
    'spaceone:is_major': 'true',
}

cst_asg._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.auto_scaling_group_name'),
        TextDyField.data_source('Desired', 'data.desired_capacity'),
        TextDyField.data_source('Min', 'data.min_size'),
        TextDyField.data_source('Max', 'data.max_size'),
        TextDyField.data_source('Launch Configuration', 'data.launch_configuration_name'),
        ListDyField.data_source('AZ', 'data.availability_zones', default_badge={'type': 'outline'})
    ],
    search=[
        SearchField.set(name='Name', key='data.auto_scaling_group_name'),
        SearchField.set(name='ARN', key='data.auto_scaling_group_arn'),
        SearchField.set(name='Launch Configuration Name', key='data.launch_configuration_name'),
        SearchField.set(name='Availability Zone', key='data.availability_zones'),
        SearchField.set(name='Creation Time', key='data.created_time', data_type='datetime'),
        SearchField.set(name='Instance ID', key='data.instances.instance_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

launch_configuration = CloudServiceTypeResource()
launch_configuration.name = 'LaunchConfiguration'
launch_configuration.provider = 'aws'
launch_configuration.group = 'AutoScaling'
launch_configuration.labels = ['Compute']
launch_configuration.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
    'spaceone:is_major': 'false',
}

launch_configuration._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.launch_configuration_name'),
        TextDyField.data_source('AMI ID', 'data.image_id'),
        TextDyField.data_source('Instance Type', 'data.instance_type'),
        TextDyField.data_source('Spot Price', 'data.spot_price'),
        DateTimeDyField.data_source('Creation Time', 'data.created_time'),
    ],
    search=[
        SearchField.set(name='Name', key='data.launch_configuration_name'),
        SearchField.set(name='ARN', key='data.launch_configuration_arn'),
        SearchField.set(name='AMI ID', key='data.image_id'),
        SearchField.set(name='Instance Type', key='data.instance_type'),
        SearchField.set(name='Monitoring', key='data.instance_monitoring.enabled', data_type='boolean'),
        SearchField.set(name='Security Group ID', key='data.security_groups'),
        SearchField.set(name='Created Time', key='data.created_time', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


launch_template = CloudServiceTypeResource()
launch_template.name = 'LaunchTemplate'
launch_template.provider = 'aws'
launch_template.group = 'AutoScaling'
launch_template.labels = ['Compute']
launch_template.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
    'spaceone:is_major': 'false',
}

launch_template._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.launch_template_name'),
        TextDyField.data_source('AMI ID', 'data.launch_template_data.image_id'),
        TextDyField.data_source('Owner', 'data.created_by'),
        EnumDyField.data_source('Default Version', 'data.default_version', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        TextDyField.data_source('Version', 'data.version'),
        DateTimeDyField.data_source('Creation Time', 'data.create_time'),
    ],
    search=[
        SearchField.set(name='Name', key='data.launch_template_name'),
        SearchField.set(name='ID', key='data.launch_template_id'),
        SearchField.set(name='AMI ID', key='data.launch_template_data.image_id'),
        SearchField.set(name='Owner', key='data.created_by'),
        SearchField.set(name='Default Version', key='data.default_version', data_type='boolean'),
        SearchField.set(name='Versions', key='data.version'),
        SearchField.set(name='Instance Type', key='data.launch_template_data.instance_type'),
        SearchField.set(name='Monitoring', key='data.launch_template_data.monitoring.enabled', data_type='boolean'),
        SearchField.set(name='Security Group ID', key='data.launch_template_data.security_group_ids'),
        SearchField.set(name='Created Time', key='data.create_time', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_asg}),
    CloudServiceTypeResponse({'resource': launch_configuration}),
    CloudServiceTypeResponse({'resource': launch_template})
]