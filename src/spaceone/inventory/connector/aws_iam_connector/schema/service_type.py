from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
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
        # TODO: GROUP MAIN TABLE FIELDS
    ],
    search=[
        # TODO: GROUP SEARCH META
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
        # TODO: USER MAIN TABLE FIELDS
    ],
    search=[
        # TODO: USER SEARCH META
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
        # TODO: ROLE MAIN TABLE FIELDS
    ],
    search=[
        # TODO: ROLE SEARCH META
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
        # TODO: POLICY MAIN TABLE FIELDS
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
