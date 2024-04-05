from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_documentdb_connector.schema.data import (
    Cluster,
    SubnetGroup,
    ParameterGroup,
)
from spaceone.inventory.libs.schema.resource import (
    CloudServiceResource,
    CloudServiceResponse,
    CloudServiceMeta,
)
from spaceone.inventory.libs.schema.dynamic_field import (
    TextDyField,
    ListDyField,
    BadgeDyField,
    EnumDyField,
    DateTimeDyField,
)
from spaceone.inventory.libs.schema.dynamic_layout import (
    ItemDynamicLayout,
    TableDynamicLayout,
    SimpleTableDynamicLayout,
)

# TAB - BASE
meta_base = ItemDynamicLayout.set_fields(
    "Clusters",
    fields=[
        TextDyField.data_source("DB Cluster", "data.db_cluster_identifier"),
        TextDyField.data_source("ARN", "data.db_cluster_arn"),
        EnumDyField.data_source(
            "Status",
            "data.status",
            default_state={
                "safe": ["available"],
                "warning": [
                    "maintenance",
                    "backing-up",
                    "creating",
                    "migrating",
                    "modifying",
                    "renaming",
                    "resetting-master-credentials",
                    "upgrading",
                ],
                "alert": [
                    "deleting",
                    "failing-over",
                    "inaccessible-encryption-credentials",
                    "migration-failed",
                ],
            },
        ),
        EnumDyField.data_source(
            "Engine", "data.engine", default_outline_badge=["docdb"]
        ),
        TextDyField.data_source("Version", "data.engine_version"),
        TextDyField.data_source("Cluster Endpoint", "data.endpoint"),
        TextDyField.data_source("Cluster Read Endpoint", "data.reader_endpoint"),
        TextDyField.data_source("Master User Name", "data.master_username"),
        TextDyField.data_source("Port", "data.port"),
        TextDyField.data_source(
            "Cluster Parameter group", "data.db_cluster_parameter_group"
        ),
        EnumDyField.data_source(
            "Deletion Protection",
            "data.deletion_protection",
            default_badge={"indigo.500": ["true"], "coral.600": ["false"]},
        ),
        ListDyField.data_source(
            "Enabled Cloudwatch Logs Exports",
            "data.enabled_cloudwatch_logs_exports",
            default_badge={"type": "outline"},
        ),
        ListDyField.data_source(
            "Availability Zones",
            "data.availability_zones",
            default_badge={"type": "outline"},
        ),
        DateTimeDyField.data_source("Creation Time", "data.cluster_create_time"),
    ],
)

cluster_sg = TableDynamicLayout.set_fields(
    "Security Groups",
    "data.vpc_security_groups",
    fields=[
        TextDyField.data_source("Security Group ID", "vpc_security_group_id"),
        EnumDyField.data_source("Status", "status", default_state={"safe": ["active"]}),
    ],
)

instances = TableDynamicLayout.set_fields(
    "Instances",
    "data.instances",
    fields=[
        TextDyField.data_source("Instance", "db_instance_identifier"),
        EnumDyField.data_source(
            "Status", "db_instance_status", default_state={"safe": ["available"]}
        ),
        TextDyField.data_source("Instance Type", "db_instance_class"),
        TextDyField.data_source("AZ", "availability_zone"),
        TextDyField.data_source("VPC ID", "db_subnet_group.vpc_id"),
        ListDyField.data_source(
            "Security Groups",
            "vpc_security_groups",
            default_badge={
                "type": "outline",
                "sub_key": "vpc_security_group_id",
                "delimiter": "<br>",
            },
        ),
        TextDyField.data_source("Instance Endpoint", "endpoint.address"),
        TextDyField.data_source("Port", "endpoint.port"),
        TextDyField.data_source("Certificate authority", "ca_certificate_identifier"),
    ],
)

snapshots = TableDynamicLayout.set_fields(
    "Snapshots",
    "data.snapshots",
    fields=[
        TextDyField.data_source("Snapshot", "db_cluster_snapshot_identifier"),
        EnumDyField.data_source(
            "Status", "status", default_state={"safe": ["available"]}
        ),
        TextDyField.data_source("Progress", "percent_progress"),
        EnumDyField.data_source(
            "Type",
            "snapshot_type",
            default_outline_badge=["automated", "manual", "shared", "public"],
        ),
        EnumDyField.data_source(
            "Encrypted",
            "storage_encrypted",
            default_badge={"indigo.500": ["true"], "coral.600": ["false"]},
        ),
        DateTimeDyField.data_source("Creation Time", "snapshot_create_time"),
    ],
)

