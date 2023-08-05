from sqlmodel import SQLModel

from sqlmodel_serializers.meta import SQLModelSerializerMetaclass
from sqlmodel_serializers.base import BaseMeta


class SQLModelSerializer(SQLModel, metaclass=SQLModelSerializerMetaclass):
    Meta = BaseMeta
