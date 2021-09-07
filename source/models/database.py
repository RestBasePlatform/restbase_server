from controller.v1.credentials import get_credentials_controller
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String

from . import Base


class DatabaseConnectionData(Base):

    __tablename__ = "database_connection"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username_secret_id = Column(Integer, ForeignKey("secret.id"))
    password_secret_id = Column(Integer, ForeignKey("secret.id"))
    host_secret_id = Column(Integer, ForeignKey("secret.id"))
    port_secret_id = Column(Integer, ForeignKey("secret.id"))
    connection_kwargs = Column(JSON)

    def __init__(
        self, username: str, password: str, host: str, port: str, **con_kwargs
    ):
        cred_controller = get_credentials_controller()
        username_secret_id = cred_controller.put(username)
        password_secret_id = cred_controller.put(password)
        host_secret_id = cred_controller.put(host)
        port_secret_id = cred_controller.put(port)

        super().__init__(
            username_secret_id=username_secret_id,
            password_secret_id=password_secret_id,
            host_secret_id=host_secret_id,
            port_secret_id=port_secret_id,
            connection_kwargs=con_kwargs,
        )

    def get_connection_data(self) -> dict:
        cred_controller = get_credentials_controller()
        return {
            "username": cred_controller.get(self.username_secret_id),
            "password": cred_controller.get(self.password_secret_id),
            "host": cred_controller.get(self.host_secret_id),
            "port": cred_controller.get(self.port_secret_id),
            "connection_kwargs": self.connection_kwargs,
        }

    def delete_credentials(self):
        cred_controller = get_credentials_controller()
        cred_controller.delete(self.host_secret_id)
        cred_controller.delete(self.port_secret_id)
        cred_controller.delete(self.username_secret_id)
        cred_controller.delete(self.port_secret_id)
        cred_controller.delete(self.password_secret_id)


class DatabaseList(Base):

    __tablename__ = "database_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    installation = Column(String, ForeignKey("installation.name"))


class SchemaList(Base):

    __tablename__ = "schema_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    database = Column(Integer, ForeignKey("database_list.id"))


class TableList(Base):

    __tablename__ = "table_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    schema = Column(Integer, ForeignKey("schema_list.id"))


class ColumnList(Base):

    __tablename__ = "column_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    datatype = Column(String)
    table = Column(Integer, ForeignKey("table_list.id"))
