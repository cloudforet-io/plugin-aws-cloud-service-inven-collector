import time
import logging
from typing import List
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_iam_connector.schema.data import Tags, PermissionsBoundary, Permission, \
    PermissionSummary, Policy, CredentialKeyInfo, User, Group, RoleLastUsed, Condition, Role, IdentityProvider
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
    service_name = 'iam'

    def get_resources(self):
        print("** IAM START **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_group_data(),
                'resource': GroupResource,
                'response_schema': GroupResponse
            },
            {
                'request_method': self.request_user_data(),
                'resource': UserResource,
                'response_schema': UserResponse
            },
            {
                'request_method': self.request_role_data(),
                'resource': RoleResource,
                'response_schema': RoleResponse
            },
            {
                'request_method': self.request_policy_data(),
                'resource': PolicyResource,
                'response_schema': PolicyResponse
            },
            {
                'request_method': self.request_identity_provider_data(),
                'resource': IdentityProviderResource,
                'response_schema': IdentityProviderResponse
            }
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' EBS Finished {time.time() - start_time} Seconds')
        return resources

    def request_group_data(self, region_name) -> List[Group]:
        paginator = self.client.get_paginator('list_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Groups', []):
                users = self.list_user_with_group_name(GroupName=raw['GroupName'])
                attached_policies = self.list_policy_with_group_name(GroupName=raw['GroupName'])

                raw.update({
                    'users': self._get_user_info_with_group(users),
                    'user_count': len(users),
                    'attached_permission': self._get_policies_info_with_group(attached_policies)
                })

                yield Group(raw, strict=False)

    def request_user_data(self, region_name) -> List[User]:
        paginator = self.client.get_paginator('describe_volumes')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Volumes', []):
                if name := self._get_name_from_tags(raw.get('Tags', [])):
                    raw['name'] = name


                yield User(raw, strict=False)

    def request_role_data(self, region_name) -> List[Role]:
        paginator = self.client.get_paginator('describe_volumes')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('Volumes', []):
                if name := self._get_name_from_tags(raw.get('Tags', [])):
                    raw['name'] = name

                attr = self.client.describe_volume_attribute(Attribute='productCodes', VolumeId=raw['VolumeId'])

                yield Role(raw, strict=False)

    def request_policy_data(self) -> List[Policy]:
        paginator = self.client.get_paginator('list_policies')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )


        for data in policies:
            for raw in data.get('Policies', []):


                yield Policy(raw, strict=False)


    def request_identity_provider_data(self) -> List[IdentityProvider]:
        response = self.client.list_open_id_connect_providers()

        for arn_vo in response.get('OpenIDConnectProviderList', []):
            arn = arn_vo.get('Arn')
            identity_provider = self.list_open_id_connect_provider_info_with_arn(arn)
            identity_provider.update({
                'arn': arn,
                'provider_type': self._get_provider_type(identity_provider.get('Url', ''))
            })

            yield IdentityProvider(identity_provider, strict=False)

    def list_user_with_group_name(self, group_name, **query):
        users = []
        query = self._generate_query(is_paginate=True, **query)
        query.update({
            'GroupName': group_name
        })
        paginator = self.client.get_paginator('get_group')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            users.extend(data.get('Users', []))

        return users

    def list_policy_with_group_name(self, group_name, **query):
        policies = []
        query = self._generate_query(is_paginate=True, **query)
        query.update({'GroupName': group_name})
        paginator = self.client.get_paginator('list_group_policies')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            policies.extend(data.get('PolicyNames', []))

        return policies


    def list_open_id_connect_provider_info_with_arn(self, oidcp_arn):
        response = self.client.get_open_id_connect_provider(OpenIDConnectProviderArn=oidcp_arn)
        return response

    def list_policies(self, **query):
        policies = []
        paginator = self.client.get_paginator('list_policies')
        query = self._generate_query(is_paginate=True, **query)
        query.update({'Scope': 'Local'})
        iterator_local = paginator.paginate(**query)
        query.update({'Scope': 'AWS'})
        iterator_aws = paginator.paginate(**query)

        for data in iterator_aws:
            po = [dict(policy, policy_type='AWS') for policy in data.get('Policies', [])]
            policies.extend(po)

        for data in iterator_local:
            po = [dict(policy, policy_type='Custom') for policy in data.get('Policies', [])]
            policies.extend(po)

        return policies

    @staticmethod
    def _get_name_from_tags(tags):
        for _tag in tags:
            if 'Name' in _tag.get('Key'):
                return _tag.get('Value')

        return None

    @staticmethod
    def _generate_query(is_paginate=False, **query):
        if is_paginate:
            query.update({
                'PaginationConfig': {
                    'MaxItems': PAGINATOR_MAX_ITEMS,
                    'PageSize': PAGINATOR_PAGE_SIZE,
                }
            })

        return query


    @staticmethod
    def _get_provider_type(url):
        if url == '':
            return url
        else:
            provider_type = url.split('.')
            return provider_type[0].upper()

