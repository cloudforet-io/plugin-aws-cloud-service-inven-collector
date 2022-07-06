import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType, DictType
from spaceone.inventory.libs.schema.resource import CloudWatchDimensionModel
from spaceone.inventory.libs.schema.resource import AWSCloudService


_LOGGER = logging.getLogger(__name__)

'''
HTTP WEBSOCKET
'''
class CorsConfiguration(Model):
    allow_credentials = BooleanType(deserialize_from="AllowCredentials", serialize_when_none=False)
    allow_headers = ListType(StringType, deserialize_from="AllowHeaders", serialize_when_none=False)
    allow_methods = ListType(StringType, deserialize_from="AllowMethods", serialize_when_none=False)
    allow_origins = ListType(StringType, deserialize_from="AllowOrigins", serialize_when_none=False)
    expose_headers = ListType(StringType, deserialize_from="ExposeHeaders", serialize_when_none=False)
    max_age = IntType(deserialize_from="MaxAge", serialize_when_none=False)


class HTTPWebsocket(AWSCloudService):
    arn = StringType()
    name = StringType(deserialize_from="Name")
    api_endpoint = StringType(deserialize_from="ApiEndpoint", serialize_when_none=False)
    id = StringType(deserialize_from="ApiId")
    protocol = StringType(choices=('REST', 'HTTP', 'WEBSOCKET'))
    endpoint_type = StringType()
    api_key_selection_expression = StringType(deserialize_from="ApiKeySelectionExpression", serialize_when_none=False)
    cors_configuration = ModelType(CorsConfiguration, deserialize_from="CorsConfiguration", serialize_when_none=False)
    created_date = DateTimeType(deserialize_from="CreatedDate", serialize_when_none=False)
    description = StringType(deserialize_from="Description", default="")
    disable_schema_validation = BooleanType(deserialize_from="DisableSchemaValidation", serialize_when_none=False)
    import_info = ListType(StringType,deserialize_from="ImportInfo", serialize_when_none=False)
    protocol_type = StringType(deserialize_from="ProtocolType", choices=("WEBSOCKET", "HTTP"))
    route_selection_expression = StringType(deserialize_from="RouteSelectionExpression", serialize_when_none=False)
    version = StringType(deserialize_from="Version", serialize_when_none=False)
    warnings = ListType(StringType, deserialize_from="Warnings", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/apigateway/home?region={region_code}#/apis/{self.id}/routes"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/ApiGateway",
            "dimensions": [CloudWatchDimensionModel({'Name': 'ApiId', 'Value': self.id})],
            "region_name": region_code
        }


'''
REST API
'''
class EndpointConfiguration(Model):
    types = ListType(StringType, deserialize_from="types", choices=("REGIONAL", "EDGE", "PRIVATE"))
    vpc_endpoint_ids = ListType(StringType, deserialize_from="vpcEndpointIds", serialize_when_none=False)


class IntegrationResponsesInfo(Model):
    status_code = StringType(deserialize_from="statusCode", serialize_when_none=False)
    selection_pattern = StringType(deserialize_from="selectionPattern", serialize_when_none=False)
    response_parameters = DictType(StringType, deserialize_from="responseParameters", serialize_when_none=False)
    response_templates = DictType(StringType, deserialize_from="responseTemplates", serialize_when_none=False)
    content_handling = StringType(deserialize_from="contentHandling", choices=("CONVERT_TO_BINARY", "CONVERT_TO_TEXT"))


class IntegrationResponses(Model):
    method = ModelType(IntegrationResponsesInfo, deserialize_from="string", serialize_when_none=False)


