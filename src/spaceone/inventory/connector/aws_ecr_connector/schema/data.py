import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, DictType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


'''
IMAGE
'''
class imageScanStatus(Model):
    status = StringType(deserialize_from="status", choices=("IN_PROGRESS", "COMPLETE", "FAILED"))
    description = StringType(deserialize_from="description")


class imageScanFindingsSummary(Model):
    image_scan_completed_at = DateTimeType(deserialize_from="imageScanCompletedAt")
    vulnerability_source_updated_at = DateTimeType(deserialize_from="vulnerabilitySourceUpdatedAt")
    finding_severity_counts = DictType(StringType, deserialize_from="findingSeverityCounts")


class Image(Model):
    registry_id = StringType(deserialize_from="registryId")
    repository_name = StringType(deserialize_from="repositoryName")
    image_digest = StringType(deserialize_from="imageDigest")
    image_tags = ListType(StringType, deserialize_from="imageTags")
    image_tags_display = ListType(StringType)
    image_uri = StringType(default='')
    image_size_in_bytes = IntType(deserialize_from="imageSizeInBytes")
    # image_size_in_megabytes = FloatType()
    image_pushed_at = DateTimeType(deserialize_from="imagePushedAt")
    image_scan_status = ModelType(imageScanStatus, deserialize_from="imageScanStatus")
    image_scan_findings_summary = ModelType(imageScanFindingsSummary, deserialize_from="imageScanFindingsSummary")

'''
REPOSITORY
'''
class imageScanningConfiguration(Model):
    scan_on_push = BooleanType(deserialize_from="scanOnPush")


class Repository(AWSCloudService):
    repository_arn = StringType(deserialize_from="repositoryArn")
    registry_id = StringType(deserialize_from="registryId")
    repository_name = StringType(deserialize_from="repositoryName")
    repository_uri = StringType(deserialize_from="repositoryUri")
    created_at = DateTimeType(deserialize_from="createdAt")
    image_tag_mutability = StringType(deserialize_from="imageTagMutability", choices=("MUTABLE", "IMMUTABLE"))
    image_scanning_configuration = ModelType(imageScanningConfiguration, deserialize_from="imageScanningConfiguration")
    images = ListType(ModelType(Image))

    def reference(self, region_code):
        return {
            "resource_id": self.repository_arn,
            "external_link": f"https://console.aws.amazon.com/ecr/repositories/{self.repository_name}/?region={region_code}"
        }

