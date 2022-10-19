from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, BooleanType, FloatType
from .dynamic_layout import BaseLayoutField, QuerySearchTableDynamicLayout
from .dynamic_search import BaseDynamicSearch
from .dynamic_widget import BaseDynamicWidget


class MetaDataViewSubData(Model):
    layouts = ListType(PolyModelType(BaseLayoutField))


class MetaDataViewTable(Model):
    layout = PolyModelType(BaseLayoutField)


class MetaDataView(Model):
    table = PolyModelType(MetaDataViewTable, serialize_when_none=False)
    sub_data = PolyModelType(MetaDataViewSubData, serialize_when_none=False)
    search = ListType(PolyModelType(BaseDynamicSearch), serialize_when_none=False)
    widget = ListType(PolyModelType(BaseDynamicWidget), serialize_when_none=False)


class BaseMetaData(Model):
    view = ModelType(MetaDataView)


class BaseResponse(Model):
    state = StringType(default='SUCCESS', choices=('SUCCESS', 'FAILURE', 'TIMEOUT'))
    message = StringType(default='')
    resource_type = StringType(required=True)
    match_rules = DictType(ListType(StringType), serialize_when_none=False)
    resource = PolyModelType(Model, default={})
    
    
class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class CloudWatchDimension(Model):
    Name = StringType(serialize_when_none=False)
    Value = StringType(serialize_when_none=False)


class CloudWatchMetricInfo(Model):
    Namespace = StringType(serialize_when_none=False)
    Dimensions = ListType(ModelType(CloudWatchDimension), serialize_when_none=False)


class CloudWatchModel(Model):
    region_name = StringType(default='us-east-1')
    metrics_info = ListType(ModelType(CloudWatchMetricInfo), default=[])


class CloudTrailLookupResource(Model):
    AttributeKey = StringType(default='ResourceName')
    AttributeValue = StringType(default='')


class CloudTrailModel(Model):
    region_name = StringType(serialize_when_none=False)
    resource_type = StringType(serialize_when_none=False)
    LookupAttributes = ListType(ModelType(CloudTrailLookupResource), default=[])


class CloudServiceTypeMeta(BaseMetaData):
    @classmethod
    def set_meta(cls, name='', fields=[], search=[], widget=[]):
        table_meta = MetaDataViewTable({'layout': QuerySearchTableDynamicLayout.set_fields(name, fields)})
        return cls({'view': MetaDataView({'table': table_meta, 'search': search, 'widget': widget})})


class CloudServiceMeta(BaseMetaData):
    @classmethod
    def set(cls):
        sub_data = MetaDataViewSubData()
        return cls({'view': MetaDataView({'sub_data': sub_data})})

    @classmethod
    def set_layouts(cls, layouts=[]):
        sub_data = MetaDataViewSubData({'layouts': layouts})
        return cls({'view': MetaDataView({'sub_data': sub_data})})


class CloudServiceTypeResource(Model):
    name = StringType()
    provider = StringType()
    group = StringType()
    _metadata = PolyModelType(CloudServiceTypeMeta, serialize_when_none=False, serialized_name='metadata')
    labels = ListType(StringType(), serialize_when_none=False)
    tags = DictType(StringType, serialize_when_none=False)
    is_primary = BooleanType(default=False)
    is_major = BooleanType(default=False)
    resource_type = StringType(default='inventory.CloudService')
    service_code = StringType(serialize_when_none=False)


class CloudServiceTypeResponse(BaseResponse):
    resource_type = StringType(default='inventory.CloudServiceType')
    match_rules = DictType(ListType(StringType), default={'1': ['name', 'group', 'provider']})
    resource = PolyModelType(CloudServiceTypeResource)


class CloudServiceResource(Model):
    name = StringType(default="")
    provider = StringType(default="aws")
    account = StringType()
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = StringType(serialize_when_none=False)
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    data = PolyModelType(Model, default=lambda: {})
    tags = DictType(StringType, default={})
    reference = ModelType(ReferenceModel)
    region_code = StringType(serialize_when_none=False)
    _metadata = PolyModelType(CloudServiceMeta, serialize_when_none=False, serialized_name='metadata')


class AWSCloudService(Model):
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)
    cloudtrail = ModelType(CloudTrailModel, serialize_when_none=False)


class RegionResource(Model):
    name = StringType(default="")
    region_code = StringType()
    provider = StringType(default='aws')
    tags = DictType(StringType)


class CloudServiceResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id', 'provider', 'cloud_service_type', 'cloud_service_group', 'account']
    })
    resource_type = StringType(default='inventory.CloudService')
    resource = PolyModelType(CloudServiceResource)


class RegionResponse(BaseResponse):
    resource_type = StringType(default='inventory.Region')
    match_rules = DictType(ListType(StringType), default={'1': ['provider', 'region_code']})
    resource = PolyModelType(RegionResource)


class ErrorResource(Model):
    resource_type = StringType(default='inventory.CloudService')
    provider = StringType(default='aws')
    cloud_service_group = StringType(serialize_when_none=False)
    cloud_service_type = StringType(serialize_when_none=False)
    resource_id = StringType(serialize_when_none=False)


class ErrorResourceResponse(BaseResponse):
    state = StringType(default='FAILURE')
    resource_type = StringType(default='inventory.ErrorResource')
    resource = ModelType(ErrorResource, default={})
