from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_iam_connector.schema.data import Group, User, Role, Policy, IdentityProvider
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, ListDyField, \
    BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout, ListDynamicLayout


group_base = ItemDynamicLayout.set_fields('Group', fields=[
    TextDyField.data_source('Group ARN', 'data.path'),
    TextDyField.data_source('Group Name', 'data.group_name'),
    TextDyField.data_source('Group ID', 'data.group_id'),
    TextDyField.data_source('Path', 'data.path'),
    TextDyField.data_source('User Count', 'data.user_count'),
    DateTimeDyField.data_source('Created At', 'data.create_date'),
])

group_user_table = TableDynamicLayout.set_fields('Users', root_path='data.users', fields=[
    TextDyField.data_source('User Name', 'user_name'),
    TextDyField.data_source('Access Key Age', 'access_key_age_display'),
    TextDyField.data_source('Last Activity', 'last_activity'),
    TextDyField.data_source('MFA', 'mfa_device'),
])

group_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.attached_permission', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy ID', 'policy_id'),
    TextDyField.data_source('Policy Type', 'policy_type'),
    TextDyField.data_source('Policy ARN', 'arn'),
    TextDyField.data_source('Permission Usage Count', 'attachment_count'),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Created At', 'create_date'),
    DateTimeDyField.data_source('Updated At', 'update_date'),
])

group_metadata = CloudServiceMeta.set_layouts(layouts=[group_base, group_user_table, group_policy_table])

user_base = ItemDynamicLayout.set_fields('User', fields=[
    TextDyField.data_source('User Name', 'user_name'),
    TextDyField.data_source('User ID', 'user_id'),
    TextDyField.data_source('User ARN', 'arn'),
    TextDyField.data_source('Path', 'path'),
    TextDyField.data_source('groups', 'groups_display'),
    TextDyField.data_source('Access Key Age', 'access_key_age_display'),
    TextDyField.data_source('Last Activity', 'last_activity'),
    TextDyField.data_source('MFA', 'mfa_device'),
    DateTimeDyField.data_source('Created At', 'create_date'),
    DateTimeDyField.data_source('Last Accessed At', 'password_last_used'),
])

user_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.user.policies', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy Type', 'policy_type'),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

user_group_table = TableDynamicLayout.set_fields('Groups', root_path='data.user.groups', fields=[
    TextDyField.data_source('Group Name', 'group_name'),
    TextDyField.data_source('Policy Name', 'attached_policy_name'),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

sign_in_credentials = ItemDynamicLayout.set_fields('Sign-in Credentials', root_path='data.user.sign_in_credential',
                                                   fields=[
                                                       ListDyField.data_source('Summary', 'summary'),
                                                       TextDyField.data_source('Console Password', 'console_password'),
                                                       TextDyField.data_source('Assigned MFA device',
                                                                               'assigned_mfa_device'),
                                                   ])


access_key = SimpleTableDynamicLayout.set_fields('Access Keys', root_path='data.user.access_key', fields=[
    TextDyField.data_source('Access Key ID', 'key_id'),
    DateTimeDyField.data_source('Created At', 'create_date'),
    TextDyField.data_source('Last Used', 'last_update_date_display'),
    EnumDyField.data_source('Status', 'data.status', default_outline_badge=['Active', 'Inactive']),
])

ssh_codecommit = SimpleTableDynamicLayout.set_fields('SSH Keys for AWS CodeCommit', root_path='data.user.ssh_public_key'
                                                     , fields=[
        TextDyField.data_source('SSH Key ID', 'key_id'),
        DateTimeDyField.data_source('Uploaded At', 'upload_date'),
        EnumDyField.data_source('Status', 'status', default_outline_badge=['Active', 'Inactive']),
    ])

https_codecommit = SimpleTableDynamicLayout.set_fields('HTTPS Git Credentials for AWS CodeCommit',
                                                       root_path='data.user.code_commit_credential',
                                                       fields=[
                                                           TextDyField.data_source('User Name', 'service_user_name'),
                                                           EnumDyField.data_source('Status', 'status',
                                                                                   default_outline_badge=['Active',
                                                                                                          'Inactive']),
                                                           DateTimeDyField.data_source('Created At', 'create_date'),
                                                       ])

cred_aws_keyspaces = SimpleTableDynamicLayout.set_fields('Credentials for Amazon Keyspaces (for Apache Cassandra)',
                                                         root_path='data.user.cassandra_credential', fields=[
        TextDyField.data_source('User Name', 'service_user_name'),
        EnumDyField.data_source('Status', 'status', default_outline_badge=['Active', 'Inactive']),
        DateTimeDyField.data_source('Created At', 'create_date'),
    ])

user_security_credential = ListDynamicLayout.set_layouts('Security Credentials', layouts=[sign_in_credentials,
                                                                                          access_key,
                                                                                          ssh_codecommit,
                                                                                          https_codecommit,
                                                                                          cred_aws_keyspaces])

user_tags = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.user.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

user_metadata = CloudServiceMeta.set_layouts(layouts=[user_base, user_policy_table, user_group_table,
                                                      user_security_credential, user_tags])

role_base = ItemDynamicLayout.set_fields('Roles', fields=[
    TextDyField.data_source('Role ARN', 'arn'),
    TextDyField.data_source('Description', 'description'),
    TextDyField.data_source('Role Name', 'role_name'),
    TextDyField.data_source('Role ID', 'role_id'),
    TextDyField.data_source('Path', 'path'),
    DateTimeDyField.data_source('Created At', 'create_date'),
    ListDyField.data_source('Trusted entities', 'trusted_entities'),
    TextDyField.data_source('Last Activity', 'last_activity'),
    TextDyField.data_source('Maximum session duration', 'max_session_duration'),
])

role_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.role.policies', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy ID', 'policy_id'),
    TextDyField.data_source('Used As', 'attachment_count'),
    TextDyField.data_source('Policy Type', 'policy_type'),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Created At', 'create_date'),

])

