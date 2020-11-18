from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_ebs = CloudServiceTypeResource()
cst_ebs.name = 'Volume'
cst_ebs.provider = 'aws'
cst_ebs.group = 'EC2'
cst_ebs.labels = ['Compute', 'Storage']
cst_ebs.is_major = True
cst_ebs.service_code = 'AmazonEC2'
cst_ebs.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Block-Store-EBS.svg',
    'display_name': 'EBS'
}
cst_ebs._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Volume ID', 'data.volume_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['in-use'],
            'available': ['available'],
            'warning': ['deleting', 'creating'],
            'disable': ['deleted'],
            'alert': ['error']
        }),
        TextDyField.data_source('Size (GB)', 'data.size_gb'),
        EnumDyField.data_source('Volume Type', 'data.volume_type',
                                default_outline_badge=['standard', 'io1', 'gp2', 'sc1', 'st1']),
        TextDyField.data_source('IOPS', 'data.iops'),
        TextDyField.data_source('From Snapshot', 'data.snapshot_id'),
        TextDyField.data_source('Availablity Zone', 'data.availability_zone'),
        DateTimeDyField.data_source('Created', 'data.create_time'),
    ],
    search=[
        SearchField.set(name='Volume ID', key='data.volume_id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'in-use': {'label': 'in-use', 'icon': {'color': 'green.500'}},
                            'available': {'label': 'available', 'icon': {'color': 'blue.400'}},
                            'deleting': {'label': 'deleting', 'icon': {'color': 'yellow.500'}},
                            'creating': {'label': 'creating', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'deleted', 'icon': {'color': 'gray.400'}},
                            'error': {'label': 'error', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Size (GB)', key='data.size', data_type='integer'),
        SearchField.set(name='Volume Type', key='data.volume_type',
                        enums={
                            'gp2': {'label': 'General Purpose SSD (gp2)'},
                            'io1': {'label': 'Provisioned IOPS SSD (io1)'},
                            'sc1': {'label': 'Cold HDD (sc1)'},
                            'st1': {'label': 'Throughput Optimized HDD (st1)'},
                            'standard': {'label': 'Magnetic (standard)'},
                        }),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='IOPS', key='data.iops', data_type='integer'),
        SearchField.set(name='Created Time', key='data.create_time', data_type='datetime'),
        SearchField.set(name='Attached Instance ID', key='data.attachments.instance_id'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


cst_snapshot = CloudServiceTypeResource()
cst_snapshot.name = 'Snapshot'
cst_snapshot.provider = 'aws'
cst_snapshot.group = 'EC2'
cst_snapshot.labels = ['Compute', 'Storage']
cst_snapshot.service_code = 'AmazonEC2'
cst_snapshot.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Block-Store-EBS.svg',
}
cst_snapshot._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Snapshot ID', 'data.snapshot_id'),
        TextDyField.data_source('Size (GB)', 'data.volume_size'),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['completed'],
            'warning': ['pending'],
            'alert': ['error']
        }),
        TextDyField.data_source('Description', 'data.description'),
        TextDyField.data_source('Progress', 'data.progress'),
        EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        DateTimeDyField.data_source('Start Time', 'data.start_time'),
    ],
    search=[
        SearchField.set(name='Snapshot ID', key='data.snapshot_id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Status', key='data.state',
                        enums={
                            'completed': {'label': 'completed', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'pending', 'icon': {'color': 'yellow.500'}},
                            'error': {'label': 'error', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Size (GB)', key='data.volume_size', data_type='integer'),
        SearchField.set(name='Started Time', key='data.start_time', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ebs}),
    CloudServiceTypeResponse({'resource': cst_snapshot}),
]
