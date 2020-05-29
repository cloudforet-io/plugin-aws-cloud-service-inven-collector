from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_sns_connector.schema.data import Topic
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

sns = ItemDynamicLayout.set_fields('SNS', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Display Name', 'data.display_name'),
    TextDyField.data_source('ARN', 'data.topic_arn'),
    TextDyField.data_source('Topic Owner', 'data.owner'),
])

subscription = TableDynamicLayout.set_fields('Subscriptions', 'data.subscriptions', fields=[
    TextDyField.data_source('Subscription ARN', 'subscription_arn'),
    TextDyField.data_source('Endpoint', 'endpoint'),
    EnumDyField.data_source('Protocol', 'protocol', default_outline_badge=['http', 'https', 'email', 'email-json',
                                                                           'sqs', 'lambda']),
])

encryption = ItemDynamicLayout.set_fields('Encryptions', 'data.kms', fields=[
    EnumDyField.data_source('Encryption', 'encryption', default_badge={
        'indigo.500': ['Configured']
    }),
    TextDyField.data_source('Description', 'description'),
    TextDyField.data_source('Custom Master Key (CMK)', 'alias'),
    TextDyField.data_source('CMK ARN', 'arn'),
])

tags = SimpleTableDynamicLayout.set_tags()
metadata = CloudServiceMeta.set_layouts(layouts=[sns, subscription, encryption, tags])


class SNSResource(CloudServiceResource):
    cloud_service_group = StringType(default='SNS')


class TopicResource(SNSResource):
    cloud_service_type = StringType(default='Topic')
    data = ModelType(Topic)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class TopicResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.topic_arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(TopicResource)
