import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
GROUP
"""
cst_group = CloudServiceTypeResource()
cst_group.name = 'Group'
cst_group.provider = 'aws'
cst_group.group = 'IAM'
cst_group.labels = ['Security']
cst_group.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Identity-and-Access-Management_IAM.svg',
}

cst_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('User Count', 'data.user_count'),
        DateTimeDyField.data_source('Creation Time', 'data.create_date'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Group ID', 'data.group_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Attached Policies name', 'data.attached_permission', options={
            'sub_key': 'policy_name',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Attached Policies Id', 'data.attached_permission', options={
            'sub_key': 'policy_id',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Attached Policies ARN', 'data.attached_permission', options={
            'sub_key': 'arn',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('User Names', 'data.users', options={
            'sub_key': 'user_name',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Users Last Activity', 'data.users', options={
            'sub_key': 'last_activity',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Users Access Key Age', 'data.users', options={
            'sub_key': 'access_key_age_display',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('Path', 'data.path', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Group ARN', key='data.arn'),
        SearchField.set(name='User Name', key='data.users.user_name'),
        SearchField.set(name='Policy Name', key='data.attached_permission.policy_name'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='account')
    ]
)

"""
USER
"""
total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
access_key_total_count_conf = os.path.join(current_dir, 'widget/access_key_total_count.yaml')
mfa_used_status_conf = os.path.join(current_dir, 'widget/mfa_used_status.yaml')
access_key_age_30_total_count_conf = os.path.join(current_dir, 'widget/access_key_age_30_total_count.yaml')
access_key_age_ratio_conf = os.path.join(current_dir, 'widget/access_key_age_ratio.yaml')

cst_user = CloudServiceTypeResource()
cst_user.name = 'User'
cst_user.provider = 'aws'
cst_user.group = 'IAM'
cst_user.labels = ['Security']
cst_user.is_primary = True
cst_user.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Identity-and-Access-Management_IAM.svg',
}

cst_user._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        ListDyField.data_source('Groups', 'data.groups', options={
            'delimiter': '<br>',
            'sub_key': 'group_name'
        }),
        TextDyField.data_source('Access Key Age', 'data.access_key_age', options={
            'postfix': 'days'
        }),
        TextDyField.data_source('Last Activity', 'data.last_active_age', options={
            'postfix': 'days'
        }),
        TextDyField.data_source('MFA', 'data.mfa_device'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('User ID', 'data.user_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Console Password Enabled', 'data.sign_in_credential.console_password', options={
            'is_optional': True
        }),
        TextDyField.data_source('MFA Device', 'data.mfa_device', options={
            'is_optional': True
        }),
        ListDyField.data_source('Access Key IDs', 'data.access_key', options={
            'sub_key': 'key_id',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Access Key status', 'data.access_key', options={
            'sub_key': 'status',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('SSH Public Key', 'data.ssh_public_key', options={
            'delimiter': '<br>',
            'sub_key': 'key_id',
            'is_optional': True
        }),
        ListDyField.data_source('Cassandra Credential User Name', 'data.cassandra_credential', options={
            'delimiter': '<br>',
            'sub_key': 'service_user_name',
            'is_optional': True
        }),
        ListDyField.data_source('Code Commit Credential User Name', 'data.code_commit_credential', options={
            'delimiter': '<br>',
            'sub_key': 'service_user_name',
            'is_optional': True
        }),
        ListDyField.data_source('Policy Names', 'data.policies', options={
            'sub_key': 'policy_name',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Policy IDs', 'data.policies', options={
            'sub_key': 'policy_id',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Policy ARNs', 'data.policies', options={
            'sub_key': 'arn',
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Policy Types', 'data.policies', options={
            'sub_key': 'policy_type',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
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
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(access_key_total_count_conf)),
        CardWidget.set(**get_data_from_yaml(mfa_used_status_conf)),
        CardWidget.set(**get_data_from_yaml(access_key_age_30_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(access_key_age_ratio_conf))
    ]
)


"""
ROLE
"""

cst_role = CloudServiceTypeResource()
cst_role.name = 'Role'
cst_role.provider = 'aws'
cst_role.group = 'IAM'
cst_role.labels = ['Security']
cst_role.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Identity-and-Access-Management_IAM.svg',
}

cst_role._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Last Activity', 'data.last_activity'),
        ListDyField.data_source('Trusted Entities', 'data.trusted_entities', options={
            'delimiter': '<br>'
        }),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Role ID', 'data.role_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Role Last Used Region', 'data.role_last_used.region', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Role Last Used Date', 'data.role_last_used.last_used_data', options={
            'is_optional': True
        }),
        ListDyField.data_source('Policy Names', 'data.policies', options={
            'delimiter': '<br>',
            'sub_key': 'policy_name',
            'is_optional': True
        }),
        ListDyField.data_source('Policy ARNs', 'data.policies', options={
            'delimiter': '<br>',
            'sub_key': 'arn',
            'is_optional': True
        }),
        ListDyField.data_source('Policy IDs', 'data.policies', options={
            'delimiter': '<br>',
            'sub_key': 'policy_id',
            'is_optional': True
        }),
        ListDyField.data_source('Policy Types', 'data.policies', options={
            'delimiter': '<br>',
            'sub_key': 'policy_type',
            'is_optional': True
        }),
        TextDyField.data_source('Path', 'data.path', options={
            'is_optional': True
        }),
        TextDyField.data_source('Max Session Duration', 'data.max_session_duration', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Role ARN', key='data.arn'),
        SearchField.set(name='Trust Relationships', key='data.trust_relationship.trust_relationship'),
        SearchField.set(name='Policy Name', key='data.policies.policy_name'),
        SearchField.set(name='Last Used Time', key='data.role_last_used.last_used_data', data_type='datetime'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='account')
    ]
)


"""
POLICY
"""

cst_policy = CloudServiceTypeResource()
cst_policy.name = 'Policy'
cst_policy.provider = 'aws'
cst_policy.group = 'IAM'
cst_policy.labels = ['Security']
cst_policy.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Identity-and-Access-Management_IAM.svg',
}

cst_policy._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Policy ID', 'data.policy_id'),
        TextDyField.data_source('Attachment Count', 'data.attachment_count'),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Is Attachable', 'data.is_attachable', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Policy Type', 'data.policy_type', options={
            'is_optional': True
        }),
        TextDyField.data_source('Default Version ID', 'data.default_version_id', options={
            'is_optional': True
        }),
        ListDyField.data_source('Policy Usage Name', 'data.policy_usage', options={
            'delimiter': '<br>',
            'sub_key': 'name',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Policy ARN', key='data.arn'),
        SearchField.set(name='Policy ID', key='data.policy_id'),
        SearchField.set(name='Permission Usage Count', key='data.permissions_boundary_usage_count',
                        data_type='integer'),
        SearchField.set(name='Update Time', key='data.update_date', data_type='datetime'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
        SearchField.set(name='Is Attachable', key='data.is_attachable', enums={
                    'true': {'label': 'true'},
                    'false': {'label': 'false'},
                }),
        SearchField.set(name='AWS Account ID', key='account')
    ]
)

"""
IDENTITY PROVIDER
"""

cst_identity_provider = CloudServiceTypeResource()
cst_identity_provider.name = 'IdentityProvider'
cst_identity_provider.provider = 'aws'
cst_identity_provider.group = 'IAM'
cst_identity_provider.labels = ['Security']
cst_identity_provider.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Identity-and-Access-Management_IAM.svg',
}

cst_identity_provider._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source(name='provider_type', key='data.provider_type', default_badge={'indigo.500': ['OIDC']}),
        TextDyField.data_source('ARN', 'data.arn', options={
            'is_optional': True
        }),
        ListDyField.data_source('Client ID List', 'data.client_id_list', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        ListDyField.data_source('Thumbprint List', 'data.thumbprint_list', options={
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='Identity Provider ARN', key='data.arn'),
        SearchField.set(name='Provider Type', key='data.provider_type'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='account')
    ]
)


"""
ACCESS KEY
"""

cst_access_key = CloudServiceTypeResource()
cst_access_key.name = 'AccessKey'
cst_access_key.provider = 'aws'
cst_access_key.group = 'IAM'
cst_access_key.labels = ['Security']
cst_access_key.tags = {
    'spaceone:icon': f'{ASSET_URL}/AWS-Identity-and-Access-Management_IAM.svg',
}

cst_access_key._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.status',
                                default_badge={'indigo.500': ['Active'], 'coral.600': ['Inactive']}),
        TextDyField.data_source('User name', 'data.user_name'),
        TextDyField.data_source('Last Used', 'data.last_update_date_display'),
        DateTimeDyField.data_source('Created At', 'data.create_date'),
    ],
    search=[
        SearchField.set(name='Access Key ID', key='data.key_id'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='User name', key='data.user_name'),
        SearchField.set(name='User ARN', key='data.user_arn'),
        SearchField.set(name='Creation Time', key='data.create_date', data_type='datetime'),
        SearchField.set(name='Last Used Time', key='data.access_key_last_used.last_update_date', data_type='datetime'),
        SearchField.set(name='AWS Account ID', key='account')
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_group}),
    CloudServiceTypeResponse({'resource': cst_user}),
    CloudServiceTypeResponse({'resource': cst_role}),
    CloudServiceTypeResponse({'resource': cst_policy}),
    CloudServiceTypeResponse({'resource': cst_identity_provider}),
    CloudServiceTypeResponse({'resource': cst_access_key}),
]
