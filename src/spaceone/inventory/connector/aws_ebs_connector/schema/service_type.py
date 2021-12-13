import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, DateTimeDyField, \
    SizeField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))


"""
VOLUME
"""
vol_total_size_conf = os.path.join(current_dir, 'widget/vol_total_size.yaml')
vol_total_size_per_region_conf = os.path.join(current_dir, 'widget/vol_total_size_per_region.yaml')
vol_total_size_per_account_conf = os.path.join(current_dir, 'widget/vol_total_size_per_account.yaml')
vol_total_size_per_az_conf = os.path.join(current_dir, 'widget/vol_total_size_per_az.yaml')
vol_total_size_per_type_conf = os.path.join(current_dir, 'widget/vol_total_size_per_type.yaml')
vol_total_size_per_state_conf = os.path.join(current_dir, 'widget/vol_total_size_per_state.yaml')

cst_ebs = CloudServiceTypeResource()
cst_ebs.name = 'Volume'
cst_ebs.provider = 'aws'
cst_ebs.group = 'EC2'
cst_ebs.labels = ['Compute', 'Storage']
cst_ebs.is_primary = True
cst_ebs.is_major = True
cst_ebs.service_code = 'AmazonEC2'
cst_ebs.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Block-Store-EBS.svg',
    'spaceone:display_name': 'EBS'
}
cst_ebs._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Volume ID', 'data.volume_id'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['in-use'],
            'available': ['available'],
            'warning': ['deleting', 'creating'],
            'disable': ['deleted'],
            'alert': ['error']
        }),
        SizeField.data_source('Size', 'instance_size'),
        TextDyField.data_source('Volume Type', 'instance_type'),
        TextDyField.data_source('IOPS', 'data.iops'),
        TextDyField.data_source('From Snapshot', 'data.snapshot_id'),
        TextDyField.data_source('Availablity Zone', 'data.availability_zone'),
        DateTimeDyField.data_source('Created', 'data.create_time'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encrypted', 'data.encrypted', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Multi Attach Enabled', 'data.multi_attach_enabled', options={
            'is_optional': True
        }),
        ListDyField.data_source('Attached Instance ID', 'data.attachments', options={
            'sub_key': 'instance_id',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'data.account_id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Volume ID', key='data.volume_id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='State', key='data.state',
                        enums={
                            'in-use': {'label': 'in-use', 'icon': {'color': 'green.500'}},
                            'available': {'label': 'available', 'icon': {'color': 'blue.400'}},
                            'deleting': {'label': 'deleting', 'icon': {'color': 'yellow.500'}},
                            'creating': {'label': 'creating', 'icon': {'color': 'yellow.500'}},
                            'deleted': {'label': 'deleted', 'icon': {'color': 'gray.400'}},
                            'error': {'label': 'error', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Size (Bytes)', key='instance_size', data_type='integer'),
        SearchField.set(name='Size (GB)', key='data.size_gb', data_type='integer'),
        SearchField.set(name='Volume Type', key='instance_type',
                        enums={
                            'gp2': {'label': 'General Purpose SSD (gp2)'},
                            'gp3': {'label': 'General Purpose SSD (gp3)'},
                            'io1': {'label': 'Provisioned IOPS SSD (io1)'},
                            'sc1': {'label': 'Cold HDD (sc1)'},
                            'st1': {'label': 'Throughput Optimized HDD (st1)'},
                            'standard': {'label': 'Magnetic (standard)'},
                        }),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='IOPS', key='data.iops', data_type='integer'),
        SearchField.set(name='Attached Instance ID', key='data.attachments.instance_id'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(vol_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_per_account_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_per_az_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_per_type_conf)),
        ChartWidget.set(**get_data_from_yaml(vol_total_size_per_state_conf))
    ]
)

"""
SNAPSHOT
"""
snapshot_total_size_conf = os.path.join(current_dir, 'widget/snapshot_total_size.yaml')
snapshot_total_count_per_region_conf = os.path.join(current_dir, 'widget/snapshot_total_count_per_region.yaml')
snapshot_total_count_per_account_conf = os.path.join(current_dir, 'widget/snapshot_total_count_per_account.yaml')
snapshot_total_size_per_region_conf = os.path.join(current_dir, 'widget/snapshot_total_size_per_region.yaml')
snapshot_total_size_per_account_conf = os.path.join(current_dir, 'widget/snapshot_total_size_per_account.yaml')

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
        TextDyField.data_source('Name', 'name'),
        TextDyField.data_source('Snapshot ID', 'data.snapshot_id'),
        SizeField.data_source('Size', 'instance_size', options={
            'source_unit': 'GB',
            'display_unit': 'GB'
        }),
        EnumDyField.data_source('Status', 'data.state', default_state={
            'safe': ['completed'],
            'warning': ['pending'],
            'alert': ['error']
        }),
        TextDyField.data_source('Progress', 'data.progress'),
        EnumDyField.data_source('Encryption', 'data.encrypted', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Encrypted', 'data.encrypted', options={
            'is_optional': True
        }),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Snapshot ID', key='data.snapshot_id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Status', key='data.state',
                        enums={
                            'completed': {'label': 'completed', 'icon': {'color': 'green.500'}},
                            'pending': {'label': 'pending', 'icon': {'color': 'yellow.500'}},
                            'error': {'label': 'error', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Size (GB)', key='instance_size', data_type='integer'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(snapshot_total_size_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_total_count_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_total_count_per_account_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_total_size_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(snapshot_total_size_per_account_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ebs}),
    CloudServiceTypeResponse({'resource': cst_snapshot}),
]
