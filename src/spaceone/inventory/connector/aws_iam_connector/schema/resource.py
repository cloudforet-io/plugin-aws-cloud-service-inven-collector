from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_iam_connector.schema.data import Group, User, Role, Policy, IdentityProvider
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, ListDyField, \
    BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout, ListDynamicLayout

# GROUP
group_base = ItemDynamicLayout.set_fields('Group', fields=[
    TextDyField.data_source('Group ARN', 'data.arn'),
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
    EnumDyField.data_source('MFA', 'mfa_device', default_badge={
        'indigo.500': ['Virtual'], 'coral.600': ['Not enabled'],
    }),
])

group_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.attached_permission', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy ID', 'policy_id'),
    EnumDyField.data_source('Policy Type', 'policy_type', default_badge={
        'indigo.500': ['AWS Managed'], 'coral.600': ['Local Managed'],
    }),
    TextDyField.data_source('Policy ARN', 'arn'),
    TextDyField.data_source('Permission Usage Count', 'attachment_count'),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Created At', 'create_date'),
    DateTimeDyField.data_source('Updated At', 'update_date'),
])

group_metadata = CloudServiceMeta.set_layouts(layouts=[group_base, group_user_table, group_policy_table])

# USER
user_base = ItemDynamicLayout.set_fields('User', fields=[
    TextDyField.data_source('User Name', 'data.user_name'),
    TextDyField.data_source('User ID', 'data.user_id'),
    TextDyField.data_source('User ARN', 'data.arn'),
    TextDyField.data_source('Path', 'data.path'),
    TextDyField.data_source('groups', 'data.groups_display'),
    TextDyField.data_source('Access Key Age', 'data.access_key_age_display'),
    TextDyField.data_source('Last Activity', 'data.last_activity'),
    EnumDyField.data_source('MFA', 'data.mfa_device', default_badge={
        'indigo.500': ['Virtual'], 'coral.600': ['Not enabled'],
    }),
    DateTimeDyField.data_source('Created At', 'data.create_date'),
    DateTimeDyField.data_source('Last Accessed At', 'data.password_last_used'),
])

