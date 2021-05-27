from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_asg = CloudServiceTypeResource()
cst_asg.name = 'AutoScalingGroup'
cst_asg.provider = 'aws'
cst_asg.group = 'EC2'
cst_asg.labels = ['Compute']
cst_asg.service_code = 'AmazonEC2'
cst_asg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
}

cst_asg._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.auto_scaling_group_name'),
        TextDyField.data_source('Desired', 'data.desired_capacity'),
        TextDyField.data_source('Min', 'data.min_size'),
        TextDyField.data_source('Max', 'data.max_size'),
        TextDyField.data_source('Launch Template / Configuration', 'data.display_launch_configuration_template'),
        ListDyField.data_source('AZ', 'data.availability_zones',
                                default_badge={'delimiter': '<br>'}),
        # For Dynamic Table
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Check Type', 'data.health_check_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Instance Protected from Scale In', 'data.new_instances_protected_from_scale_in',
                                options={'is_optional': True}),
        TextDyField.data_source('Default CoolDown (sec)', 'data.default_cooldown', options={
            'is_optional': True
        }),
        TextDyField.data_source('Health Check Grace Period (sec)', 'data.health_check_grace_period', options={
            'is_optional': True
        }),
        ListDyField.data_source('Instances ID', 'data.instances.instance_id', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Instances Lifecycle', 'data.instances.lifecycle', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Instances status', 'data.instances.health_status', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Instances type', 'data.instances.instance_type', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Instances type', 'data.instances.availability_zone', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('LoadBalancers ARNs', 'data.load_balancer_arns', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('LoadBalancers name', 'data.load_balancers.name', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('LoadBalancers endpoint', 'data.load_balancers.endpoint', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Target Group ARNs', 'data.target_group_arns', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Policy ARNs', 'data.policies.policy_arn', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Policy Names', 'data.policies.policy_name', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Name', key='data.auto_scaling_group_name'),
        SearchField.set(name='ARN', key='data.auto_scaling_group_arn'),
        SearchField.set(name='Launch Configuration Name', key='data.launch_configuration_name'),
        SearchField.set(name='Launch Configuration ARN', key='data.launch_configuration.launch_configuration_arn'),
        SearchField.set(name='Launch Template Name', key='data.launch_template.launch_template_name'),
        SearchField.set(name='Launch Template ID', key='data.launch_template.launch_template_id'),
        SearchField.set(name='Availability Zone', key='data.availability_zones'),
        SearchField.set(name='Instance ID', key='data.instances.instance_id'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

launch_configuration = CloudServiceTypeResource()
launch_configuration.name = 'LaunchConfiguration'
launch_configuration.provider = 'aws'
launch_configuration.group = 'EC2'
launch_configuration.labels = ['Compute']
launch_configuration.service_code = 'AmazonEC2'
launch_configuration.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
}

launch_configuration._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.launch_configuration_name'),
        TextDyField.data_source('AMI ID', 'data.image_id'),
        TextDyField.data_source('Instance Type', 'data.instance_type'),
        TextDyField.data_source('Spot Price', 'data.spot_price'),
        DateTimeDyField.data_source('Creation Time', 'data.created_time'),
        # For Dynamic Table
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Keypair name', 'data.key_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('IAM Instance Profile', 'data.iam_instance_profile', options={
            'is_optional': True
        }),
        TextDyField.data_source('IAM Instance Profile', 'data.iam_instance_profile', options={
            'is_optional': True
        }),
        ListDyField.data_source('Security Group IDs', 'data.security_groups', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('Image ID', 'data.image_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='Name', key='data.launch_configuration_name'),
        SearchField.set(name='ARN', key='data.launch_configuration_arn'),
        SearchField.set(name='AMI ID', key='data.image_id'),
        SearchField.set(name='Instance Type', key='data.instance_type'),
        SearchField.set(name='Monitoring', key='data.instance_monitoring.enabled', data_type='boolean'),
        SearchField.set(name='Security Group ID', key='data.security_groups'),
        SearchField.set(name='Created Time', key='data.created_time', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


launch_template = CloudServiceTypeResource()
launch_template.name = 'LaunchTemplate'
launch_template.provider = 'aws'
launch_template.group = 'EC2'
launch_template.labels = ['Compute']
launch_template.service_code = 'AmazonEC2'
launch_template.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
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
        # For Dynamic Table
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Launch Template ID', 'data.launch_template_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Version Description', 'data.version_description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Keypair name', 'data.launch_template_data.key_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('Instance Type', 'data.launch_template_data.instance_type', options={
            'is_optional': True
        }),
        ListDyField.data_source('Security Groups', 'data.launch_template_data.security_group_ids', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        }),
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
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_asg}),
    CloudServiceTypeResponse({'resource': launch_configuration}),
    CloudServiceTypeResponse({'resource': launch_template})
]