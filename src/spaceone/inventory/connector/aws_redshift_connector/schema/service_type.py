from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, BadgeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_redshift_cluster = CloudServiceTypeResource()
cst_redshift_cluster.name = 'Cluster'
cst_redshift_cluster.provider = 'aws'
cst_redshift_cluster.group = 'RedShift'
cst_redshift_cluster.tags = {
    'spaceone:icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Redshift.svg',
    'spaceone:is_major': 'true',
}

cst_redshift_cluster._metadata = CloudServiceTypeMeta.set_fields(fields=[
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
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_redshift_cluster}),
]