user_policy_table = TableDynamicLayout.set_fields('Permission', root_path='data.policies', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    EnumDyField.data_source('Policy Type', 'policy_type', default_badge={
        'indigo.500': ['AWS Managed'], 'coral.600': ['Local Managed'],
    }),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

user_group_table = TableDynamicLayout.set_fields('Groups', root_path='data.groups', fields=[
    TextDyField.data_source('Group Name', 'group_name'),
    ListDyField.data_source('Policy Name', 'attached_policy_name', default_badge={'type': 'outline',
                                                                                  'delimiter': '<br>'}),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

sign_in_credentials = ItemDynamicLayout.set_fields('Sign-in Credentials', root_path='data.sign_in_credential',
                                                   fields=[
                                                       ListDyField.data_source('Summary', 'summary'),
                                                       EnumDyField.data_source('Console Password', 'console_password',
                                                                               default_badge={
                                                                                   'indigo.500': ['Enabled'],
                                                                                   'coral.600': ['Disabled'],
                                                                               }),
                                                       TextDyField.data_source('Assigned MFA device',
                                                                               'assigned_mfa_device'),
                                                   ])


access_key = SimpleTableDynamicLayout.set_fields('Access Keys', root_path='data.access_key', fields=[
    TextDyField.data_source('Access Key ID', 'key_id'),
    DateTimeDyField.data_source('Created At', 'create_date'),
    TextDyField.data_source('Last Used', 'last_update_date_display'),
])

ssh_codecommit = SimpleTableDynamicLayout.set_fields('SSH Keys for AWS CodeCommit', root_path='data.ssh_public_key'
                                                     , fields=[
        TextDyField.data_source('SSH Key ID', 'key_id'),
        DateTimeDyField.data_source('Uploaded At', 'upload_date'),
        EnumDyField.data_source('Status', 'status',
                                default_badge={'indigo.500': ['Active'], 'coral.600': ['Inactive']}),
    ])

https_codecommit = SimpleTableDynamicLayout.set_fields('HTTPS Git Credentials for AWS CodeCommit',
                                                       root_path='data.code_commit_credential',
                                                       fields=[
                                                           TextDyField.data_source('User Name', 'service_user_name'),
                                                           DateTimeDyField.data_source('Created At', 'create_date'),
                                                           EnumDyField.data_source('Status', 'status', default_badge={
                                                               'indigo.500': ['Active'],
                                                               'coral.600': ['Inactive']
                                                           }),
                                                       ])

cred_aws_keyspaces = SimpleTableDynamicLayout.set_fields('Credentials for Amazon Keyspaces (for Apache Cassandra)',
                                                         root_path='data.cassandra_credential',
                                                         fields=[
                                                             TextDyField.data_source('User Name', 'service_user_name'),
                                                             DateTimeDyField.data_source('Created At', 'create_date'),
                                                             EnumDyField.data_source('Status', 'status',
                                                                                     default_badge={
                                                                                         'indigo.500': ['Active'],
                                                                                         'coral.600': ['Inactive']}),
                                                         ])

user_security_credential = ListDynamicLayout.set_layouts('Security Credentials', layouts=[sign_in_credentials,
                                                                                          access_key,
                                                                                          ssh_codecommit,
                                                                                          https_codecommit,
                                                                                          cred_aws_keyspaces])

user_tags = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

user_metadata = CloudServiceMeta.set_layouts(layouts=[user_base, user_policy_table, user_group_table,
                                                      user_security_credential, user_tags])

# ROLE
role_base = ItemDynamicLayout.set_fields('Roles', fields=[
    TextDyField.data_source('Role ARN', 'data.arn'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Role Name', 'data.role_name'),
    TextDyField.data_source('Role ID', 'data.role_id'),
    TextDyField.data_source('Path', 'data.path'),
    ListDyField.data_source('Trusted entities', 'data.trusted_entities', default_badge={'type': 'outline', 'delimiter': '<br>' }),
    TextDyField.data_source('Last Activity', 'data.last_activity'),
    TextDyField.data_source('Maximum session duration', 'data.max_session_duration'),
    DateTimeDyField.data_source('Created At', 'data.create_date'),
])

role_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.policies', fields=[
    TextDyField.data_source('Policy Name', 'policy_name'),
    TextDyField.data_source('Policy ID', 'policy_id'),
    TextDyField.data_source('Used As', 'attachment_count'),
    EnumDyField.data_source('Policy Type', 'policy_type', default_badge={
        'indigo.500': ['AWS Managed'], 'coral.600': ['Local Managed'],
    }),
    TextDyField.data_source('Description', 'description'),
    DateTimeDyField.data_source('Created At', 'create_date'),

])
# data.trust_relationship.trusted_entities
role_trust_relationships = TableDynamicLayout.set_fields('Trust Relationships', root_path='data.trust_relationship',
                                                         fields=[
                                                             ListDyField.data_source('Trusted Entities',
                                                                                     'trusted_entities',
                                                                                     default_badge={'type': 'outline',
                                                                                                    'delimiter': '<br>'}),
                                                             ListDyField.data_source('Condition',
                                                                                     'condition_name',
                                                                                     default_badge={
                                                                                         'type': 'outline',
                                                                                          'delimiter': '<br>'
                                                                                     }),
                                                             ListDyField.data_source('Condition Key',
                                                                                     'condition_key',
                                                                                     default_badge={
                                                                                         'delimiter': '<br>'
                                                                                     }),
                                                             ListDyField.data_source('Condition Value',
                                                                                     'condition_value',
                                                                                     default_badge={
                                                                                         'delimiter': '<br>'
                                                                                     }),
                                                         ])

role_tags = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

role_metadata = CloudServiceMeta.set_layouts(layouts=[role_base, role_policy_table, role_trust_relationships, role_tags])

# POLICY
policy_base = ItemDynamicLayout.set_fields('Policy', fields=[
    TextDyField.data_source('Policy Name', 'data.policy_name'),
    TextDyField.data_source('Policy ARN', 'data.arn'),
    TextDyField.data_source('Policy ID', 'data.policy_id'),
    EnumDyField.data_source('Policy Type', 'data.policy_type', default_badge={
        'indigo.500': ['AWS Managed'], 'coral.600': ['Local Managed'],
    }),
    TextDyField.data_source('Attachment Count', 'data.attachment_count'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Path', 'data.path'),
    DateTimeDyField.data_source('Created At', 'data.create_date'),
])

policy_permission = TableDynamicLayout.set_fields('Permission', root_path='data.permission.statement', fields=[
    ListDyField.data_source('Action', 'action'),
    ListDyField.data_source('Condition', 'condition'),
    ListDyField.data_source('Resource', 'resource'),
    EnumDyField.data_source('Effect', 'effect', default_badge={
        'indigo.500': ['Allow'], 'coral.600': ['Deny']
    }),
    TextDyField.data_source('Sid', 'sid'),
])

policy_usage = TableDynamicLayout.set_fields('Policy Usage', root_path='data.policy_usage', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Type', 'type', default_badge={
        'indigo.500': ['Group'], 'coral.600': ['User'], 'green.500': ['Role'],
    }),
])

policy_version = TableDynamicLayout.set_fields('Policy Versions', root_path='data.permission_versions', fields=[
    TextDyField.data_source('Version ID', 'version_id'),
    EnumDyField.data_source('Is Default version', 'is_default_version', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    DateTimeDyField.data_source('Created At', 'create_date'),
])

policy_metadata = CloudServiceMeta.set_layouts(layouts=[policy_base, policy_permission, policy_usage, policy_version])

# Identity Provider
identity_provider_base = ItemDynamicLayout.set_fields('Identity Provider', fields=[
    TextDyField.data_source('Provider Name', 'data.url'),
    EnumDyField.data_source('Type', 'data.provider_type', default_badge={'indigo.500': ['OIDC']}),
    DateTimeDyField.data_source('Created At', 'data.create_date'),
])

identity_provider_metadata = CloudServiceMeta.set_layouts(layouts=[identity_provider_base])


class IAMResource(CloudServiceResource):
    cloud_service_group = StringType(default='IAM')


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
