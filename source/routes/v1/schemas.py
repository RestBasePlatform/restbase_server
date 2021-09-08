from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class CreateInstallationModel(BaseModel):
    installation_name: str = Field(description="Installation name")
    submodule_name: str = Field(description="Submodule name")
    submodule_version: str = Field(description="Submodule version")

    username: str = Field(description="Database server username")
    password: str = Field(description="Database server password")
    host: str = Field(description="Database server host")
    port: str = Field(description="Database server port", default=None)

    def get_db_con_data(self) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
        }


class CreateUserSchema(BaseModel):
    username: str = Field(description="Database username(platform)")
    password: str = Field(description="Database password(platform)")
    comment: str = Field(description="User comment(platform)", default="")
    group_list: Optional[List[str]] = Field(
        description="Group names for give access to.", default=[]
    )


class CreateGroupSchema(BaseModel):
    name: str = Field(description="Group name(platform)")
    comment: str = Field(description="User comment(platform)", default="")
    user_list: Optional[List[int]] = Field(
        description="User id's for give access to.", default=[]
    )
