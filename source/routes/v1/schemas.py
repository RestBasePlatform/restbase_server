from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class AddCustomSubmoduleSchema(BaseModel):
    submodule_name: str = Field(description="Submodule name")
    tag: str = Field(description="Unique version of submodule name")
    github_url: str = Field(description="Url for github zip archive")


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


class EditUserSchema(BaseModel):
    username: str = Field(description="Database username(platform)")
    password: str = Field(description="Database password(platform)")
    comment: str = Field(description="User comment(platform)", default="")


class CreateGroupSchema(BaseModel):
    name: str = Field(description="Group name(platform)")
    comment: str = Field(description="User comment(platform)", default="")
    user_list: Optional[List[int]] = Field(
        description="User id's for give access to.", default=[]
    )


class DatabaseAddress(BaseModel):
    database: str = Field(default=None)
    schema_name: str = Field(default=None, alias="schema")
    table: str = Field(default=None)


class GrantAccessSchema(BaseModel):
    granter_type: str = Field(description="User or Group")
    granter_type_name: str = Field(description="Name of granter")
    installation_name: str
    database_address: Optional[DatabaseAddress] = Field(
        description="Full address of access object"
    )
    access_string: str


class ServerCredentialSchema(BaseModel):
    username: str = Field(description="Username")
    ssh_key: Optional[str] = Field(description="Private SSH Key")
    password: Optional[str] = Field(description="Password for key or user")


class CreateServerSchema(BaseModel):
    name: str = Field(description="Server name")
    host: str = Field(description="Server ip address")
    port: int = Field(description="SSH port of server in 'host'", default=22)
    credential_id: int = Field(description="ID from Server Credentials list")
    connection_kwargs: dict = Field(
        description="Additional parameters for server connection", default={}
    )
