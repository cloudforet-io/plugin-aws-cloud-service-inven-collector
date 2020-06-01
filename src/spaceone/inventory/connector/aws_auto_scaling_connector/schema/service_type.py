from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_asg = CloudServiceTypeResource()
cst_asg.name = 'AutoScalingGroup'
cst_asg.provider = 'aws'
cst_asg.group = 'AutoScaling'
cst_asg.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
    'spaceone:is_major': 'true',
}

cst_asg._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.auto_scaling_group_name'),
    TextDyField.data_source('Desired', 'data.desired_capacity'),
    TextDyField.data_source('Min', 'data.min_size'),
    TextDyField.data_source('Max', 'data.max_size'),
    TextDyField.data_source('Launch Configuration', 'data.launch_configuration_name'),
    ListDyField.data_source('AZ', 'data.availability_zones', default_badge={'type': 'outline'})
])

launch_configuration = CloudServiceTypeResource()
launch_configuration.name = 'LaunchConfiguration'
launch_configuration.provider = 'aws'
launch_configuration.group = 'AutoScaling'
launch_configuration.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg',
    'spaceone:is_major': 'false',
}

launch_configuration._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.launch_configuration_name'),
    TextDyField.data_source('AMI ID', 'data.image_id'),
    TextDyField.data_source('Instance Type', 'data.instance_type'),
    TextDyField.data_source('Spot Price', 'data.spot_price'),
    DateTimeDyField.data_source('Creation Time', 'data.created_time'),
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_asg}),
    CloudServiceTypeResponse({'resource': launch_configuration}),
]