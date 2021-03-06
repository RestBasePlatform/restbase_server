from controller.v1.credentials import get_credentials_controller
from restbase_types import UserData
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from . import Base


class User(Base):
    __tablename__ = "user"

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

    def get_user_data(self) -> UserData:
        """Get and decrypt user data.

        Returns
        -------
        [UserData]
            Userdata with decrypted username and password.
        """
        cred_controller = get_credentials_controller()
        username = cred_controller.get(self.username_secret_id)
        password = cred_controller.get(self.password_secret_id)

        return UserData(username=username, password=password)

    def set_secret(self, secret_name: str, secret_data: str):
        """Change username or password.

        Parameters
        ----------
        secret_name : str
            'username' or 'password'
        secret_data : str
            New value of secret_name
        """
        cred_controller = get_credentials_controller()
        setattr(self, secret_name + "_secret_id", cred_controller.put(secret_data))


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_list = Column(String, nullable=False)
    comment = Column(String, nullable=True)
