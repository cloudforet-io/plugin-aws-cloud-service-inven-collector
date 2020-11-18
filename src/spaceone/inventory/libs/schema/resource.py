from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType, BooleanType
from .dynamic_layout import BaseLayoutField, QuerySearchTableDynamicLayout
from .dynamic_search import BaseDynamicSearch


class MetaDataViewSubData(Model):
    layouts = ListType(PolyModelType(BaseLayoutField))


class MetaDataViewTable(Model):
    layout = PolyModelType(BaseLayoutField)


class MetaDataView(Model):
    table = PolyModelType(MetaDataViewTable, serialize_when_none=False)
    sub_data = PolyModelType(MetaDataViewSubData, serialize_when_none=False)
    search = ListType(PolyModelType(BaseDynamicSearch), serialize_when_none=False)


class BaseMetaData(Model):
    view = ModelType(MetaDataView)


class BaseResponse(Model):
    state = StringType(default='SUCCESS', choices=('SUCCESS', 'FAILURE', 'TIMEOUT'))
    resource_type = StringType(required=True)
    match_rules = DictType(ListType(StringType), default={})
    resource = PolyModelType(Model, default={})


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class CloudWatchDimensionModel(Model):
    name = StringType(serialized_name='Name')
    value = StringType(serialized_name='Value')


class CloudWatchModel(Model):
    class Option:
        serialize_when_none = False

    namespace = StringType()
    region_name = StringType()
    dimensions = ListType(ModelType(CloudWatchDimensionModel))


class CloudServiceTypeMeta(BaseMetaData):
    @classmethod
    def set_fields(cls, name='', fields=[]):
        _table = MetaDataViewTable({'layout': QuerySearchTableDynamicLayout.set_fields(name, fields)})
        return cls({'view': MetaDataView({'table': _table})})

    @classmethod
    def set_meta(cls, name='', fields=[], search=[]):
        table_meta = MetaDataViewTable({'layout': QuerySearchTableDynamicLayout.set_fields(name, fields)})
        return cls({'view': MetaDataView({'table': table_meta, 'search': search})})


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
    provider = StringType(default="aws")
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    data = PolyModelType(Model, default=lambda: {})
    reference = ModelType(ReferenceModel)
    region_code = StringType(serialize_when_none=False)
    _metadata = PolyModelType(CloudServiceMeta, serialize_when_none=False, serialized_name='metadata')


class RegionResource(Model):
    name = StringType(default="")
    region_code = StringType()
    provider = StringType(default='aws')
    tags = DictType(StringType)


class CloudServiceResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource_type = StringType(default='inventory.CloudService')
    resource = PolyModelType(CloudServiceResource)


class RegionResponse(BaseResponse):
    resource_type = StringType(default='inventory.Region')
    match_rules = DictType(ListType(StringType), default={'1': ['provider', 'region_code']})
    resource = PolyModelType(RegionResource)
