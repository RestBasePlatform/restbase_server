from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base


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
