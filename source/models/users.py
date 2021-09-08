from controller.v1.credentials import get_credentials_controller
from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username_secret_id = Column(Integer, ForeignKey("secret.id"))
    password_secret_id = Column(Integer, ForeignKey("secret.id"))
    comment = Column(String, nullable=True)

    def __init__(
        self,
        username: str,
        password: str,
        comment: str,
    ):
        cred_controller = get_credentials_controller()
        username_secret_id = cred_controller.put(username)
        password_secret_id = cred_controller.put(password)

        super().__init__(
            username_secret_id=username_secret_id,
            password_secret_id=password_secret_id,
            comment=comment,
        )


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_list = Column(String, nullable=False)
    comment = Column(String, nullable=True)
