import datetime
import os
from typing import List
from typing import Optional
from typing import Tuple

from controller.v1.database import refresh_database_data
from controller.v1.pathdir import download_tar
from controller.v1.pathdir import extract_data_from_tar
from exceptions import InstallationNotFound
from jinja2 import Template
from models import DatabaseConnectionData
from models import Installation
from models import Submodule
from sqlalchemy.orm import Session


MODULES_PATH = "modules" if not os.getenv("TEST") else "./source/modules"


async def create_installation(
    installation_name: str,
    submodule_name: str,
    version: str,
    db_session: Session,
    **db_con_data,
) -> Installation:
    """
    Create installation from module.

    Parameters
    ----------
    installation_name : str
        Name of installation to create
    submodule_name : str
        Name of submodule to work with
    version : str
        Version of submodule
    db_session : Session
        Session of SQL Alchemy

    Raises
    ------
    ConnectionError
        When database server is unreachable.
    """

    if installation_name in list_installations_names(db_session):
        raise Exception(f"Installation with name {installation_name} already exists.")

    p_key = submodule_name + version

    submodule_data = db_session.query(Submodule).filter_by(id=p_key).first()

    if not submodule_data:
        pass

    if p_key.replace(".", "_") not in os.listdir(MODULES_PATH):
        tar_path = download_tar(submodule_data.files_url)
        extract_data_from_tar(
            tar_path, f"{MODULES_PATH}/{submodule_data.submodule_folder}"
        )

    await append_imports(
        functions=submodule_data.functions,
        module_folder=submodule_data.submodule_folder,
    )

    is_healthy = True

    if not is_healthy:
        raise ConnectionError(
            f"Database with params: {db_con_data} is not reachable from platform."
        )

    db_con_row = DatabaseConnectionData(**db_con_data)
    db_session.add(db_con_row)
    db_session.commit()
    new_row = Installation(
        name=installation_name,
        installation_date=datetime.datetime.now(),
        submodule_id=submodule_data.id,
        connection_data_id=db_con_row.id,
    )
    db_session.add(new_row)
    db_session.commit()
    # try:
    await refresh_database_data(new_row, db_session)
    # except BaseException as e:
    #     print(e)
    #     db_session.delete(new_row)
    #     db_session.commit()

    return new_row


def list_installations(db_session) -> List[Installation]:
    return [i for i in db_session.query(Installation)]


def list_installations_names(db_session) -> List[str]:
    return [i.name for i in list_installations(db_session)]


async def append_imports(
    import_template_path: str = "templates/import_block.j2", **template_kwargs
):
    """Append new imports to __init__ file in modules.

    Parameters
    ----------
    import_template_path : str, optional
        Path to template with import block, by default "templates/import_block.j2"
    """
    with open(MODULES_PATH + "/__init__.py") as f:
        if template_kwargs.get("module_folder") in f.read():
            return

    with open(import_template_path) as f:
        template = Template(f.read())

    module_block = "\n" + template.render(**template_kwargs) + "\n"

    with open(MODULES_PATH + "/__init__.py", "a") as f:
        f.write(module_block)


def delete_installation(installation_name: str, db_session: Session):
    """Delete installation and all relative data

    Parameters
    ----------
    installation_name : str
        Installation name
    db_session : Session
        SQL Alchemy Sessin

    Raises
    ------
    InstallationNotFound
        When installation not found.
    """

    if installation_name not in list_installations_names(db_session):
        raise InstallationNotFound(installation_name)

    installation = (
        db_session.query(Installation).filter_by(name=installation_name).first()
    )
    db_connection_data = (
        db_session.query(DatabaseConnectionData)
        .filter_by(id=installation.connection_data_id)
        .first()
    )
    db_connection_data.delete_credentials()
    db_session.delete(db_connection_data)
    db_session.delete(installation)

    db_session.commit()

    return installation_name


async def get_installation(
    installation_name: str, with_credentials: bool, db_session
) -> Tuple[Installation, Submodule, Optional[DatabaseConnectionData]]:
    """Get the installation object data. Include:
        - submodule data
        - database connection credentials

    Args:
        installation_name (str): Installation name from databas
        with_credentials (bool): Include credentials
        db_session ([type]): Session for local database

    Raises:
        InstallationNotFound: If module not found

    Returns:
        Tuple[Installation, Submodule, Optional[DatabaseConnectionData]]: Database data as SQL ORM objects
    """
    if installation_name not in list_installations_names(db_session):
        raise InstallationNotFound(installation_name)

    installation = (
        db_session.query(Installation).filter_by(name=installation_name).first()
    )

    db_credentials = None
    if with_credentials:
        db_credentials = (
            db_session.query(DatabaseConnectionData)
            .filter_by(id=installation.connection_data_id)
            .first()
        )

    submodule = (
        db_session.query(Submodule).filter_by(id=installation.submodule_id).first()
    )

    return installation, submodule, db_credentials
