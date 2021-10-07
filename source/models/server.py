from controller.v1.credentials import get_credentials_controller
from restbase_types.server import ServerConnectionCredentials
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base


class Servers(Base):
    __tablename__ = "servers"
    name = Column(String, primary_key=True)
    ip = Column(String)
    credential_id = Column(Integer, ForeignKey("server_credentials.id"))


class ServerCredentials(Base):
    __tablename__ = "server_credentials"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    ssh_key = Column(Integer, ForeignKey("secret.id"), nullable=True)
    password = Column(Integer, ForeignKey("secret.id"), nullable=True)

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
