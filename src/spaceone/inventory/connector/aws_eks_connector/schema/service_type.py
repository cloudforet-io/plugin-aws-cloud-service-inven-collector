from spaceone.inventory.libs.schema.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_eks_cluster = CloudServiceTypeResource()
cst_eks_cluster.name = 'Cluster'
cst_eks_cluster.provider = 'aws'
cst_eks_cluster.group = 'EKS'
cst_eks_cluster.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Kubernetes-Service.svg',
    'spaceone:is_major': 'true',
}

cst_eks_cluster._metadata = CloudServiceTypeMeta.set_fields(fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Version', 'data.version'),
    EnumDyField.data_source('Status', 'data.status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['CREATING', 'DELETING', 'UPDATING'],
        'alert': ['FAILED']
    })
])


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_eks_cluster}),
]