class MethodIntegration(Model):
    type = StringType(deserialize_from="type", choices=("HTTP", "AWS", "MOCK", "HTTP_PROXY", "AWS_PROXY"))
    http_method = StringType(deserialize_from="httpMethod", serialize_when_none=False)
    uri = StringType(deserialize_from="uri", serialize_when_none=False)
    connection_type = StringType(deserialize_from="connectionType", choices=("INTERNET", "VPC_LINK"))
    connection_id = StringType(deserialize_from="connectionId", serialize_when_none=False)
    credentials = StringType(deserialize_from="credentials", serialize_when_none=False)
    request_parameters = DictType(StringType, deserialize_from="requestParameters", serialize_when_none=False)
    request_templates = DictType(StringType, deserialize_from="requestTemplates", serialize_when_none=False)
    passthrough_behavior = StringType(deserialize_from="passthroughBehavior", serialize_when_none=False)
    content_handling = StringType(deserialize_from="contentHandling", choices=("CONVERT_TO_BINARY", "CONVERT_TO_TEXT"))
    timeout_in_millis = IntType(deserialize_from="timeoutInMillis", serialize_when_none=False)
    cache_namespace = StringType(deserialize_from="cacheNamespace", serialize_when_none=False)
    cache_key_parameters = ListType(StringType, deserialize_from="cacheKeyParameters", serialize_when_none=False)
    integration_responses = ModelType(IntegrationResponses, deserialize_from="integrationResponses",
                                      serialize_when_none=False)


class MethodResponsesInfo(Model):
    status_code = StringType(deserialize_from="statusCode", serialize_when_none=False)
    response_parameters = DictType(BooleanType, deserialize_from="responseParameters", serialize_when_none=False)
    response_models = DictType(StringType, deserialize_from="responseModels", serialize_when_none=False)


class MethodResponses(Model):
    method = ModelType(MethodResponsesInfo, deserialize_from="string", serialize_when_none=False)


class ResourceMethodInfo(Model):
    http_method = StringType(deserialize_from="httpMethod", serialize_when_none=False)
    authorization_type = StringType(deserialize_from="authorizationType", serialize_when_none=False)
    authorizer_id = StringType(deserialize_from="authorizerId", serialize_when_none=False)
    api_key_required = BooleanType(deserialize_from="apiKeyRequired", serialize_when_none=False)
    request_validator_id = StringType(deserialize_from="requestValidatorId", serialize_when_none=False)
    operation_name = StringType(deserialize_from="operationName", serialize_when_none=False)
    request_parameters = DictType(BooleanType, deserialize_from="requestParameters", serialize_when_none=False)
    request_models = DictType(StringType, deserialize_from="requestModels", serialize_when_none=False)
    method_responses = ModelType(MethodResponses, deserialize_from="methodResponses", serialize_when_none=False)
    method_integration = ModelType(MethodIntegration, deserialize_from="methodIntegration", serialize_when_none=False)
    authorization_scopes = ListType(StringType, deserialize_from="authorizationScopes", serialize_when_none=False)


class Resource(Model):
    id = StringType(deserialize_from="id")
    parent_id = StringType(deserialize_from="parentId", serialize_when_none=False)
    path_part = StringType(deserialize_from="pathPart", serialize_when_none=False)
    path = StringType(deserialize_from="path", serialize_when_none=False)
    display_methods = ListType(StringType(), default=[])
    resource_methods = DictType(ModelType(ResourceMethodInfo), deserialize_from="resourceMethods", default={})


class RestAPI(AWSCloudService):
    arn = StringType(default="")
    id = StringType(deserialize_from="id")
    name = StringType(deserialize_from="name")
    protocol = StringType(choices=('REST', 'HTTP', 'WEBSOCKET'))
    endpoint_type = StringType()
    description = StringType(deserialize_from="description", default="")
    created_date = DateTimeType(deserialize_from="createdDate", serialize_when_none=False)
    version = StringType(deserialize_from="version", serialize_when_none=False)
    warnings = ListType(StringType, deserialize_from="warnings", serialize_when_none=False)
    binary_media_types = ListType(StringType, deserialize_from="binaryMediaTypes", serialize_when_none=False)
    minimum_compression_size = IntType(deserialize_from="minimumCompressionSize", serialize_when_none=False)
    api_key_source = StringType(deserialize_from="apiKeySource", choices=("HEADER", "AUTHORIZER"))
    endpoint_configuration = ModelType(EndpointConfiguration, deserialize_from="endpointConfiguration",
                                       serialize_when_none=False)
    policy = StringType(deserialize_from="policy", serialize_when_none=False)
    resources = ListType(ModelType(Resource), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/apigateway/home?region={region_code}#/apis/{self.id}/resources/"
        }

    def set_cloudwatch(self, region_code):
        return {
            "namespace": "AWS/ApiGateway",
            "dimensions": [CloudWatchDimensionModel({'Name': 'ApiName', 'Value': self.name})],
            "region_name": region_code
        }
