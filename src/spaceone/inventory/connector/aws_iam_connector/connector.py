import time
import logging
from typing import List
from datetime import date, datetime, timezone
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_iam_connector.schema.data import Policy, AccessKeyLastUsed, User, Group, Role, \
    IdentityProvider
from spaceone.inventory.connector.aws_iam_connector.schema.resource import IAMResource, GroupResource, GroupResponse, \
    UserResource, UserResponse, RoleResource, RoleResponse, PolicyResource, PolicyResponse, IdentityProviderResource, \
    IdentityProviderResponse

from spaceone.inventory.connector.aws_iam_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)

PAGINATOR_MAX_ITEMS = 10000
PAGINATOR_PAGE_SIZE = 50


class IAMConnector(SchematicAWSConnector):
    group_response_schema = GroupResponse
    user_response_schema = UserResponse
    role_response_schema = RoleResponse
    policy_response_schema = PolicyResponse
    identity_provider_response_schema = IdentityProviderResponse

    service_name = 'iam'

    def get_resources(self):
        print("** IAM START **")
        resources = []
        start_time = time.time()
        policies = self.request_policy_data()
        users = self.request_user_data(policies)
        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        try:
            for data in policies:
                resources.append(self.policy_response_schema(
                    {'resource': PolicyResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            for data in self.request_role_dataata(policies):
                resources.append(self.role_response_schema(
                    {'resource': RoleResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            for data in users:
                resources.append(self.user_response_schema(
                    {'resource': UserResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            for data in self.request_group_data(users, policies):
                resources.append(self.group_response_schema(
                    {'resource': GroupResource({'data': data, 'reference': ReferenceModel(data.reference)})}))

            for data in self.request_identity_provider_data():
                resources.append(self.identity_provider_response_schema(
                    {'resource': IdentityProvider({'data': data, 'reference': ReferenceModel(data.reference)})}))

        except Exception as e:
            print(f'[ERROR {self.service_name}] {e}')

        print(f' EBS Finished {time.time() - start_time} Seconds')
        return resources

    def request_group_data(self, users, policies) -> List[Group]:
        paginator = self.client.get_paginator('list_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for group in data.get('Groups', []):
                group_name = group.get('GroupName')
                user_infos = self.list_user_with_group_name(group_name)
                user_names = [d['UserName'] for d in user_infos if 'UserName' in d]
                matched_users = [p for p in users if p.get('user_name', '') in user_names]

                policy_infos = self.list_policy_with_group_name(group_name)
                policy_name = [d['PolicyName'] for d in policy_infos if 'PolicyName' in d]
                matched_policies = [p for p in policies if p.get('policy_name', '') in policy_name]

                group.update({
                    'users': matched_users,
                    'user_count': len(users),
                    'attached_permission': matched_policies
                })

                yield Group(group, strict=False)

    def request_user_data(self, policies) -> List[User]:
        paginator = self.client.get_paginator('list_users')
        query = self._generate_default_query()
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            for user in data.get('Users', []):

                user_name = user.get('UserName')
                user_info = self.get_user_info(user_name)
                mfa_devices = self.list_mfa_devices(user_name)
                access_keys = self.list_access_keys(user_name)
                login_profile = self.get_login_profile(user_name)
                groups = self.list_groups_with_user_name(user_name)

                self._conditional_update_for_password_last_used(user, user_info)
                self.conditional_update_for_access_key_age_and_access_key_age_display(user, access_keys)
                code_commit_credential, cassandra_credential = self.list_service_specific_credentials(self, user_name)
                last_active_age, last_activity = self._get_age_and_age_display(user_info.get('PasswordLastUsed', None))
                sign_in_link = self._get_sign_in_link(user_info.get('Arn'))

                attached_policies = self.self.list_attached_policy_to_user(user_name)
                matching_policies = self._get_matched_policies_with_attached_policy_info(policies, attached_policies)

                user.update({
                    'access_key': self.list_access_keys(user_name),
                    'ssh_public_key': self.list_ssh_keys(user_name),
                    'code_commit_credential': code_commit_credential,
                    'cassandra_credential': cassandra_credential,
                    'mfa_device': 'Virtual' if len(mfa_devices) > 0 else 'Not enabled',
                    'last_active_age': last_active_age,
                    'last_activity': last_activity,
                    'policies': matching_policies,
                    'groups_display': groups[0].get('GroupName', '') if len(groups) > 0 else '',
                    'groups': self.get_groups_for_user(groups),
                    'sign_in_credential': {
                        'summary': self._get_summary_with_login_profile(login_profile, sign_in_link, mfa_devices),
                        'console_password': 'Enabled' if login_profile is not None else 'Disabled',
                        'assigned_mfa_device': user_info.get('Arn') if len(mfa_devices) > 0 else 'Not assigned'
                    }
                })

                yield User(user, strict=False)


    def request_role_data(self, policies) -> List[Role]:
        paginator = self.client.get_paginator('list_roles')
        query = self._generate_default_query()
        response_iterator = paginator.paginate(**query)

        for response in response_iterator:
            for role in response.get('Roles', []):
                role_name = role.get('RoleName')
                role_info = self.list_role_info_with_role_name(role_name)
                role_last_used, last_activity = self._get_role_last_used_and_activity(role_info)

                attached_policies = self.list_attached_policy_to_role(role_name)
                matching_policies = self._get_matched_policies_with_attached_policy_info(policies, attached_policies)
                trusted_relationship, conditions, trust_entities = self._get_trusted_relationship(role)

                role.update({
                    'trusted_relationship': {
                        'trusted_relationship': trusted_relationship,
                        'condition': conditions
                    },
                    'condition': trusted_relationship,
                    'trust_entities': trust_entities,
                    'policies': matching_policies,
                    'role_last_used': role_last_used,
                    'last_activity': last_activity,
                    'tags': role_info.get('Tags', [])
                })

                yield Role(role, strict=False)

    def request_policy_data(self, **query) -> List[Policy]:
        policies = []
        policy_paginator = self.client.get_paginator('list_policies')
        permission_paginator = self.client.get_paginator('list_policy_versions')
        query = self._generate_key_query('Scope', 'AWS', '', is_paginate=True, **query)
        response_iterator_aws = policy_paginator.paginate(**query)
        query = self._generate_key_query('Scope', 'Local', '', is_paginate=True, **query)
        response_iterator_local = policy_paginator.paginate(**query)

        for data in response_iterator_local:
            for policy in data.get('Policies', []):
                policy_arn = policy.get('Arn')

                query = self._generate_key_query('PolicyArn', policy_arn, 'Scope', is_paginate=True, **query)
                permission_versions = permission_paginator.paginate(**query)
                description = self.list_policy_description(policy_arn)
                permission = self.list_policy_summary(policy_arn, policy.get('DefaultVersionId'))

                for permission_version in permission_versions:
                    policy.update({'description': description,
                                   'permission': permission,
                                   'permission_versions': permission_version.get('Versions', []),
                                   'policy_type': 'Custom Managed'})

                policies.append(Policy(policy, strict=False))

        for data in response_iterator_aws:
            for policy in data.get('Policies', []):
                policy_arn = policy.get('Arn')
                query = self._generate_key_query('PolicyArn', policy_arn, 'Scope', is_paginate=True, **query)
                permission_versions = permission_paginator.paginate(**query)
                description = self.list_policy_description(policy_arn)
                permission = self.list_policy_summary(policy_arn, policy.get('DefaultVersionId'))

                for permission_version in permission_versions:
                    policy.update({'description': description,
                                   'permission': permission,
                                   'permission_versions': permission_version.get('Versions', []),
                                   'policy_type': 'AWS Managed'})

                policies.append(Policy(policy, strict=False))

        return policies

    def request_identity_provider_data(self) -> List[IdentityProvider]:
        response = self.client.list_open_id_connect_providers()

        for arn_dict in response.get('OpenIDConnectProviderList', []):
            arn = arn_dict.get('Arn')
            identity_provider = self.list_open_id_connect_provider_info_with_arn(arn)
            identity_provider.update({
                'arn': arn,
                'provider_type': self._get_provider_type(identity_provider.get('Url', ''))
            })

            yield IdentityProvider(identity_provider, strict=False)

    # For Users list_service_specific_credentials
    def conditional_update_for_access_key_age_and_access_key_age_display(self, user, access_keys):
        if len(access_keys) > 0:
            access_key_date = access_keys[0].get('create_date')
            age, display = self._get_age_and_age_display(access_key_date)
            user.update({'access_key_age': age,
                         'access_key_age_display': display})
        else:
            user.update({'access_key_age': 0, 'access_key_age_display': 'None'})

    def get_user_info(self, user_name):
        response = self.client.get_user(UserName=user_name)
        return response.get('User', {})

    def get_login_profile(self, user_name):
        login_profile = None
        try:
            response = self.client.get_login_profile(UserName=user_name)
            login_profile = response.get('LoginProfile', {})
        except Exception as e:
            print(f'[ERROR: No login_profile with {user_name}] : {e}')

        return login_profile

    def list_access_keys(self, user_name, **query):
        access_keys = []
        query = self._generate_key_query('UserName', user_name, '', is_paginate=True, **query)
        paginator = self.client.get_paginator('list_access_keys')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            for access_key_meta in data.get('AccessKeyMetadata', []):
                key_id = access_key_meta.get('AccessKeyId')
                access_key_last_used_vo = AccessKeyLastUsed(self.get_access_key_last_used(key_id), strict=False)

                access_keys.append({
                    'key_id': key_id,
                    'status': access_key_meta.get('Status', ''),
                    'create_date': access_key_meta.get('CreateDate'),
                    'access_key_last_used': access_key_last_used_vo,
                    'last_update_date_display': self.get_last_update_date_display(access_key_last_used_vo)
                })

        return access_keys

    def list_ssh_keys(self, user_name, **query):
        ssh_keys = []
        query = self._generate_key_query('UserName', user_name, '', is_paginate=True, **query)
        paginator = self.client.get_paginator('list_access_keys')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            for ssh_key in data.get('AccessKeyMetadata', []):
                ssh_keys.append({
                    'key_id': ssh_key.get('SSHPublicKeyId', ''),
                    'status': ssh_key.get('Status', ''),
                    'upload_date': ssh_key.get('UploadDate')
                })

        return ssh_keys

    def list_mfa_devices(self, user_name):
        response = self.client.list_mfa_devices(UserName=user_name)
        return response.get('MFADevices', [])

    def list_service_specific_credentials(self, user_name):
        code_commit_credential = []
        cassandra_credential = []
        response = self.client.get_role(UserName=user_name)
        service_specific_credentials = response.get('ServiceSpecificCredentials', [])
        for ssc in service_specific_credentials:
            if 'UserName' in ssc:
                ssc.pop('UserName', None)

            if ssc.get('ServiceName', '') == 'codecommit.amazonaws.com':
                code_commit_credential.append(ssc)
            elif ssc.get('ServiceName', '') == 'cassandra.amazonaws.com':
                cassandra_credential.append(ssc)

        return code_commit_credential, cassandra_credential

    def list_groups_with_user_name(self, user_name, **query):
        groups = []
        query = self._generate_key_query('UserName', user_name, '', is_paginate=True, **query)
        paginator = self.client.get_paginator('list_groups_for_user')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            groups.extend(data.get('Groups', []))

        return groups

    def list_user_with_group_name(self, group_name, **query):
        users = []
        query = self._generate_key_query('GroupName', group_name, '', is_paginate=True, **query)
        paginator = self.client.get_paginator('get_group')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            users.extend(data.get('Users', []))

        return users

    def get_groups_for_user(self, groups):
        groups_for_user = []
        for group in groups:
            group_name = group.get('GroupName')
            policy_vos = self.list_policy_with_group_name(group_name)
            groups_for_user.append({
                'group_name': group_name,
                'attached_policy_name': [d['PolicyName'] for d in policy_vos if 'PolicyName' in d],
                'create_date': group.get('CreateDate')
            })

        return groups_for_user

    def list_policy_with_group_name(self, group_name, **query):
        policies = []
        query = self._generate_key_query('GroupName', group_name, '', is_paginate=True, **query)
        paginator = self.client.get_paginator('list_attached_group_policies')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            policies.extend(data.get('AttachedPolicies', []))

        return policies

    def list_role_info_with_role_name(self, role_name):
        response = self.client.get_role(RoleName=role_name)
        return response.get('Role', {})

    def list_attached_policy_to_user(self, user_name):
        response = self.client.list_attached_user_policies(UserName=user_name)
        return response.get('AttachedPolicies', [])

    def list_attached_policy_to_role(self, role_name):
        response = self.client.list_attached_role_policies(RoleName=role_name)
        return response.get('AttachedPolicies', [])

    def list_open_id_connect_provider_info_with_arn(self, oidcp_arn):
        response = self.client.get_open_id_connect_provider(OpenIDConnectProviderArn=oidcp_arn)
        return response

    def get_access_key_last_used(self, access_key_id):
        response = self.client.get_access_key_last_used(AccessKeyId=access_key_id)
        return response.get('AccessKeyLastUsed',{})

    def list_policy_description(self, policy_arn):
        policy_info = self.client.get_policy(PolicyArn=policy_arn).get('Policy', {})
        return policy_info.get('Description', '')

    def list_policy_summary(self, policy_arn, version_id):
        policy_info = self.client.get_policy_version(PolicyArn=policy_arn,
                                                     VersionId=version_id).get('PolicyVersion', {})
        empty_permission_summary = {'Statement': [], 'Version': 'N/A'}
        return policy_info.get('Document', empty_permission_summary)

    def list_versions_from_policy(self, policy_arn, **query):
        policy_versions = []
        paginator = self.client.get_paginator('list_policy_versions')
        query = self._generate_default_query(is_paginate=True, **query)
        query.update({'PolicyArn': policy_arn})
        iterator_response = paginator.paginate(**query)

        for data in iterator_response:
            policy_versions.extend(data.get('Versions', []))

        return policy_versions

    @staticmethod
    def _conditional_update_for_password_last_used(user, user_info):
        password_last_used = user_info.get('PasswordLastUsed', None)
        if password_last_used is not None:
            user.update({'password_last_used': password_last_used})



    @staticmethod
    def _conditional_update_for_password_last_used(user, user_info):
        password_last_used = user_info.get('PasswordLastUsed', None)
        if password_last_used is not None:
            user.update({'password_last_used': password_last_used})

    @staticmethod
    def _get_console_password_with_login_profile(login_profile):
        return 'Enable' if login_profile is not None else 'Disable'

    @staticmethod
    def _get_summary_with_login_profile(login_profile, sign_in_link, mfa_devices):
        summary = []
        if login_profile is not None:
            if sign_in_link != '':
                summary.append(f'Console sign-in link: {sign_in_link}')
            if len(mfa_devices) > 0:
                summary.append('MFA is required when signing in.')
        else:
            summary.append('User does not have console management access')

        return summary

    @staticmethod
    def _get_sign_in_link(arn):
        sign_in_link = ''
        parse_arn = arn.split("::")[-1]
        if parse_arn.find(":") > 0:
            account_id = parse_arn[0:parse_arn.find(":")]
            sign_in_link = f'https://{account_id}.signin.aws.amazon.com/console'

        return sign_in_link

    @staticmethod
    def _get_matched_users_with_use_info(policies, policies_info):
        attached_policy_arn = {policy['PolicyArn'] for policy in policies_info}
        matching_policies = [p for p in policies if p.get('arn', '') in attached_policy_arn]
        return matching_policies

    @staticmethod
    def _get_name_from_tags(tags):
        for _tag in tags:
            if 'Name' in _tag.get('Key'):
                return _tag.get('Value')

        return None

    @staticmethod
    def _generate_key_query(key, value, delete, is_paginate=False, **query):
        if is_paginate:
            if delete != '':
                query.pop(delete, None)

            query.update({
                key: value,
                'PaginationConfig': {
                    'MaxItems': PAGINATOR_MAX_ITEMS,
                    'PageSize': PAGINATOR_PAGE_SIZE,
                }
            })

        return query

    @staticmethod
    def _generate_default_query(is_paginate=False, **query):
        if is_paginate:
            query.update({
                'PaginationConfig': {
                    'MaxItems': PAGINATOR_MAX_ITEMS,
                    'PageSize': PAGINATOR_PAGE_SIZE,
                }
            })

        return query

    @staticmethod
    def _get_trusted_relationship(role):
        trusted_relationship = []
        conditions = []
        trust_entities = []
        policy_document = role.get('AssumeRolePolicyDocument', {})
        statements = policy_document.get('Statement', [])

        for statement in statements:
            principal = statement.get('Principal', {})
            condition = statement.get('Condition', {})
            for k, v in condition.items():
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        conditions.append({
                            'condition': k,
                            'key': k2,
                            'value': v2
                        })

            if principal.get('Service', None) is not None:
                if isinstance(principal.get('Service'), list):
                    for svc in principal.get('Service', []):
                        trusted_relationship.append(svc)
                        trust_entities.append(f"AWS service: {svc}")
                else:
                    trusted_relationship.append(principal.get('Service'))
                    trust_entities.append(f"AWS service: {principal.get('Service')}")

            if principal.get('AWS', None) is not None:
                if isinstance(principal.get('AWS'), list):
                    for aws in principal.get('AWS', []):
                        trusted_relationship.append(aws)
                        trust_entities.append(f"Account: {aws}")
                else:
                    trusted_relationship.append(principal.get('AWS'))
                    trust_entities.append(f"Account: {principal.get('AWS')}")

            if principal.get('Federated', None) is not None:
                if isinstance(principal.get('Federated'), list):
                    for federate in principal.get('Federated', []):
                        trusted_relationship.append(federate)
                        trust_entities.append(f"Identity Provider: {federate}")
                else:
                    trusted_relationship.append(principal.get('Federated'))
                    trust_entities.append(f"Identity Provider: {principal.get('Federated')}")

        return trusted_relationship, conditions, trust_entities

    @staticmethod
    def _get_age_and_age_display(calculating_date):
        age = 0
        age_display = 'None'
        if calculating_date is not None:
            utc = datetime.utcnow()
            utc_now = utc.replace(tzinfo=timezone.utc)
            exp = utc_now - calculating_date
            age = exp.days
            if exp.days == 0:
                age_display = 'Today'
            else:
                age_display = f'{exp.days} days'

        return age, age_display

    @staticmethod
    def _get_role_last_used_and_activity(role_info):
        last_activity = 'None'
        role_last_used = role_info.get('RoleLastUsed', {})
        last_used_date = role_last_used.get('LastUsedDate', '')

        if last_used_date != '':
            utc = datetime.utcnow()
            utc_now = utc.replace(tzinfo=timezone.utc)
            exp = utc_now - last_used_date
            if exp.days == 0:
                last_activity = 'Today'
            else:
                last_activity = f'{exp.days} days'

        return role_last_used, last_activity

    @staticmethod
    def get_last_update_date_display(access_key_last_used):
        region = access_key_last_used.get('region', 'N/A')
        service_name = access_key_last_used.get('service_name', 'N/A')
        if region != 'N/A' and service_name != 'N/A':
            return f'{access_key_last_used.get("last_update_date")} with {service_name} in {region}'
        else:
            return 'N/A'


    @staticmethod
    def _get_provider_type(url):
        if url == '':
            return url
        else:
            provider_type = url.split('.')
            return provider_type[0].upper()

