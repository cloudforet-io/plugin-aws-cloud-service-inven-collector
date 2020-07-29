from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

# GROUP
cst_group = CloudServiceTypeResource()
cst_group.name = 'Group'
cst_group.provider = 'aws'
cst_group.group = 'IAM'
cst_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/',
    'spaceone:is_major': 'true',
}

cst_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Group Name', 'data.group_name'),
        TextDyField.data_source('Users', 'data.user_count'),
        DateTimeDyField.data_source('Creation Time', 'data.create_date'),
    ],
    search=[
        SearchField.set(name='Group Name', key='data.group_name'),
        SearchField.set(name='Group ARN', key='data.arn'),
        SearchField.set(name='User Name', key='data.users.user_name'),
        SearchField.set(name='Policy Name', key='data.attached_permission.policy_name'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
    ]
)

# USER
cst_user = CloudServiceTypeResource()
cst_user.name = 'User'
cst_user.provider = 'aws'
cst_user.group = 'IAM'
cst_user.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/',
    'spaceone:is_major': 'true',
}

cst_user._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('User Name', 'data.user_name'),
        TextDyField.data_source('Groups', 'data.groups.group_name'),
        TextDyField.data_source('Access Key Age', 'data.access_key_age_display'),
        TextDyField.data_source('Last Activity', 'data.last_activity'),
        TextDyField.data_source('MFA', 'data.mfa_device'),
    ],
    search=[
        SearchField.set(name='User Name', key='data.user_name'),
        SearchField.set(name='User ARN', key='data.arn'),
        SearchField.set(name='Group Name', key='data.user_name'),
        SearchField.set(name='Access Key Age', key='data.access_key_age', data_type='integer'),
        SearchField.set(name='Last Activity', key='data.last_active_age', data_type='integer'),
        SearchField.set(name='MFA', key='data.mfa_device'),
        SearchField.set(name='Policy Name', key='data.policies.policy_name'),
        SearchField.set(name='Access Key ID', key='data.access_key.key_id'),
        SearchField.set(name='Access Key Status', key='data.access_key.status', enums={
            'Active': {'label': 'Active'},
            'Inactive': {'label': 'Inactive'},
        }),
        SearchField.set(name='Access Key Created Time', key='data.access_key.create_date', data_type='datetime'),
        SearchField.set(name='Access Key Last Used', key='data.access_key.access_key_last_used.last_update_date',
                        data_type='datetime'),
        SearchField.set(name='SSH Key ID', key='data.ssh_public_key.key_id'),
        SearchField.set(name='SSH Key Status', key='data.ssh_public_key.status', enums={
            'Active': {'label': 'Active'},
            'Inactive': {'label': 'Inactive'},
        }),
        SearchField.set(name='SSH Key Upload Time', key='data.ssh_public_key.upload_date', data_type='datetime'),
        SearchField.set(name='SSH Key Upload Time', key='data.ssh_public_key.upload_date', data_type='datetime'),
        SearchField.set(name='CodeCommit User Name', key='data.code_commit_credential.service_user_name'),
        SearchField.set(name='CodeCommit Status', key='data.code_commit_credential.status', enums={
            'Active': {'label': 'Active'},
            'Inactive': {'label': 'Inactive'},
        }),
        SearchField.set(name='CodeCommit Created Time ', key='data.code_commit_credential.create_date',
                        data_type='datetime'),
        SearchField.set(name='Keyspaces User Name', key='data.cassandra_credential.service_user_name'),
        SearchField.set(name='Keyspaces Status', key='data.cassandra_credential.status', enums={
            'Active': {'label': 'Active'},
            'Inactive': {'label': 'Inactive'},
        }),
        SearchField.set(name='Keyspaces Created Time ', key='data.cassandra_credential.create_date',
                        data_type='datetime'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
    ]
)

# ROLE
cst_role = CloudServiceTypeResource()
cst_role.name = 'Role'
cst_role.provider = 'aws'
cst_role.group = 'IAM'
cst_role.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/',
    'spaceone:is_major': 'false',
}

cst_role._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Role Name', 'data.role_name'),
        TextDyField.data_source('Trusted Entities', 'data.trusted_entities'),
        TextDyField.data_source('Last Activity', 'data.last_activity'),
    ],
    search=[
        SearchField.set(name='Role Name', key='data.role_name'),
        SearchField.set(name='Role ARN', key='data.arn'),
        SearchField.set(name='Trust Relationships', key='data.trust_relationship.trust_relationship'),
        SearchField.set(name='Policy Name', key='data.policies.policy_name'),
        SearchField.set(name='Last Used Time', key='data.role_last_used.last_used_data', data_type='datetime'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
    ]
)

# POLICY
cst_policy = CloudServiceTypeResource()
cst_policy.name = 'Policy'
cst_policy.provider = 'aws'
cst_policy.group = 'IAM'
cst_policy.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/',
    'spaceone:is_major': 'false',
}

cst_policy._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Role Name', 'data.role_name'),
        TextDyField.data_source('Trusted Entities', 'data.trusted_entities'),
        TextDyField.data_source('Last Activity', 'data.last_activity'),
    ],
    search=[
        # TODO: POLICY SEARCH META
    ]
)

# IDENTITY PROVIDER
cst_identity_provider = CloudServiceTypeResource()
cst_identity_provider.name = 'IdentityProvider'
cst_identity_provider.provider = 'aws'
cst_identity_provider.group = 'IAM'
cst_identity_provider.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/',
    'spaceone:is_major': 'false',
}

cst_identity_provider._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        # TODO: IDENTITY PROVIDER MAIN TABLE FIELDS
    ],
    search=[
        # TODO: IDENTITY PROVIDER SEARCH META
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_group}),
    CloudServiceTypeResponse({'resource': cst_user}),
    CloudServiceTypeResponse({'resource': cst_role}),
    CloudServiceTypeResponse({'resource': cst_policy}),
    CloudServiceTypeResponse({'resource': cst_identity_provider}),
]
