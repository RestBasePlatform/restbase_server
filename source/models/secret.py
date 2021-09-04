from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from . import Base


class Secret(Base):
    __tablename__ = "secret"

    id = Column(Integer, primary_key=True, autoincrement=True)
    secret = Column(String, nullable=False)


class DatabaseConnectionData(Base):

    __tablename__ = "database_connection"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username_secret_id = Column(Integer, ForeignKey("secret.id"))
    password_secret_id = Column(Integer, ForeignKey("secret.id"))
    ip_secret_id = Column(Integer, ForeignKey("secret.id"))
    port_secret_id = Column(Integer, ForeignKey("secret.id"))
