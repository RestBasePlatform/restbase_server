from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base


class Secret(Base):
    __tablename__ = "secret"

    id = Column(Integer, primary_key=True, autoincrement=True)
    secret = Column(String, nullable=False)
