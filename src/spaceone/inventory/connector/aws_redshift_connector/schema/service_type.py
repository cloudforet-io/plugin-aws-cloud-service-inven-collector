from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, BadgeDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_redshift_cluster = CloudServiceTypeResource()
cst_redshift_cluster.name = 'Cluster'
cst_redshift_cluster.provider = 'aws'
cst_redshift_cluster.group = 'Redshift'
cst_redshift_cluster.labels = ['Database', 'Analytics']
cst_redshift_cluster.is_primary = True
cst_redshift_cluster.is_major = True
cst_redshift_cluster.service_code = 'AmazonRedshift'
cst_redshift_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Redshift.svg'
}

cst_redshift_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Cluster', 'data.cluster_identifier'),
        EnumDyField.data_source('Status', 'data.cluster_status', default_state={
            'safe': ['available'],
            'warning': ['prep-for-resize', 'resize-cleanup', 'cancelling-resize', 'creating', 'deleting', 'final-snapshot',
                        'modifying', 'rebooting', 'renaming', 'resizing', 'rotating-keys', 'updating-hsm'],
            'disable': ['paused'],
            'alert': ['hardware-failure', 'incompatible-hsm', 'incompatible-network', 'incompatible-parameters',
                      'incompatible-restore', 'storage-full']
        }),
        TextDyField.data_source('Cluster Version', 'data.cluster_version'),
        TextDyField.data_source('Nodes', 'data.number_of_nodes'),
        BadgeDyField.data_source('Node Type', 'data.node_type'),
    ],
    search=[
        SearchField.set(name='Cluster Identifier', key='data.cluster_identifier'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Cluster Version', key='data.cluster_version'),
        SearchField.set(name='Node Type', key='data.node_type'),
        SearchField.set(name='Status', key='data.cluster_status',
                        enums={
                            "available": {'label': 'Available', 'icon': {'color': 'green.500'}},
                            "prep-for-resize": {'label': 'Prepare for Resize', 'icon': {'color': 'yellow.400'}},
                            "resize-cleanup": {'label': 'Resize Cleanup', 'icon': {'color': 'yellow.400'}},
                            "cancelling-resize": {'label': 'Cancelling Resize', 'icon': {'color': 'yellow.400'}},
                            "creating": {'label': 'Creating', 'icon': {'color': 'yellow.400'}},
                            "deleting": {'label': 'Deleting', 'icon': {'color': 'yellow.400'}},
                            "final-snapshot": {'label': 'Final Snapshot', 'icon': {'color': 'yellow.400'}},
                            "modifying": {'label': 'Modifying', 'icon': {'color': 'yellow.400'}},
                            "rebooting": {'label': 'Rebooting', 'icon': {'color': 'yellow.400'}},
                            "renaming": {'label': 'Renaming', 'icon': {'color': 'yellow.400'}},
                            "resizing": {'label': 'Resizing', 'icon': {'color': 'yellow.400'}},
                            "rotating-keys": {'label': 'Rotating Keys', 'icon': {'color': 'yellow.400'}},
                            "updating-hsm": {'label': 'Updating HSM', 'icon': {'color': 'yellow.400'}},
                            "hardware-failure": {'label': 'Hardware Failure', 'icon': {'color': 'red.500'}},
                            "incompatible-hsm": {'label': 'Incompatible HSM', 'icon': {'color': 'red.500'}},
                            "incompatible-network": {'label': 'Incompatible Network', 'icon': {'color': 'red.500'}},
                            "incompatible-parameters": {'label': 'Incompatible Parameters', 'icon': {'color': 'red.500'}},
                            "incompatible-restore": {'label': 'Incompatible Restore', 'icon': {'color': 'red.500'}},
                            "storage-full": {'label': 'Storage Full', 'icon': {'color': 'red.500'}},
                            "paused": {'label': 'Paused', 'icon': {'color': 'gray.400'}},
                        }),
        SearchField.set(name='DB Name', key='data.db_name'),
        SearchField.set(name='Endpoint', key='data.endpoint.address'),
        SearchField.set(name='Port', key='data.endpoint.port', data_type='integer'),
        SearchField.set(name='Security Group ID', key='data.vpc_security_groups.vpc_security_group_id'),
        SearchField.set(name='Parameter Group Name', key='data.cluster_parameter_groups.parameter_group_name'),
        SearchField.set(name='Subnet Group ID', key='data.cluster_subnet_group_name'),
        SearchField.set(name='VPC ID', key='data.vpc_id'),
        SearchField.set(name='Availability Zone', key='data.availability_zone'),
        SearchField.set(name='Node Counts', key='data.number_of_nodes', data_type='integer'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_redshift_cluster}),
]
