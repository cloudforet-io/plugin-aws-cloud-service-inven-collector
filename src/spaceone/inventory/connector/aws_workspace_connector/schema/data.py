import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class endpointConfiguration(Model):
    types = ListType(StringType,deserialize_from="types")
    vpc_endpoint_ids = ListType(StringType,deserialize_from="vpcEndpointIds")


class tags(Model):
    string = StringType(deserialize_from="string")


class RestAPIs(Model):
    arn = StringType()
    id = StringType(deserialize_from="id")
    name = StringType(deserialize_from="name")
    description = StringType(deserialize_from="description")
    created_date = DateTimeType(deserialize_from="createdDate")
    version = StringType(deserialize_from="version")
    warnings = ListType(StringType,deserialize_from="warnings")
    binary_media_types = ListType(StringType,deserialize_from="binaryMediaTypes")
    minimum_compression_size = IntType(deserialize_from="minimumCompressionSize")
    api_key_source = StringType(deserialize_from="apiKeySource",choices=("HEADER","AUTHORIZER"))
    endpoint_configuration = ModelType(endpointConfiguration,deserialize_from="endpointConfiguration")
    policy = StringType(deserialize_from="policy")
    tags = ModelType(tags,deserialize_from="tags")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/"
        }
