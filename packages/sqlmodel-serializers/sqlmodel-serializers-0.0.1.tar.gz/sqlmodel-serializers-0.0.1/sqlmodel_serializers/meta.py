from typing import Any

from sqlmodel.main import SQLModelMetaclass

from sqlmodel_serializers.base import BaseMeta
from sqlmodel_serializers.filters import AllFilterSet 

Attrs = dict[str, Any]

ALL = '__all__'


class SQLModelSerializerMetaclass(SQLModelMetaclass):
    def __new__(cls, name: str,  parents: tuple[type], attrs: dict[str, Any], **kwargs) -> Any:
        meta = attrs.get('Meta')

        if meta and not (meta is BaseMeta):
            filter_set = AllFilterSet(attrs, meta)

            attrs = filter_set.filter()

        new_cls = super().__new__(cls, name, parents, attrs, **kwargs)
        
        return new_cls
