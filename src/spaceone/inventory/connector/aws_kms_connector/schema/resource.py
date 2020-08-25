from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_kms_connector.schema.data import Key
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField, \
    DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

base = ItemDynamicLayout.set_fields('Keys', fields=[
    TextDyField.data_source('ID', 'data.key_id'),
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Alias', 'data.alias_name'),
    EnumDyField.data_source('Enabled', 'data.enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Key Status', 'data.key_state', default_state={
        'safe': ['Enabled'],
        'warning': ['PendingDeletion', 'PendingImport'],
        'disable': ['Disabled'],
        'alert': ['Unavailable']
    }),
    TextDyField.data_source('Description', 'data.description'),
    ListDyField.data_source('Key Algorithms', 'data.encryption_algorithms', default_badge={
        'type': 'outline'
    }),
    ListDyField.data_source('Signing Algorithms', 'data.signing_algorithms', default_badge={
        'type': 'outline'
    }),
    EnumDyField.data_source('Origin', 'data.origin', default_outline_badge=['AWS_KMS', 'EXTERNAL', 'AWS_CLOUDHSM']),
    EnumDyField.data_source('Key Manager', 'data.key_manager', default_outline_badge=['AWS', 'CUSTOMER']),
    EnumDyField.data_source('CMK Auto Rotation', 'data.key_rotated', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Key Usage', 'data.key_usage', default_outline_badge=['SIGN_VERIFY', 'ENCRYPT_DECRYPT']),
    EnumDyField.data_source('Expiration Model', 'data.expiration_model',
                            default_outline_badge=['KEY_MATERIAL_EXPIRES', 'KEY_MATERIAL_DOES_NOT_EXPIRE']),
    EnumDyField.data_source('Custom Master Key Spec.', 'data.customer_master_key_spec',
                            default_outline_badge=['RSA_2048', 'RSA_3072', 'RSA_4096', 'ECC_NIST_P256',
                                                   'ECC_NIST_P384', 'ECC_NIST_P521', 'ECC_SECG_P256K1',
                                                   'SYMMETRIC_DEFAULT']),
    TextDyField.data_source('Custom Key Store ID', 'data.custom_key_store_id'),
    TextDyField.data_source('Cloud HSM Cluster ID', 'data.cloud_hsm_cluster_id'),
    DateTimeDyField.data_source('Creation Time', 'data.creation_date')
])

metadata = CloudServiceMeta.set_layouts(layouts=[base])


class KMSResource(CloudServiceResource):
    cloud_service_group = StringType(default='KMS')


class KeyResource(KMSResource):
    cloud_service_type = StringType(default='Key')
    data = ModelType(Key)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class KeyResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(KeyResource)