cluster_subnet_groups = ItemDynamicLayout.set_fields(
    "Subnet Groups",
    "data.subnet_group",
    fields=[
        TextDyField.data_source("Name", "db_subnet_group_name"),
        TextDyField.data_source("ARN", "db_subnet_group_arn"),
        EnumDyField.data_source(
            "Status", "subnet_group_status", default_state={"safe": ["Complete"]}
        ),
        TextDyField.data_source("Description", "db_subnet_group_description"),
        ListDyField.data_source(
            "Subnet",
            "subnets",
            options={
                "sub_key": "subnet_identifier",
            },
        ),
    ],
)

cluster_parameter = TableDynamicLayout.set_fields(
    "Parameters",
    "data.parameter_group.parameters",
    fields=[
        TextDyField.data_source("Name", "parameter_name"),
        TextDyField.data_source("Value", "parameter_value"),
        TextDyField.data_source("Description", "description"),
    ],
)

cluster_metadata = CloudServiceMeta.set_layouts(
    layouts=[
        meta_base,
        cluster_sg,
        instances,
        snapshots,
        cluster_subnet_groups,
        cluster_parameter,
    ]
)

# SUBNET GROUP
subnet_group_base = ItemDynamicLayout.set_fields(
    "Subnet Groups",
    fields=[
        TextDyField.data_source("Name", "data.db_subnet_group_name"),
        TextDyField.data_source("ARN", "data.db_subnet_group_arn"),
        EnumDyField.data_source(
            "Status", "data.subnet_group_status", default_state={"safe": ["Complete"]}
        ),
        TextDyField.data_source("Description", "data.db_subnet_group_description"),
    ],
)

subnet = TableDynamicLayout.set_fields(
    "Subnets",
    "data.subnets",
    fields=[
        TextDyField.data_source("Availability Zone", "subnet_availability_zone.name"),
        TextDyField.data_source("Subnet ID", "subnet_identifier"),
        EnumDyField.data_source(
            "Subnet Group Status", "subnet_status", default_state={"safe": ["Active"]}
        ),
    ],
)

subnet_group_metadata = CloudServiceMeta.set_layouts(
    layouts=[subnet_group_base, subnet]
)

parameter_group_base = ItemDynamicLayout.set_fields(
    "Parameter Groups",
    fields=[
        TextDyField.data_source("Name", "data.db_cluster_parameter_group_name"),
        TextDyField.data_source("ARN", "data.db_cluster_parameter_group_arn"),
        BadgeDyField.data_source("Family", "data.db_parameter_group_family"),
        TextDyField.data_source("Description", "data.description"),
    ],
)

parameter = TableDynamicLayout.set_fields(
    "Parameters",
    "data.parameters",
    fields=[
        TextDyField.data_source("Name", "parameter_name"),
        TextDyField.data_source("Value", "parameter_value"),
        TextDyField.data_source("Allowed Values", "allowed_values"),
        EnumDyField.data_source(
            "Modifiable",
            "is_modifiable",
            default_badge={"indigo.500": ["true"], "coral.600": ["false"]},
        ),
        EnumDyField.data_source(
            "Apply Type", "apply_type", default_outline_badge=["static", "dynamic"]
        ),
        EnumDyField.data_source(
            "Data Type",
            "data_type",
            default_outline_badge=["string", "boolean", "integer", "list"],
        ),
        TextDyField.data_source("Description", "description"),
    ],
)

parameter_group_metadata = CloudServiceMeta.set_layouts(
    layouts=[parameter_group_base, parameter]
)


class DocumentDBResource(CloudServiceResource):
    cloud_service_group = StringType(default="DocumentDB")


class ClusterResource(DocumentDBResource):
    cloud_service_type = StringType(default="Cluster")
    data = ModelType(Cluster)
    _metadata = ModelType(
        CloudServiceMeta, default=cluster_metadata, serialized_name="metadata"
    )


class ClusterResponse(CloudServiceResponse):
    resource = PolyModelType(ClusterResource)


class SubnetGroupResource(DocumentDBResource):
    cloud_service_type = StringType(default="SubnetGroup")
    data = ModelType(SubnetGroup)
    _metadata = ModelType(
        CloudServiceMeta, default=subnet_group_metadata, serialized_name="metadata"
    )


class SubnetGroupResponse(CloudServiceResponse):
    resource = PolyModelType(SubnetGroupResource)


class ParameterGroupResource(DocumentDBResource):
    cloud_service_type = StringType(default="ParameterGroup")
    data = ModelType(ParameterGroup)
    _metadata = ModelType(
        CloudServiceMeta, default=parameter_group_metadata, serialized_name="metadata"
    )


class ParameterGroupResponse(CloudServiceResponse):
    resource = PolyModelType(ParameterGroupResource)
