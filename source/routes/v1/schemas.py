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
