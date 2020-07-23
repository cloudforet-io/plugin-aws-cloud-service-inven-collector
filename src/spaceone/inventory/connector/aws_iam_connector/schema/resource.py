from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_iam_connector.schema.data import Group, User, Role, Policy, IdentityProvider
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    SimpleTableDynamicLayout, ListDynamicLayout

# GROUP
group_base = ItemDynamicLayout.set_fields('Group', fields=[
    # TODO: GROUP ITEM FIELDS
])

group_user_table = TableDynamicLayout.set_fields('Users', root_path='data.users', fields=[
    # TODO: USER TABLE FIELDS each GROUPS
])

group_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.attached_permission', fields=[
    # TODO: PERMISSION TABLE FIELDS each GROUPS
])

group_metadata = CloudServiceMeta.set_layouts(layouts=[group_base, group_user_table, group_policy_table])


# USER
user_base = ItemDynamicLayout.set_fields('User', fields=[
    # TODO: USER ITEM FIELDS
])

user_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.policies', fields=[
    # TODO: PERMISSION TABLE FIELDS each USERS
])

user_group_table = TableDynamicLayout.set_fields('Groups', root_path='data.groups', fields=[
    # TODO: GROUP TABLE FIELDS each USERS
])

signin_cred = ItemDynamicLayout.set_fields('Sign-in Credentials', fields=[
    # TODO: SIGN-IN CREDENTIAL ITEM FIELDS each USERS
])

access_key = SimpleTableDynamicLayout.set_fields('Access Keys', root_path='data.', fields=[
    # TODO: ACCESS KEY TABLE FIELDS each USERS
])

ssh_codecommit = SimpleTableDynamicLayout.set_fields('SSH Keys for AWS CodeCommit', root_path='data.', fields=[
    # TODO: SSH KEYS for CodeCommit each USERS
])

https_codecommit = SimpleTableDynamicLayout.set_fields('HTTPS Git Credentials for AWS CodeCommit', root_path='data.', fields=[
    # TODO: HTTPS GIT CREDENTIALS for CodeCommit each USERS
])

cred_aws_keyspaces = SimpleTableDynamicLayout.set_fields('Credentials for Amazon Keyspaces (for Apache Cassandra)', root_path='data.', fields=[
    # TODO: CREDENTIALS for Amazon Keyspaces each USERS
])

user_security_cred = ListDynamicLayout.set_layouts('Security Credentials',
                                                   layouts=[signin_cred, access_key, ssh_codecommit,
                                                            https_codecommit, cred_aws_keyspaces])

user_tags = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.tags', fields=[
    # TODO: USER TAGS FIELDS
])

user_metadata = CloudServiceMeta.set_layouts(layouts=[user_base, user_policy_table, user_group_table,
                                                       user_security_cred, user_tags])

# ROLE
role_base = ItemDynamicLayout.set_fields('Roles', fields=[
    # TODO: ROLE ITEM FIELDS
])

role_policy_table = TableDynamicLayout.set_fields('Permissions', root_path='data.policies', fields=[
    # TODO: PERMISSION TABLE FIELDS each ROLES
])

role_trust_relationship_entities = ItemDynamicLayout.set_fields('Trusted Entities', fields=[
    # TODO: TRUSTED ENTITIES ITEM FIELDS each Roles
])

role_trust_relationship_condition = SimpleTableDynamicLayout.set_fields('Conditions', fields=[
    # TODO: TRUSTED ENTITIES CONDITIONS ITEM FIELDS each Roles
])

role_trust_relationship = ListDynamicLayout.set_layouts(name='Trust relationships',
                                                        layouts=[role_trust_relationship_entities,
                                                                 role_trust_relationship_condition])

role_tags = SimpleTableDynamicLayout.set_fields('Tags', root_path='data.tags', fields=[
    # TODO: ROLE TAGS
])

role_metadata = CloudServiceMeta.set_layouts(layouts=[role_base, role_policy_table, role_trust_relationship, role_tags])


# POLICY
policy_base = ItemDynamicLayout.set_fields('Policy', fields=[
    # TODO: POLICY ITEM FIELDS
])

policy_permission = TableDynamicLayout.set_fields('Permissions', root_path='data.', fields=[
    # TODO: PERMISSION TABLE FIELDS for POLICY
])

policy_usage = TableDynamicLayout.set_fields('Policy Usage', root_path='data.', fields=[
    # TODO: USAGE TABLE FIELDS for POLICY
])

policy_version = TableDynamicLayout.set_fields('Policy Versions', root_path='data.', fields=[
    # TODO: VERSION TABLE FIELDS for POLICY
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
