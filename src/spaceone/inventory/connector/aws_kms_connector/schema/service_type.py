import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_account_conf = os.path.join(current_dir, 'widget/count_by_account.yaml')

cst_kms_cluster = CloudServiceTypeResource()
cst_kms_cluster.name = 'Key'
cst_kms_cluster.provider = 'aws'
cst_kms_cluster.group = 'KMS'
cst_kms_cluster.labels = ['Security']
cst_kms_cluster.is_primary = True
cst_kms_cluster.service_code = 'awskms'
cst_kms_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Key-Management-Service.svg',
}

cst_kms_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.key_id'),
        TextDyField.data_source('Alias', 'name'),
        EnumDyField.data_source('Status', 'data.key_state', default_state={
            'safe': ['Enabled'],
            'warning': ['PendingDeletion', 'PendingImport'],
            'disable': ['Disabled'],
            'alert': ['Unavailable']
        }),
        EnumDyField.data_source('Enabled', 'data.enabled', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Usage', 'data.key_usage', options={
            'is_optional': True
        }),
        TextDyField.data_source('Origin', 'data.origin', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Roated', 'data.key_rotated', options={
            'is_optional': True
        }),
        TextDyField.data_source('Customer Master Key Spec.', 'data.customer_master_key_spec', options={
            'is_optional': True
        }),
        TextDyField.data_source('Custom Key ID', 'data.custom_key_store_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Signing Algorithms', 'data.signing_algorithms', options={
            'is_optional': True
        }),
        TextDyField.data_source('Cloud HSM Cluster ID', 'data.cloud_hsm_cluster_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Encryption Algorithms', 'data.encryption_algorithms', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('Key Type Path', 'data.key_type_path', options={
            'is_optional': True
        }),
        TextDyField.data_source('Key Manager', 'data.key_manager', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='KMS ID', key='data.key_id'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Alias', key='name'),
        SearchField.set(name='Enabled', key='data.enabled', data_type='boolean'),
        SearchField.set(name='Key Status', key='data.key_state',
                        enums={
                            "Enabled": {'label': 'Enabled', 'icon': {'color': 'green.500'}},
                            "Disabled": {'label': 'Disabled', 'icon': {'color': 'gray.400'}},
                            "PendingDeletion": {'label': 'Pending Deletion', 'icon': {'color': 'yellow.500'}},
                            "PendingImport": {'label': 'Pending Import', 'icon': {'color': 'yellow.500'}},
                            "Unavailable": {'label': 'Unavailable', 'icon': {'color': 'red.500'}}
                        }),
        SearchField.set(name='Key Algorithms', key='data.encryption_algorithms'),
        SearchField.set(name='Origin', key='data.origin',
                        enums={
                            'AWS_KMS': {'label': 'KMS'},
                            'EXTERNAL': {'label': 'EXTERNAL'},
                            'AWS_CLOUDHSM': {'label': 'CLOUD HSM'},
                        }),
        SearchField.set(name='Key Manager', key='data.key_manager',
                        enums={
                            'AWS': {'label': 'AWS'},
                            'CUSTOMER': {'label': 'CUSTOMER'},
                        })
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(key_count_per_region_conf)),
        ChartWidget.set(**get_data_from_yaml(key_count_per_account_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_kms_cluster}),
]
