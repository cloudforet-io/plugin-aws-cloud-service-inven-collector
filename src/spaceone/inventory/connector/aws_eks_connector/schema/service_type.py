from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_eks_cluster = CloudServiceTypeResource()
cst_eks_cluster.name = 'Cluster'
cst_eks_cluster.provider = 'aws'
cst_eks_cluster.group = 'EKS'
cst_eks_cluster.labels = ['Container']
cst_eks_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Kubernetes-Service.svg',
    'spaceone:is_major': 'true',
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


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_eks_cluster}),
]
