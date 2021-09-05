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
    database_type = Column(String)

    @property
    def submodule_folder(self):
        return self.id.replace(".", "_")

    def get_function_imported_name(self, block: str, essence: str) -> str:
        return f"{self.submodule_folder}_ {block}_{essence}"


class Installation(Base):
    __tablename__ = "installation"

    name = Column(String, nullable=False, primary_key=True)
    installation_date = Column(DateTime, nullable=False)
    submodule_id = Column(Integer, ForeignKey("submodule.id"), nullable=False)
    connection_data_id = Column(
        Integer, ForeignKey("database_connection.id"), nullable=False
    )
