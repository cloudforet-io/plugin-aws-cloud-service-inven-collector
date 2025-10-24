import copy
import time
import logging
from typing import List
from datetime import datetime, timezone

from spaceone.inventory.connector.aws_iam_connector.schema.data import (
    Policy,
    AccessKeyLastUsed,
    User,
    Group,
    Role,
    IdentityProvider,
    AccessKey,
)
from spaceone.inventory.connector.aws_iam_connector.schema.resource import (
    GroupResource,
    GroupResponse,
    UserResource,
    UserResponse,
    RoleResource,
    RoleResponse,
    PolicyResource,
    PolicyResponse,
    IdentityProviderResource,
    IdentityProviderResponse,
    AccessKeyResource,
    AccessKeyResponse,
)
from spaceone.inventory.connector.aws_iam_connector.schema.service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import (
    ReferenceModel,
    CloudTrailModel,
)

_LOGGER = logging.getLogger(__name__)

PAGINATOR_MAX_ITEMS = 10000
PAGINATOR_PAGE_SIZE = 50


class IAMConnector(SchematicAWSConnector):
    group_response_schema = GroupResponse
    user_response_schema = UserResponse
    role_response_schema = RoleResponse
    policy_response_schema = PolicyResponse
    identity_provider_response_schema = IdentityProviderResponse
    access_key_response_schema = AccessKeyResponse

    service_name = "iam"
    cloud_service_group = "IAM"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: IAM")
        start_time = time.time()
        resources = []

        policy_errors = []
        user_errors = []

        resources.extend(self.set_cloud_service_types())

        try:
            policies, policy_errors = self.list_local_managed_policies()
            users, access_keys, user_errors = self.request_user_data(policies)

            for role, tags in self.request_role_data(policies):
                if (
                    getattr(role, "resource_type", None)
                    and role.resource_type == "inventory.ErrorResource"
                ):
                    # Error Resource
                    resources.append(role)
                else:
                    resources.append(
                        self.role_response_schema(
                            {
                                "resource": RoleResource(
                                    {
                                        "name": role.role_name,
                                        "data": role,
                                        "account": self.account_id,
                                        "tags": self.convert_tags_to_dict_type(tags),
                                        "reference": ReferenceModel(role.reference()),
                                        "region_code": "global",
                                    }
                                )
                            }
                        )
                    )

            for user in users:
                if (
                    getattr(user, "resource_type", None)
                    and user.resource_type == "inventory.ErrorResource"
                ):
                    # Error Resource
                    resources.append(user)
                else:
                    resources.append(
                        self.user_response_schema(
                            {
                                "resource": UserResource(
                                    {
                                        "name": user.user_name,
                                        "data": user,
                                        "account": self.account_id,
                                        "reference": ReferenceModel(user.reference()),
                                        "region_code": "global",
                                    }
                                )
                            }
                        )
                    )

            for group in self.request_group_data(users, policies):
                if (
                    getattr(group, "resource_type", None)
                    and group.resource_type == "inventory.ErrorResource"
                ):
                    # Error Resource
                    resources.append(group)
                else:
                    resources.append(
                        self.group_response_schema(
                            {
                                "resource": GroupResource(
                                    {
                                        "name": group.group_name,
                                        "data": group,
                                        "account": self.account_id,
                                        "reference": ReferenceModel(group.reference()),
                                        "region_code": "global",
                                    }
                                )
                            }
                        )
                    )

            for policy in policies:
                if (
                    getattr(policy, "resource_type", None)
                    and policy.resource_type == "inventory.ErrorResource"
                ):
                    # Error Resource
                    resources.append(policy)
                else:
                    resources.append(
                        self.policy_response_schema(
                            {
                                "resource": PolicyResource(
                                    {
                                        "name": policy.policy_name,
                                        "data": policy,
                                        "account": self.account_id,
                                        "reference": ReferenceModel(policy.reference()),
                                        "region_code": "global",
                                    }
                                )
                            }
                        )
                    )

            for identity_provider in self.request_identity_provider_data():
                if (
                    getattr(identity_provider, "resource_type", None)
                    and identity_provider.resource_type == "inventory.ErrorResource"
                ):
                    # Error Resource
                    resources.append(identity_provider)
                else:
                    resources.append(
                        self.identity_provider_response_schema(
                            {
                                "resource": IdentityProviderResource(
                                    {
                                        "name": identity_provider.url,
                                        "data": identity_provider,
                                        "account": self.account_id,
                                        "reference": ReferenceModel(
                                            identity_provider.reference()
                                        ),
                                        "region_code": "global",
                                    }
                                )
                            }
                        )
                    )

            for access_key in access_keys:
                if (
                    getattr(access_key, "resource_type", None)
                    and access_key.resource_type == "inventory.ErrorResource"
                ):
                    # Error Resource
                    resources.append(access_key)
                else:
                    resources.append(
                        self.access_key_response_schema(
                            {
                                "resource": AccessKeyResource(
                                    {
                                        "name": access_key.key_id,
                                        "data": access_key,
                                        "account": self.account_id,
                                        "reference": ReferenceModel(
                                            access_key.reference()
                                        ),
                                        "region_code": "global",
                                    }
                                )
                            }
                        )
                    )
        except Exception as e:
            resource_id = ""
            resources.append(self.generate_error("global", resource_id, e))

        resources.extend(policy_errors)
        resources.extend(user_errors)

        _LOGGER.debug(
            f"[get_resources][account_id: {self.account_id}] FINISHED: IAM ({time.time() - start_time} sec)"
        )
        return resources

    def request_group_data(self, users, policies) -> List[Group]:
        self.cloud_service_type = "Group"
        cloudtrail_resource_type = "AWS::IAM::Group"

        paginator = self.client.get_paginator("list_groups")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )

        for data in response_iterator:
            for group in data.get("Groups", []):
                try:
                    group_name = group.get("GroupName")
                    group_user_info = self.list_user_with_group_name(group_name)
                    matched_users = self._get_matched_users_with_attached_user_info(
                        users, group_user_info
                    )
                    attached_managed_policies = self.list_attached_managed_policy_to_group(group_name)
                    attached_inline_policies = self.list_attached_inline_policy_to_group(group_name)

                    matched_policies = (
                        self.get_matched_policies_with_attached_policy_info(
                            policies, attached_managed_policies, attached_inline_policies
                        )
                    )

                    group.update(
                        {
                            "users": matched_users,
                            "user_count": len(group_user_info),
                            "attached_permission": matched_policies,
                            "cloudtrail": self.set_cloudtrail(
                                "us-east-1",
                                cloudtrail_resource_type,
                                group["GroupName"],
                            ),
                        }
                    )

                    yield Group(group, strict=False)
                except Exception as e:
                    resource_id = group.get("Arn", "")
                    error_resource_response = self.generate_error(
                        "global", resource_id, e
                    )
                    yield error_resource_response

    def request_user_data(self, policies):
        self.cloud_service_type = "User"
        cloudtrail_resource_type = "AWS::IAM::User"

        paginator = self.client.get_paginator("list_users")
        query = self._generate_default_query()
        response_iterator = paginator.paginate(**query)

        users = []
        access_keys = []
        errors = []

        for data in response_iterator:
            for user in data.get("Users", []):
                try:
                    user_name = user.get("UserName")
                    user_arn = user.get("Arn")
                    user_info = self.get_user_info(user_name)
                    mfa_devices = self.list_mfa_devices(user_name)
                    _access_keys = self.list_access_keys(user_name, user_arn)
                    login_profile = self.get_login_profile(user_name)
                    groups = self.list_groups_with_user_name(user_name)

                    self._conditional_update_for_password_last_used(user, user_info)
                    self.conditional_update_for_access_key_age_and_access_key_age_display(
                        user, _access_keys
                    )
                    (
                        code_commit_credential,
                        cassandra_credential,
                    ) = self.list_service_specific_credentials(user_name)
                    last_active_age, last_activity = self._get_age_and_age_display(
                        user_info.get("PasswordLastUsed", None)
                    )
                    sign_in_link = self._get_sign_in_link(user_info.get("Arn"))

                    attached_managed_policies = self.list_attached_managed_policy_to_user(user_name)
                    attached_inline_policies = self.list_attached_inline_policy_to_user(user_name)

                    matching_policies = (
                        self.get_matched_policies_with_attached_policy_info(
                            policies, attached_managed_policies, attached_inline_policies
                        )
                    )

                    user.update(
                        {
                            "access_key": _access_keys,
                            "ssh_public_key": self.list_ssh_keys(user_name),
                            "code_commit_credential": code_commit_credential,
                            "cassandra_credential": cassandra_credential,
                            "mfa_device": (
                                "Virtual" if len(mfa_devices) > 0 else "Not enabled"
                            ),
                            "last_active_age": last_active_age,
                            "last_activity": last_activity,
                            "policies": matching_policies,
                            "groups_display": (
                                groups[0].get("GroupName", "")
                                if len(groups) > 0
                                else ""
                            ),
                            "groups": self.get_groups_for_user(groups),
                            "sign_in_credential": {
                                "summary": self._get_summary_with_login_profile(
                                    login_profile, sign_in_link, mfa_devices
                                ),
                                "console_password": (
                                    "Enabled"
                                    if login_profile is not None
                                    else "Disabled"
                                ),
                                "assigned_mfa_device": (
                                    user_info.get("Arn")
                                    if len(mfa_devices) > 0
                                    else "Not assigned"
                                ),
                            },
                            "cloudtrail": self.set_cloudtrail(
                                "us-east-1", cloudtrail_resource_type, user["UserName"]
                            ),
                            "tags": user_info.get("Tags", []),
                        }
                    )
                    users.append(User(user, strict=False))
                    access_keys.extend([AccessKey(_key) for _key in _access_keys])

                except Exception as e:
                    resource_id = user.get("Arn", "")
                    errors.append(self.generate_error("global", resource_id, e))

        return users, access_keys, errors

    def request_role_data(self, policies) -> List[Role]:
        self.cloud_service_type = "Role"
        cloudtrail_resource_type = "AWS::IAM::Role"

        paginator = self.client.get_paginator("list_roles")
        query = self._generate_default_query()
        response_iterator = paginator.paginate(**query)

        for response in response_iterator:
            for role in response.get("Roles", []):
                try:
                    role_name = role.get("RoleName")
                    role_info = self.list_role_info_with_role_name(role_name)
                    (
                        role_last_used,
                        last_activity,
                    ) = self._get_role_last_used_and_activity(role_info)

                    attached_managed_policies = self.list_attached_managed_policy_to_role(role_name)
                    attached_inline_policies = self.list_attached_inline_policy_to_role(role_name)

                    matched_policies = (
                        self.get_matched_policies_with_attached_policy_info(
                            policies, attached_managed_policies, attached_inline_policies
                        )
                    )
                    (
                        assume_role_policy_document,
                        trust_entities,
                        trusted_relationship,
                        conditions,
                    ) = self._get_role_policy_doc_and_trusted_entities_and_relationship_meta(
                        role
                    )

                    role.update(
                        {
                            "AssumeRolePolicyDocument": assume_role_policy_document,
                            "trust_relationship": [
                                {
                                    "trusted_entities": trusted_relationship,
                                    "condition_name": conditions.get(
                                        "condition_name", []
                                    ),
                                    "condition_key": conditions.get(
                                        "condition_key", []
                                    ),
                                    "condition_value": conditions.get(
                                        "condition_value", []
                                    ),
                                }
                            ],
                            "trusted_entities": trust_entities,
                            "policies": matched_policies,
                            "role_last_used": role_last_used,
                            "last_activity": last_activity,
                            "cloudtrail": self.set_cloudtrail(
                                "us-east-1", cloudtrail_resource_type, role["RoleName"]
                            ),
                        }
                    )

                    yield Role(role, strict=False), role.get("Tags", [])
                except Exception as e:
                    resource_id = role.get("Arn", "")
                    error_resource_response = self.generate_error(
                        "global", resource_id, e
                    )
                    yield error_resource_response, []

    def request_identity_provider_data(self) -> List[IdentityProvider]:
        self.cloud_service_type = "IdentityProvider"
        cloudtrail_resource_type = "AWS::IAM::OpenIDConnectProvider"

        response = self.client.list_open_id_connect_providers()

        for arn_dict in response.get("OpenIDConnectProviderList", []):
            try:
                arn = arn_dict.get("Arn")
                identity_provider = self.get_open_id_connect_provider_info_with_arn(arn)
                identity_provider.update(
                    {
                        "arn": arn,
                        "cloudtrail": self.set_cloudtrail(
                            "us-east-1", cloudtrail_resource_type, arn_dict["Arn"]
                        ),
                        "provider_type": self._get_provider_type(
                            identity_provider.get("Url", "")
                        ),
                    }
                )

                yield IdentityProvider(identity_provider, strict=False)
            except Exception as e:
                resource_id = arn_dict.get("Arn", "")
                error_resource_response = self.generate_error("global", resource_id, e)
                yield error_resource_response

    def conditional_update_for_access_key_age_and_access_key_age_display(
        self, user, access_keys
    ):
        if access_keys:
            access_key_date = access_keys[0].get("create_date")
            age, display = self._get_age_and_age_display(access_key_date)
            # Create access_key_age_status
            age_status = "~30"
            if age > 180:
                age_status = "181~"
            elif age > 150:
                age_status = "151~180"
            elif age > 120:
                age_status = "121~150"
            elif age > 90:
                age_status = "91~120"
            elif age > 60:
                age_status = "61~90"
            elif age > 30:
                age_status = "31~60"
            user.update(
                {
                    "access_key_age": age,
                    "access_key_age_display": display,
                    "access_key_age_status": age_status,
                }
            )
        else:
            user.update(
                {
                    "access_key_age": 0,
                    "access_key_age_display": "None",
                    "access_key_age_status": "NO Key",
                }
            )

    def get_user_info(self, user_name):
        response = self.client.get_user(UserName=user_name)
        return response.get("User", {})

    def get_login_profile(self, user_name):
        login_profile = None
        try:
            response = self.client.get_login_profile(UserName=user_name)
            login_profile = response.get("LoginProfile", {})
        except Exception as e:
            pass
            # print(f'[ERROR: No login_profile with {user_name}] : {e}')
            # print(f' no login_profile data found with {user_name}')

        return login_profile

    def list_local_managed_policies(self, **query):
        self.cloud_service_type = "Policy"
        cloudtrail_resource_type = "AWS::IAM::Policy"

        policies = []
        errors = []

        policy_paginator = self.client.get_paginator("list_policies")

        query = self._generate_key_query(
            "Scope", "Local", "", is_paginate=True, **query
        )
        response_iterator_local = policy_paginator.paginate(**query)

        for data in response_iterator_local:
            for policy in data.get("Policies", []):
                try:
                    policy_arn = policy.get("Arn")
                    description = self.list_policy_description(policy_arn)

                    permission_summary = self.list_policy_summary(
                        policy_arn, policy.get("DefaultVersionId")
                    )
                    policy.update(
                        {
                            "description": description,
                            "policy_usage": self.list_policy_usage(policy_arn),
                            "permission": permission_summary,
                            "permission_versions": self.list_policy_versions(
                                policy_arn
                            ),
                            "cloudtrail": self.set_cloudtrail(
                                "us-east-1", cloudtrail_resource_type, policy["Arn"]
                            ),
                            "policy_type": "Customer Managed",
                        }
                    )

                    policies.append(Policy(policy, strict=False))

                except Exception as e:
                    resource_id = policy.get("Arn", "")
                    errors.append(self.generate_error("global", resource_id, e))

        return policies, errors

    def list_access_keys(self, user_name, user_arn):
        self.cloud_service_type = "AccessKey"
        cloudtrail_resource_type = "AWS::IAM::AccessKey"

        access_keys = []
        _filter = {"UserName": user_name}
        query = self._generate_query(filter_dict=_filter, is_paginate=True)

        paginator = self.client.get_paginator("list_access_keys")
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            for access_key_meta in data.get("AccessKeyMetadata", []):
                key_id = access_key_meta.get("AccessKeyId")
                access_key_last_used_vo = AccessKeyLastUsed(
                    self.get_access_key_last_used(key_id), strict=False
                )
                access_key_vo = {
                    "key_id": key_id,
                    "user_name": user_name,
                    "user_arn": user_arn,
                    "create_date": access_key_meta.get("CreateDate"),
                    "access_key_last_used": access_key_last_used_vo,
                    "last_update_date_display": self.get_last_update_date_display(
                        access_key_last_used_vo
                    ),
                    "status": str(access_key_meta.get("Status", "")),
                    "cloudtrail": CloudTrailModel(
                        {
                            "LookupAttributes": [
                                {
                                    "AttributeKey": "AccessKeyId",
                                    "AttributeValue": key_id,
                                }
                            ],
                            "resource_type": cloudtrail_resource_type,
                            "region_name": "us-east-1",
                        },
                        strict=False,
                    ),
                }
                access_keys.append(access_key_vo)

        return access_keys

    def list_ssh_keys(self, user_name, **query):
        ssh_keys = []
        query = self._generate_key_query(
            "UserName", user_name, "", is_paginate=True, **query
        )
        paginator = self.client.get_paginator("list_ssh_public_keys")
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            for ssh_key in data.get("SSHPublicKeys", []):
                ssh_keys.append(
                    {
                        "key_id": ssh_key.get("SSHPublicKeyId", ""),
                        "status": ssh_key.get("Status", ""),
                        "upload_date": ssh_key.get("UploadDate"),
                    }
                )

        return ssh_keys

    def list_mfa_devices(self, user_name):
        response = self.client.list_mfa_devices(UserName=user_name)
        return response.get("MFADevices", [])

    def list_service_specific_credentials(self, user_name):
        code_commit_credential = []
        cassandra_credential = []
        response = self.client.list_service_specific_credentials(UserName=user_name)
        service_specific_credentials = response.get("ServiceSpecificCredentials", [])
        for ssc in service_specific_credentials:
            if "UserName" in ssc:
                ssc.pop("UserName", None)

            if ssc.get("ServiceName", "") == "codecommit.amazonaws.com":
                code_commit_credential.append(ssc)
            elif ssc.get("ServiceName", "") == "cassandra.amazonaws.com":
                cassandra_credential.append(ssc)

        return code_commit_credential, cassandra_credential

    def list_groups_with_user_name(self, user_name, **query):
        groups = []
        query = self._generate_key_query(
            "UserName", user_name, "", is_paginate=True, **query
        )
        paginator = self.client.get_paginator("list_groups_for_user")
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            groups.extend(data.get("Groups", []))

        return groups

    def list_user_with_group_name(self, group_name, **query):
        users = []
        query = self._generate_key_query(
            "GroupName", group_name, "", is_paginate=True, **query
        )
        paginator = self.client.get_paginator("get_group")
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            users.extend(data.get("Users", []))

        return users

    def get_groups_for_user(self, groups):
        groups_for_user = []
        for group in groups:
            group_name = group.get("GroupName")
            policy_vos = self.list_attached_managed_policy_to_group(group_name)
            groups_for_user.append(
                {
                    "group_name": group_name,
                    "attached_policy_name": [
                        d["PolicyName"] for d in policy_vos if "PolicyName" in d
                    ],
                    "create_date": group.get("CreateDate"),
                }
            )

        return groups_for_user

    def list_role_info_with_role_name(self, role_name):
        response = self.client.get_role(RoleName=role_name)
        return response.get("Role", {})

    def list_attached_managed_policy_to_group(self, group_name, **query):
        response = self.client.list_attached_group_policies(GroupName=group_name)
        return response.get("AttachedPolicies", [])

    def list_attached_managed_policy_to_user(self, user_name):
        response = self.client.list_attached_user_policies(UserName=user_name)
        return response.get("AttachedPolicies", [])

    def list_attached_managed_policy_to_role(self, role_name):
        response = self.client.list_attached_role_policies(RoleName=role_name)
        return response.get("AttachedPolicies", [])

    def list_attached_inline_policy_to_group(self, group_name, **query):
        response = self.client.list_group_policies(GroupName=group_name)
        policy_names = response.get("PolicyNames", [])

        return self._generate_policy_data(policy_names)

    def list_attached_inline_policy_to_user(self, user_name):
        response = self.client.list_user_policies(UserName=user_name)
        policy_names = response.get("PolicyNames", [])

        return self._generate_policy_data(policy_names)

    def list_attached_inline_policy_to_role(self, role_name):
        response = self.client.list_role_policies(RoleName=role_name)
        policy_names = response.get("PolicyNames", [])

        return self._generate_policy_data(policy_names)

    @staticmethod
    def _generate_policy_data(policy_names):
        policies = []

        if policy_names:
            for policy_name in policy_names:
                print(policy_name)
                policy = {
                    "PolicyName": policy_name,
                    "policy_type": "Customer Inline"
                }

                policies.append(Policy(policy, strict=False))

        return policies


    def get_open_id_connect_provider_info_with_arn(self, oidcp_arn):
        response = self.client.get_open_id_connect_provider(
            OpenIDConnectProviderArn=oidcp_arn
        )
        return response

    def get_access_key_last_used(self, access_key_id):
        response = self.client.get_access_key_last_used(AccessKeyId=access_key_id)
        return response.get("AccessKeyLastUsed", {})

    def get_policy_info(self, policy_arn):
        return self.client.get_policy(PolicyArn=policy_arn).get("Policy", {})

    def list_policy_description(self, policy_arn):
        policy_info = self.client.get_policy(PolicyArn=policy_arn).get("Policy", {})
        return policy_info.get("Description", "")

    def list_policy_versions(self, policy_arn, **query):
        versions = []
        query = self._generate_key_query(
            "PolicyArn", policy_arn, "", is_paginate=True, **query
        )
        paginator = self.client.get_paginator("list_policy_versions")
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            versions.extend(data.get("Versions", []))

        return versions

    def list_policy_summary(self, policy_arn, version_id):
        policy_info = self.client.get_policy_version(
            PolicyArn=policy_arn, VersionId=version_id
        ).get("PolicyVersion", {})
        empty_permission_summary = {"Statement": [], "Version": "N/A"}
        return_value = policy_info.get("Document", empty_permission_summary)
        statements = []

        if isinstance(return_value.get("Statement"), list):
            for statement in return_value.get("Statement"):
                statements.append(self.get_appropriate_format_statement(statement))

        elif isinstance(return_value.get("Statement"), dict):
            statements.append(
                self.get_appropriate_format_statement(return_value.get("Statement"))
            )

        return_value.update({"Statement": statements})
        return return_value

    def get_matched_policies_with_attached_policy_info(
        self, policies, attached_managed_policies, attached_inline_policies
    ):
        matched_policies = []

        # Managed Policy
        attached_managed_policy_arn = [
            policy.get("PolicyArn", "") for policy in attached_managed_policies
        ]

        for policy_arn in attached_managed_policy_arn:
            policy = [p for p in policies if p.get("arn", "") == policy_arn]
            if not policy:
                aws_managed_policy = self.get_policy_info(policy_arn)
                permission_summary = self.list_policy_summary(
                    policy_arn, aws_managed_policy.get("DefaultVersionId")
                )
                aws_managed_policy.update(
                    {
                        "policy_usage": self.list_policy_usage(policy_arn),
                        "permission": permission_summary,
                        "permission_versions": self.list_policy_versions(policy_arn),
                        "policy_type": "AWS Managed",
                    }
                )
                matched_policies.append(Policy(aws_managed_policy, strict=False))
            else:
                matched_policies.extend(policy)

        #Inline Policy
        if attached_inline_policies:
            matched_policies.extend(attached_inline_policies)

        return matched_policies

    def list_policy_usage(self, policy_arn, **query):
        query = self._generate_key_query(
            "PolicyArn", policy_arn, "", is_paginate=True, **query
        )
        paginator = self.client.get_paginator("list_entities_for_policy")
        iterator_response = paginator.paginate(**query)
        policy_usage = []
        for response in iterator_response:
            group = [
                {"name": d["GroupName"], "type": "Group"}
                for d in response.get("PolicyGroups", [])
                if "GroupName" in d
            ]
            role = [
                {"name": d["RoleName"], "type": "Role"}
                for d in response.get("PolicyRoles", [])
                if "RoleName" in d
            ]
            user = [
                {"name": d["UserName"], "type": "User"}
                for d in response.get("PolicyUsers", [])
                if "UserName" in d
            ]
            policy_usage = [*group, *role, *user]

        return policy_usage

    def list_versions_from_policy(self, policy_arn, **query):
        policy_versions = []
        paginator = self.client.get_paginator("list_policy_versions")
        query = self._generate_default_query(is_paginate=True, **query)
        query.update({"PolicyArn": policy_arn})
        iterator_response = paginator.paginate(**query)

        for data in iterator_response:
            policy_versions.extend(data.get("Versions", []))

        return policy_versions

    def get_appropriate_format_statement(self, candidate):
        action = self._switch_to_list(candidate.get("Action", []))
        resource = self._switch_to_list(candidate.get("Resource", []))
        effect = candidate.get("Effect", "")
        condition = candidate.get("Condition")
        sid = candidate.get("Sid")

        statement_candidate = {
            "action": action,
            "resource": resource,
            "effect": effect,
        }

        if condition is not None:
            conditions = []
            for k, v in condition.items():
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        if isinstance(v2, list):
                            for value_in_v2 in v2:
                                conditions.append(
                                    {
                                        "condition_name": k,
                                        "key": k2,
                                        "value": self._change_to_string(value_in_v2),
                                    }
                                )
                        else:
                            conditions.append(
                                {
                                    "condition_name": k,
                                    "key": k2,
                                    "value": self._change_to_string(v2),
                                }
                            )
            statement_candidate.update({"condition": conditions})

        if sid is not None:
            statement_candidate.update({"sid": sid})

        return statement_candidate

    @staticmethod
    def _get_role_policy_doc_and_trusted_entities_and_relationship_meta(role):
        policy_document = role.get("AssumeRolePolicyDocument", {})
        trusted_relationship = []
        trust_entities = []
        conditions = {"condition_name": [], "condition_key": [], "condition_value": []}

        modified_statements = []
        type_modify_version = policy_document.get("Version", "")
        type_modify_statement = policy_document.get("Statement", [])
        statements = policy_document.get("Statement", [])

        if isinstance(type_modify_statement, dict):
            statements = [type_modify_statement]

        for statement in statements:
            inner_principal = []
            inner_condition = []

            inner_action = (
                statement.get("Action", [])
                if isinstance(statement.get("Action", []), list)
                else [statement.get("Action", [])]
            )
            inner_effect = (
                statement.get("Effect", [])
                if isinstance(statement.get("Effect", []), list)
                else [statement.get("Effect", [])]
            )
            inner_sid = (
                statement.get("Sid", [])
                if isinstance(statement.get("Sid", []), list)
                else [statement.get("Sid", [])]
            )
            principal = statement.get("Principal", {})
            condition = statement.get("Condition", {})

            for k, v in condition.items():
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        condition_value = " / ".join(v2) if isinstance(v2, list) else v2
                        cond = {"condition": k, "key": k2, "value": condition_value}

                        inner_condition.append(cond)
                        conditions.get("condition_name").append(k)
                        conditions.get("condition_key").append(k2)
                        conditions.get("condition_value").append(condition_value)

            if principal.get("Service", None) is not None:
                if isinstance(principal.get("Service"), list):
                    for svc in principal.get("Service", []):
                        trusted_relationship.append(svc)
                        trust_entities.append(f"AWS service: {svc}")
                        inner_principal.append({"key": "service", "value": svc})
                else:
                    trusted_relationship.append(principal.get("Service"))
                    trust_entities.append(f"AWS service: {principal.get('Service')}")
                    inner_principal.append(
                        {"key": "service", "value": principal.get("Service")}
                    )

            if principal.get("AWS", None) is not None:
                if isinstance(principal.get("AWS"), list):
                    for aws in principal.get("AWS", []):
                        trusted_relationship.append(aws)
                        trust_entities.append(f"Account: {aws}")
                        inner_principal.append({"key": "aws", "value": aws})
                else:
                    trusted_relationship.append(principal.get("AWS"))
                    trust_entities.append(f"Account: {principal.get('AWS')}")
                    inner_principal.append(
                        {"key": "aws", "value": principal.get("AWS")}
                    )

            if principal.get("Federated", None) is not None:
                if isinstance(principal.get("Federated"), list):
                    for federate in principal.get("Federated", []):
                        trusted_relationship.append(federate)
                        trust_entities.append(f"Identity Provider: {federate}")
                        inner_principal.append({"key": "federated", "value": federate})
                else:
                    trusted_relationship.append(principal.get("Federated"))
                    trust_entities.append(
                        f"Identity Provider: {principal.get('Federated')}"
                    )
                    inner_principal.append(
                        {"key": "federated", "value": principal.get("Federated")}
                    )

            modified_statements.append(
                {
                    "action": inner_action,
                    "effect": inner_effect,
                    "condition": inner_condition,
                    "principal": inner_principal,
                    "sid": inner_sid,
                }
            )

        assume_role_policy_document = (
            {}
            if type_modify_version == ""
            else {"statement": modified_statements, "version": type_modify_version}
        )

        return (
            assume_role_policy_document,
            trust_entities,
            trusted_relationship,
            conditions,
        )

    @staticmethod
    def _switch_to_list(item):
        return item if isinstance(item, list) else [item]

    @staticmethod
    def _conditional_update_for_password_last_used(user, user_info):
        password_last_used = user_info.get("PasswordLastUsed", None)
        if password_last_used is not None:
            user.update({"password_last_used": password_last_used})

    @staticmethod
    def _get_console_password_with_login_profile(login_profile):
        return "Enable" if login_profile is not None else "Disable"

    @staticmethod
    def _get_summary_with_login_profile(login_profile, sign_in_link, mfa_devices):
        summary = []
        if login_profile is not None:
            if sign_in_link != "":
                summary.append(f"• Console sign-in link: {sign_in_link}")
            if len(mfa_devices) > 0:
                summary.append("• MFA is required when signing in.")
        else:
            summary.append("• User does not have console management access")

        return summary

    @staticmethod
    def _get_sign_in_link(arn):
        sign_in_link = ""
        parse_arn = arn.split("::")[-1]
        if parse_arn.find(":") > 0:
            account_id = parse_arn[0 : parse_arn.find(":")]
            sign_in_link = f"https://{account_id}.signin.aws.amazon.com/console"

        return sign_in_link

    @staticmethod
    def _get_matched_users_with_attached_user_info(users, user_info):
        user_names = [d["UserName"] for d in user_info if "UserName" in d]
        matched_users = [p for p in users if p.get("user_name", "") in user_names]
        return matched_users

    @staticmethod
    def _get_name_from_tags(tags):
        for _tag in tags:
            if "Name" in _tag.get("Key"):
                return _tag.get("Value")

        return None

    @staticmethod
    def _generate_query(filter_dict: dict = {}, is_paginate: bool = False) -> dict:
        query = copy.deepcopy(filter_dict)

        if is_paginate:
            query.update(
                {
                    "PaginationConfig": {
                        "MaxItems": PAGINATOR_MAX_ITEMS,
                        "PageSize": PAGINATOR_PAGE_SIZE,
                    }
                }
            )

        return query

    @staticmethod
    def _generate_key_query(key, value, delete, is_paginate=False, **query):
        if is_paginate:
            if delete != "":
                query.pop(delete, None)

            query.update(
                {
                    key: value,
                    "PaginationConfig": {
                        "MaxItems": PAGINATOR_MAX_ITEMS,
                        "PageSize": PAGINATOR_PAGE_SIZE,
                    },
                }
            )

        return query

    @staticmethod
    def _generate_default_query(is_paginate=False, **query):
        if is_paginate:
            query.update(
                {
                    "PaginationConfig": {
                        "MaxItems": PAGINATOR_MAX_ITEMS,
                        "PageSize": PAGINATOR_PAGE_SIZE,
                    }
                }
            )

        return query

    @staticmethod
    def _get_age_and_age_display(calculating_date):
        age = 0
        age_display = "None"

        if calculating_date:
            utc = datetime.utcnow()
            utc_now = utc.replace(tzinfo=timezone.utc)
            exp = utc_now - calculating_date
            age = int(exp.days)
            if age == 0:
                age_display = "Today"
            else:
                age_display = f"{age} days"

        return age, age_display

    @staticmethod
    def _get_role_last_used_and_activity(role_info):
        last_activity = "None"
        role_last_used = role_info.get("RoleLastUsed", {})
        last_used_date = role_last_used.get("LastUsedDate", "")

        if last_used_date != "":
            utc = datetime.utcnow()
            utc_now = utc.replace(tzinfo=timezone.utc)
            exp = utc_now - last_used_date
            if exp.days == 0:
                last_activity = "Today"
            else:
                last_activity = f"{exp.days} days"

        return role_last_used, last_activity

    @staticmethod
    def get_last_update_date_display(access_key_last_used):
        region = access_key_last_used.get("region", "N/A")
        service_name = access_key_last_used.get("service_name", "N/A")
        if region != "N/A" and service_name != "N/A":
            return f'{access_key_last_used.get("last_update_date")} with {service_name} in {region}'
        else:
            return "N/A"

    @staticmethod
    def _change_to_string(value):
        if isinstance(value, str):
            return value
        elif isinstance(value, bool):
            bool_to_string = str(value)
            return bool_to_string.lower()
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, int):
            return str(value)
        else:
            return ""

    @staticmethod
    def _get_provider_type(url):
        if url == "":
            return url
        else:
            provider_type = url.split(".")
            return provider_type[0].upper()
