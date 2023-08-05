from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, Union, Type, Iterable

from sqlmodel import SQLModel

from sqlmodel_serializers.types import Attrs, Fields
from sqlmodel_serializers.base import BaseMeta


@dataclass
class MetaFilter:
    attrs: Attrs
    meta: BaseMeta

    def _is_field(self, model: SQLModel, key: str) -> bool:
        fields = model.__fields__

        return key in fields

    def _get_model_field(self, model: SQLModel, key: str) -> Any:
        fields = model.__fields__

        return fields[key]

    def filter(self) -> Attrs:
        return self.attrs


class FieldsFilter(MetaFilter):
    def __get_fields(self):
        fields = getattr(self.meta, 'fields', None)

        return fields

    def filter(self) -> Attrs:
        attrs = super().filter().copy()

        fields = self.__get_fields()

        if fields is None:
            return attrs

        fields = frozenset(fields)

        annots = attrs.get('__annotations__', dict()).copy()

        keys = tuple(annots.keys())

        for key in keys:
            if key not in fields and key in annots:
                del annots[key]

                if key in attrs:
                    del attrs[key]

        attrs['__annotations__'] = annots

        return attrs


class OmitFilter(MetaFilter):
    def __get_omit(self):
        omit = getattr(self.meta, 'omit', None)

        return omit or []


    def filter(self) -> Attrs:
        attrs = super().filter().copy()

        omit = self.__get_omit()

        annots = attrs.get('__annotations__', dict()).copy()

        for field in omit:
            if field in annots:
                del annots[field]

                if field in attrs:
                    del attrs[field]

        attrs['__annotations__'] = annots

        return attrs


class MergeFilter(MetaFilter):
    def filter(self) -> Attrs:
        attrs = super().filter().copy()

        model = self.meta.model

        cls_annots = attrs.get('__annotations__', dict()).copy()

        annots = getattr(model, '__annotations__', dict())

        items = tuple(annots.items())

        for key, value in items:
            if key in cls_annots or not self._is_field(model, key):
                continue

            cls_annots[key] = value

            attrs[key] = self._get_model_field(model, key).field_info

        if len(cls_annots):
            attrs['__annotations__'] = cls_annots

        return attrs


class OptionalFilter(MetaFilter):
    ALL = '__all__'

    def __get_optional(self) -> Union[Fields, str]:
        optional = getattr(self.meta, 'optional', None)

        return optional or []

    def filter(self) -> Attrs:
        attrs = super().filter().copy()

        meta = self.meta

        optional = self.__get_optional()

        model = meta.model

        annots = attrs.get('__annotations__', dict()).copy()
    
        for key, value in annots.items():
            is_fields = self._is_field(model, key)

            is_optional = optional == self.ALL or key in optional

            if is_fields and is_optional:
                annots[key] = value | None

        attrs['__annotations__'] = annots

        return attrs


class AbstractMetaFilterSet(ABC):
    attrs: Attrs
    meta: BaseMeta
    filters: Iterable[Type[MetaFilter]]

    @abstractmethod
    def filter(self) -> Attrs:
        pass


@dataclass
class MetaFilterSet(AbstractMetaFilterSet):
    attrs: Attrs
    meta: BaseMeta

    def filter(self) -> Attrs:
        attrs = self.attrs

        for cls in self.filters:
            attrs = cls(attrs, self.meta).filter()

        return attrs


class AllFilterSet(MetaFilterSet):
    filters = (MergeFilter, FieldsFilter, OmitFilter, OptionalFilter)
