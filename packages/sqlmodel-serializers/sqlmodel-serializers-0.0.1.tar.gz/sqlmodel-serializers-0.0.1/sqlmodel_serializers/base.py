from typing import Optional, Union

from sqlmodel import SQLModel

from sqlmodel_serializers.types import Fields


class BaseMeta:
    fields: Optional[Fields] = None

    omit: Optional[Fields] = None

    model: SQLModel

    optional: Union[Fields, str, None] = None

