from typing import Union

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base
from .utils import get_id_by_name


class AccessOwnerType(Base):
    __tablename__ = "access_owner_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, primary_key=True)


class AccessObjectType(Base):
    __tablename__ = "access_object_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, primary_key=True)


class AccessRule(Base):
    __tablename__ = "access_rule"

    def __init__(
        self,
        access_owner_type: Union[str, int],
        access_owner_id: int,
        access_object_type: Union[str, int],
        access_object_id: int,
        access_type: str,
        session,
    ):
        if isinstance(access_owner_type, str):
            access_owner_type_id = get_id_by_name(
                AccessOwnerType, access_owner_type, session
            )
        else:
            access_owner_type_id = access_owner_id

        if isinstance(access_object_type, str):
            access_object_type_id = get_id_by_name(
                AccessObjectType, access_object_type, session
            )
        else:
            access_object_type_id = access_object_type

        super().__init__(
            access_owner_type_id=access_owner_type_id,
            access_owner_id=access_owner_id,
            access_object_type_id=access_object_type_id,
            access_object_id=access_object_id,
            access_type=access_type,
        )

    id = Column(Integer, primary_key=True, autoincrement=True)
    access_owner_type_id = Column(
        Integer, ForeignKey("access_owner_type.id"), nullable=False
    )
    access_owner_id = Column(Integer, nullable=False)

    access_object_type_id = Column(
        Integer, ForeignKey("access_object_type.id"), nullable=False
    )
    access_object_id = Column(Integer, nullable=False)

    access_type = Column(String, nullable=False)
