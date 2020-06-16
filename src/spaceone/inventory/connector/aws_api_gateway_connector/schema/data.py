import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType, \
    DictType

_LOGGER = logging.getLogger(__name__)

'''
HTTP WEBSOCKET
'''
class CorsConfiguration(Model):
    allow_credentials = BooleanType(deserialize_from="AllowCredentials")
    allow_headers = ListType(StringType, deserialize_from="AllowHeaders")
    allow_methods = ListType(StringType, deserialize_from="AllowMethods")
    allow_origins = ListType(StringType, deserialize_from="AllowOrigins")
    expose_headers = ListType(StringType, deserialize_from="ExposeHeaders")
    max_age = IntType(deserialize_from="MaxAge")


class HTTPWebsocket(Model):
    arn = StringType()
    api_endpoint = StringType(deserialize_from="ApiEndpoint")
    api_id = StringType(deserialize_from="ApiId")
    api_key_selection_expression = StringType(deserialize_from="ApiKeySelectionExpression")
    cors_configuration = ModelType(CorsConfiguration, deserialize_from="CorsConfiguration")
    created_date = DateTimeType(deserialize_from="CreatedDate")
    description = StringType(deserialize_from="Description")
    disable_schema_validation = BooleanType(deserialize_from="DisableSchemaValidation")
    import_info = ListType(StringType,deserialize_from="ImportInfo")
    name = StringType(deserialize_from="Name")
    protocol_type = StringType(deserialize_from="ProtocolType", choices=("WEBSOCKET","HTTP"))
    route_selection_expression = StringType(deserialize_from="RouteSelectionExpression")
    tags = DictType(StringType, deserialize_from="Tags")
    version = StringType(deserialize_from="Version")
    warnings = ListType(StringType, deserialize_from="Warnings")
    region_name = StringType(default='')
    account_id = StringType(default='')

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/apigateway/home?region={self.region_name}#/apis/{self.api_id}/routes"
        }

    @serializable
    def cloudwatch(self):
        return {
            "namespace": "AWS/ApiGateway",
            "dimensions": [
                {
                    "Name": "ApiId",
                    "Value": self.api_id
                }
            ],
        }


'''
REST API
'''
class EndpointConfiguration(Model):
    types = ListType(StringType, deserialize_from="types", choices=("REGIONAL", "EDGE", "PRIVATE"))
    vpc_endpoint_ids = ListType(StringType, deserialize_from="vpcEndpointIds")


class IntegrationResponsesInfo(Model):
    status_code = StringType(deserialize_from="statusCode")
    selection_pattern = StringType(deserialize_from="selectionPattern")
    response_parameters = DictType(StringType, deserialize_from="responseParameters")
    response_templates = DictType(StringType, deserialize_from="responseTemplates")
    content_handling = StringType(deserialize_from="contentHandling", choices=("CONVERT_TO_BINARY", "CONVERT_TO_TEXT"))


class IntegrationResponses(Model):
    method = ModelType(IntegrationResponsesInfo, deserialize_from="string")


class MethodIntegration(Model):
    type = StringType(deserialize_from="type", choices=("HTTP", "AWS", "MOCK", "HTTP_PROXY", "AWS_PROXY"))
    http_method = StringType(deserialize_from="httpMethod")
    uri = StringType(deserialize_from="uri")
    connection_type = StringType(deserialize_from="connectionType", choices=("INTERNET", "VPC_LINK"))
    connection_id = StringType(deserialize_from="connectionId")
    credentials = StringType(deserialize_from="credentials")
    request_parameters = DictType(StringType, deserialize_from="requestParameters")
    request_templates = DictType(StringType, deserialize_from="requestTemplates")
    passthrough_behavior = StringType(deserialize_from="passthroughBehavior")
    content_handling = StringType(deserialize_from="contentHandling", choices=("CONVERT_TO_BINARY", "CONVERT_TO_TEXT"))
    timeout_in_millis = IntType(deserialize_from="timeoutInMillis")
    cache_namespace = StringType(deserialize_from="cacheNamespace")
    cache_key_parameters = ListType(StringType, deserialize_from="cacheKeyParameters")
    integration_responses = ModelType(IntegrationResponses, deserialize_from="integrationResponses")


class MethodResponsesInfo(Model):
    status_code = StringType(deserialize_from="statusCode")
    response_parameters = DictType(BooleanType, deserialize_from="responseParameters")
    response_models = DictType(StringType, deserialize_from="responseModels")


class MethodResponses(Model):
    method = ModelType(MethodResponsesInfo, deserialize_from="string")


class ResourceMethodInfo(Model):
    http_method = StringType(deserialize_from="httpMethod")
    authorization_type = StringType(deserialize_from="authorizationType")
    authorizer_id = StringType(deserialize_from="authorizerId")
    api_key_required = BooleanType(deserialize_from="apiKeyRequired")
    request_validator_id = StringType(deserialize_from="requestValidatorId")
    operation_name = StringType(deserialize_from="operationName")
    request_parameters = DictType(BooleanType, deserialize_from="requestParameters")
    request_models = DictType(StringType, deserialize_from="requestModels")
    method_responses = ModelType(MethodResponses, deserialize_from="methodResponses")
    method_integration = ModelType(MethodIntegration, deserialize_from="methodIntegration")
    authorization_scopes = ListType(StringType, deserialize_from="authorizationScopes")


class Resource(Model):
    id = StringType(deserialize_from="id")
    parent_id = StringType(deserialize_from="parentId")
    path_part = StringType(deserialize_from="pathPart")
    path = StringType(deserialize_from="path")
    display_methods = ListType(StringType())
    resource_methods = DictType(ModelType(ResourceMethodInfo), deserialize_from="resourceMethods", default={})


class RestAPI(Model):
    arn = StringType(default="")
    id = StringType(deserialize_from="id")
    name = StringType(deserialize_from="name")
    description = StringType(deserialize_from="description")
    created_date = DateTimeType(deserialize_from="createdDate")
    version = StringType(deserialize_from="version")
    warnings = ListType(StringType, deserialize_from="warnings")
    binary_media_types = ListType(StringType, deserialize_from="binaryMediaTypes")
    minimum_compression_size = IntType(deserialize_from="minimumCompressionSize")
    api_key_source = StringType(deserialize_from="apiKeySource", choices=("HEADER", "AUTHORIZER"))
    endpoint_configuration = ModelType(EndpointConfiguration, deserialize_from="endpointConfiguration")
    policy = StringType(deserialize_from="policy")
    tags = DictType(StringType, deserialize_from="tags")
    resources = ListType(ModelType(Resource), default=[])
    region_name = StringType(default='')
    account_id = StringType(default='')

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/apigateway/home?region={self.region_name}#/apis/{self.id}/resources/"
        }

    @serializable
    def cloudwatch(self):
        return {
            "namespace": "AWS/ApiGateway",
            "dimensions": [
                {
                    "Name": "ApiName",
                    "Value": self.name
                }
            ],
        }
