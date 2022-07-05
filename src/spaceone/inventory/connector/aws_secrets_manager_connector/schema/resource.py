from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.connector.aws_secrets_manager_connector.schema.data import Secret
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout

secrets = ItemDynamicLayout.set_fields('Secrets', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('ARN', 'data.arn'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Encryption Key ID', 'data.kms_key_id'),
    TextDyField.data_source('Own Service', 'data.owning_service'),
    DateTimeDyField.data_source('Last Changed Date', 'data.last_changed_date'),
    DateTimeDyField.data_source('Last Accessed Date', 'data.last_accessed_date'),
])

rotation = ItemDynamicLayout.set_fields('Rotation Configuration', fields=[
    EnumDyField.data_source('Rotation Status', 'data.rotation_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Rotation Interval', 'data.rotation_rules'),
    TextDyField.data_source('AWS Lambda Function', 'data.rotation_lambda_arn'),
    DateTimeDyField.data_source('Last Rotated date', 'data.last_rotated_date'),
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[secrets, rotation, tags])


class SecretsManagerResource(CloudServiceResource):
    cloud_service_group = StringType(default='SecretsManager')


class SecretResource(SecretsManagerResource):
    cloud_service_type = StringType(default='Secret')
    data = ModelType(Secret)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class SecretResponse(CloudServiceResponse):
    resource = PolyModelType(SecretResource)
