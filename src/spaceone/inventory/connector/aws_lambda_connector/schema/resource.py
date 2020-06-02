import logging

from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_lambda_connector.schema.data import LambdaFunctionData, Layer
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, DateTimeDyField, \
    BadgeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout

function = ItemDynamicLayout.set_fields('Functions', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('ARN', 'data.arn'),
    BadgeDyField.data_source('Runtime', 'data.runtime'),
    EnumDyField.data_source('State', 'data.state.type', default_state={
        'safe': ['Active'],
        'warning': ['Pending'],
        'disable': ['Inactive'],
        'alert': ['Failed']
    }),
    TextDyField.data_source('State Reason', 'data.state.reason'),
    EnumDyField.data_source('State Reason Code', 'data.state.reason_code', default_state={
        'warning': ['Creating', 'Restoring', 'Idle'],
        'alert': ['EniLimitExceeded', 'InsufficientRolePermissions', 'InvalidConfiguration', 'InternalError',
                  'SubnetOutOfIPAddresses', 'InvalidSubnet', 'InvalidSecurityGroup']

    }),
    TextDyField.data_source('Role', 'data.role'),
    TextDyField.data_source('Handler', 'data.handler'),
    TextDyField.data_source('Code Size', 'data.code_size'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Timeout', 'data.timeout'),
    TextDyField.data_source('Memory Size', 'data.memory_size'),
    TextDyField.data_source('Code SHA 256', 'data.code_sha256'),
    TextDyField.data_source('KMS Key ARN', 'data.kms_key_arn'),
    TextDyField.data_source('Master ARN', 'data.master_arn'),
    TextDyField.data_source('Revision ID', 'data.revision_id'),
    EnumDyField.data_source('Last Update Status', 'data.last_update.type', default_state={
        'safe': ['Successful'],
        'alert': ['Failed'],
        'warning': ['InProgress']
    }),
    TextDyField.data_source('Last Update State Reason', 'data.last_update.reason'),
    EnumDyField.data_source('State Reason Code', 'data.last_update.reason_code', default_state={
        'alert': ['EniLimitExceeded', 'InsufficientRolePermissions', 'InvalidConfiguration', 'InternalError',
                  'SubnetOutOfIPAddresses', 'InvalidSubnet', 'InvalidSecurityGroup']

    }),
    DateTimeDyField.data_source('Last Modified', 'data.last_modified'),
])

function_vpc = ItemDynamicLayout.set_fields('VPC', fields=[
    TextDyField.data_source('VPC Id', 'data.vpc_config.vpc.id'),
    TextDyField.data_source('VPC Name', 'data.vpc_config.vpc.name'),
    EnumDyField.data_source('Default VPC', 'data.vpc_config.vpc.is_default', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    ListDyField.data_source('Subnets', 'data.vpc_config.subnets', default_badge={
        'type': 'outline',
        'sub_key': 'id',

    }),
    ListDyField.data_source('Security Groups', 'data.vpc_config.security_groups', default_badge={
        'type': 'outline',
        'sub_key': 'id',
    })
])

function_env = SimpleTableDynamicLayout.set_fields('Environment Variables', 'data.environment.variables', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

function_layers = TableDynamicLayout.set_fields('Layers', 'data.layers', fields=[
    TextDyField.data_source('ARN', 'arn'),
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Code Size', 'code_size'),
])

function_metadata = CloudServiceMeta.set_layouts(layouts=[function, function_vpc, function_env, function_layers])


layer = ItemDynamicLayout.set_fields('Layers', fields=[
    TextDyField.data_source('Name', 'data.layer_name'),
    TextDyField.data_source('ARN', 'data.layer_arn'),
    ListDyField.data_source('Compatible Runtimes', 'data.latest_matching_version.compatible_runtimes', default_badge={
        'type': 'outline',
    }),
    TextDyField.data_source('Version', 'data.latest_matching_version.version'),
    TextDyField.data_source('Description', 'data.latest_matching_version.description'),
    TextDyField.data_source('License Info', 'data.latest_matching_version.license_info'),
    TextDyField.data_source('Layer Version ARN', 'data.latest_matching_version.layer_version_arn'),
    DateTimeDyField.data_source('Created Time', 'data.latest_matching_version.created_date'),
])

layer_metadata = CloudServiceMeta.set_layouts(layouts=[layer])


class LambdaResource(CloudServiceResource):
    cloud_service_group = StringType(default='Lambda')


class LambdaFunctionResource(LambdaResource):
    cloud_service_type = StringType(default='Function')
    data = ModelType(LambdaFunctionData)
    _metadata = ModelType(CloudServiceMeta, default=function_metadata, serialized_name='metadata')


class LambdaLayerResource(LambdaResource):
    cloud_service_type = StringType(default='Layer')
    data = ModelType(Layer)
    _metadata = ModelType(CloudServiceMeta, default=layer_metadata, serialized_name='metadata')


class LambdaFunctionResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(LambdaFunctionResource)


class LambdaLayerResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.layer_arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(LambdaLayerResource)
