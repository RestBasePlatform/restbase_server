from models import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String


class Submodule(Base):
    __tablename__ = "submodule"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    functions = Column(JSON, nullable=False)
    min_module_version = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    files_url = Column(String, nullable=False)


class Installation(Base):
    __tablename__ = "installation"

    name = Column(String, nullable=False, primary_key=True)
    installation_date = Column(DateTime, nullable=False)
    submodule_id = Column(Integer, ForeignKey("submodule.id"), nullable=False)
