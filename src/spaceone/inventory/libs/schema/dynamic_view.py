from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, ModelType

from .dynamic_layout import BaseLayoutField, ItemLayoutOption, TableLayoutOption, QuerySearchTableLayoutOption, \
    SimpleTableLayoutOption, ListLayoutOption, RawLayoutOption
from .dynamic_field import BaseDynamicField




# class BaseDynamicView(Model):
#     name = StringType()
#     view_type = StringType()
#     key_path = StringType(serialize_when_none=False)
#     data_source = ListType(PolyModelType(BaseDynamicField))
#
#
# class ItemDynamicView(BaseDynamicView):
#     view_type = StringType(default='item')
#
#
# class TableDynamicView(BaseDynamicView):
#     view_type = StringType(default='table')
#     key_path = StringType(required=True)
#
#
# class SimpleTableDynamicView(BaseDynamicView):
#     view_type = StringType(default='simple-table')
#     key_path = StringType(required=True)
