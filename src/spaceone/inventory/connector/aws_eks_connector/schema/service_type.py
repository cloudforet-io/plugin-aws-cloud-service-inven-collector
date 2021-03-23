from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_eks_cluster = CloudServiceTypeResource()
cst_eks_cluster.name = 'Cluster'
cst_eks_cluster.provider = 'aws'
cst_eks_cluster.group = 'EKS'
cst_eks_cluster.labels = ['Container', 'Compute']
cst_eks_cluster.is_primary = True
cst_eks_cluster.is_major = True
cst_eks_cluster.service_code = 'AmazonEKS'
cst_eks_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Kubernetes-Service.svg',
}

cst_eks_cluster._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Version', 'data.version'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['ACTIVE'],
            'warning': ['CREATING', 'DELETING', 'UPDATING'],
            'alert': ['FAILED']
        })
    ],
    search=[
        SearchField.set(name='Cluster Name', key='data.name'),
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='Status', key='data.status',
                        enums={
                            'ACTIVE': {'label': 'ACTIVE', 'icon': {'color': 'green.500'}},
                            'CREATING': {'label': 'CREATING', 'icon': {'color': 'yellow.500'}},
                            'UPDATING': {'label': 'UPDATING', 'icon': {'color': 'yellow.500'}},
                            'DELETING': {'label': 'DELETING', 'icon': {'color': 'yellow.500'}},
                            'FAILED': {'label': 'FAILED', 'icon': {'color': 'red.500'}},
                        }),
        SearchField.set(name='Cluster Version', key='data.version'),
        SearchField.set(name='Cluster Endpoint', key='data.endpoint'),
        SearchField.set(name='Created Time', key='data.created_at', data_type='datetime'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

cst_eks_nodegrp = CloudServiceTypeResource()
cst_eks_nodegrp.name = 'NodeGroup'
cst_eks_nodegrp.provider = 'aws'
cst_eks_nodegrp.group = 'EKS'
cst_eks_nodegrp.labels = ['Container', 'Compute']
cst_eks_nodegrp.service_code = 'AmazonEKS'
cst_eks_nodegrp.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Kubernetes-Service.svg',
}

cst_eks_nodegrp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Node Group Name', 'data.nodegroup_name'),
        TextDyField.data_source('EKS Cluster Name', 'data.cluster_name'),
        TextDyField.data_source('Version', 'data.version'),
        EnumDyField.data_source('Status', 'data.status', default_state={
            'safe': ['ACTIVE'],
            'warning': ['CREATING', 'UPDATING', 'DELETING'],
            'alert': ['CREATE_FAILED', 'DELETE_FAILED', 'DEGRADED'],
        }),
        ListDyField.data_source('Instance Types', 'data.instance_types', options={
            'delimiter': '<br>'
        })
    ],
    search=[
        SearchField.set(name='Node Group Name', key='data.nodegroup_name'),
        SearchField.set(name='Node Group ARN', key='data.nodegroup_arn'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='EKS Cluster Name', key='data.cluster_name'),
        SearchField.set(name='EKS Cluster ARN', key='data.cluster_arn'),
        SearchField.set(name='Version', key='data.version'),
        SearchField.set(name='Instance Type', key='data.instance_types'),
        SearchField.set(name='Subnet', key='data.subnets'),
        SearchField.set(name='Node Role', key='data.node_role'),
        SearchField.set(name='Disk Size', key='data.disk_size', data_type='integer'),
        SearchField.set(name='Creation Time', key='data.created_at', data_type='datetime'),
        SearchField.set(name='Modification Time', key='data.modified_at', data_type='datetime'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_eks_cluster}),
    CloudServiceTypeResponse({'resource': cst_eks_nodegrp}),

]
