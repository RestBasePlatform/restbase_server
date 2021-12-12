from controller.v1.credentials import get_credentials_controller
from exceptions import CredentialsNotFoundError
from restbase_types.server import ServerConnectionCredentials
from restbase_types.server import ServerConnectionData
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Session

from . import Base


class Servers(Base):
    __tablename__ = "servers"
    name = Column(String, primary_key=True)
    host = Column(String)
    port = Column(Integer)
    credential_id = Column(Integer, ForeignKey("server_credentials.id"))
    connection_kwargs = Column(JSON, nullable=False)
    server_status = Column(String, nullable=False)

    def get_server_connection_data(self, db_session: Session) -> ServerConnectionData:
        server_credentials = (
            db_session.query(ServerCredentials).filter_by(id=self.credential_id).first()
        )
        if not server_credentials:
            raise CredentialsNotFoundError("id", self.credential_id)

        return ServerConnectionData(
            self.host,
            self.port,
            self.connection_kwargs,
            server_credentials.get_server_credentials(),
        )


class ServerCredentials(Base):
    __tablename__ = "server_credentials"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    ssh_key = Column(Integer, ForeignKey("secret.id"), nullable=True)
    password = Column(Integer, ForeignKey("secret.id"), nullable=True)
    secret_attrs = ["ssh_key", "password"]

    def __init__(self, username: str, ssh_key: str, password: str):
        cred_controller = get_credentials_controller()
        ssh_key = cred_controller.put(ssh_key) if ssh_key else False
        password = cred_controller.put(password)
        super().__init__(username=username, ssh_key=ssh_key, password=password)

    def get_server_credentials(self) -> ServerConnectionCredentials:
        cred_controller = get_credentials_controller()
        ssh_key = cred_controller.get(self.ssh_key) if self.ssh_key else None
        password = cred_controller.get(self.password) if self.password else None
        return ServerConnectionCredentials(self.username, ssh_key, password)

    def set_secret_attr(self, attr_name: str, attr_value: str):
        cred_controller = get_credentials_controller()
        if attr_name not in self.secret_attrs:
            raise ValueError(f"Values {attr_name} must be in {self.secret_attrs}")
        setattr(self, attr_name, cred_controller.put(attr_value))