role_trust_relationship_entities = ItemDynamicLayout.set_fields('Trusted Entities', root_path='data.role.trust_relationship', fields=[
    ListDyField.data_source('Trusted entities', 'trust_relationship'),
])

role_trust_relationship_condition = SimpleTableDynamicLayout.set_fields('Conditions', root_path='data.role.trust_relationship', fields=[
    TextDyField.data_source('Condition', 'condition'),
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

role_trust_relationship = ListDynamicLayout.set_layouts(name='Trust relationships',
                                                        layouts=[role_trust_relationship_entities,
                                                                 role_trust_relationship_condition])

role_tags = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.role.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

role_metadata = CloudServiceMeta.set_layouts(layouts=[role_base, role_policy_table, role_trust_relationship, role_tags])


#
# class Policy(Model):
#     arn = StringType(deserialize_from="Arn")
#     attachment_count = IntType(deserialize_from="AttachmentCount")
#     is_attachable = BooleanType(deserialize_from="IsAttachable")
#     default_version_id = StringType(deserialize_from="DefaultVersionId")
#     path = StringType(deserialize_from="Path")
#     permissions_boundary_usage_count = IntType(deserialize_from="PermissionsBoundaryUsageCount")
#     policy_id = StringType(deserialize_from="PolicyId")
#     policy_name = StringType(deserialize_from="PolicyName")
#     policy_type = StringType()
#     description = StringType(deserialize_from="Description", default='')
#     create_date = DateTimeType(deserialize_from="CreateDate")
#     update_date = DateTimeType(deserialize_from="UpdateDate")
#     permission = ListType(ModelType(PermissionSummary))
#     permission_versions = ListType(ModelType(PermissionVersions))

# POLICY
policy_base = ItemDynamicLayout.set_fields('Policy', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy ARN', 'policy_arn'),
    TextDyField.data_source('Policy ID', 'policy_id'),
    TextDyField.data_source('Policy Type', 'policy_type'),
    TextDyField.data_source('Used As', 'attachment_count'),
    TextDyField.data_source('Description', 'description'),
    TextDyField.data_source('Path', 'path'),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

policy_permission = TableDynamicLayout.set_fields('Permissions', root_path='data.', fields=[
    # TODO: PERMISSION TABLE FIELDS for POLICY
])

policy_usage = TableDynamicLayout.set_fields('Policy Usage', root_path='data.', fields=[
    # TODO: USAGE TABLE FIELDS for POLICY
])

policy_version = TableDynamicLayout.set_fields('Policy Versions', root_path='data.policy.permission_versions', fields=[
    TextDyField.data_source('Version ID', 'version_id'),
    EnumDyField.data_source('Is Default version', 'is_default_version', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

policy_metadata = CloudServiceMeta.set_layouts(layouts=[policy_base, policy_permission, policy_usage, policy_version])

# IDENTITY PROVIDER
identity_provider_base = ItemDynamicLayout.set_fields('Identity Provider', fields=[
    # TODO: IDENTITY ITEM FIELDS
])

identity_provider_metadata = CloudServiceMeta.set_layouts(layouts=[identity_provider_base])


class IAMResource(CloudServiceResource):
    cloud_service_group = StringType(default='IAM')


# GROUP
class GroupResource(IAMResource):
    cloud_service_type = StringType(default='Group')
    data = ModelType(Group)
    _metadata = ModelType(CloudServiceMeta, default=group_metadata, serialized_name='metadata')


class GroupResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(GroupResource)


# USER
class UserResource(IAMResource):
    cloud_service_type = StringType(default='User')
    data = ModelType(User)
    _metadata = ModelType(CloudServiceMeta, default=user_metadata, serialized_name='metadata')


class UserResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(UserResource)


# ROLE
class RoleResource(IAMResource):
    cloud_service_type = StringType(default='Role')
    data = ModelType(Role)
    _metadata = ModelType(CloudServiceMeta, default=role_metadata, serialized_name='metadata')


class RoleResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(RoleResource)


# POLICY
class PolicyResource(IAMResource):
    cloud_service_type = StringType(default='Policy')
    data = ModelType(Policy)
    _metadata = ModelType(CloudServiceMeta, default=policy_metadata, serialized_name='metadata')


class PolicyResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(PolicyResource)


# IDENTITY PROVIDER
class IdentityProviderResource(IAMResource):
    cloud_service_type = StringType(default='IdentityProvider')
    data = ModelType(IdentityProvider)
    _metadata = ModelType(CloudServiceMeta, default=identity_provider_metadata, serialized_name='metadata')


class IdentityProviderResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['data.arn', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource = PolyModelType(IdentityProviderResource)
