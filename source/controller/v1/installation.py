import datetime
import os
from typing import List
from typing import Tuple

from controller.v1.pathdir import download_tar
from controller.v1.pathdir import extract_data_from_tar
from controller.v1.submodule import execute_submodule_function
from exceptions import InstallationNotFound
from jinja2 import Template
from models import Installation
from models import Submodule
from models import DatabaseConnectionData


def create_installation(
    installation_name: str,
    submodule_name: str,
    version: str,
    db_session,
    **db_con_data,
):
    """Creates a new installation from scanned submodule"""

    if installation_name in list_installations_names(db_session):
        raise Exception(f"Installation with name {installation_name} already exists.")

    p_key = submodule_name + version

    submodule_data = db_session.query(Submodule).filter_by(id=p_key).first()

    if not submodule_data:
        pass

    if p_key.replace(".", "_") not in os.listdir("./modules/"):
        tar_path = download_tar(submodule_data.files_url)
        extract_data_from_tar(tar_path, f"./modules/{submodule_data.submodule_folder}")

    append_imports(
        functions=submodule_data.functions,
        module_folder=submodule_data.submodule_folder,
    )

    is_healthy = execute_submodule_function(
        p_key,
        block="common",
        essence="health_check",
        db_session=db_session,
        **db_con_data,
    )

    if not is_healthy:
        raise ConnectionError(f"Database with params: {db_con_data} is not reachable from platform.")

    new_row = Installation(
        name=installation_name,
        installation_date=datetime.datetime.now(),
        submodule_id=submodule_data.id,
    )
    db_session.add(new_row)
    db_session.commit()
    return installation_name


def list_installations(db_session) -> List[Installation]:
    return [i for i in db_session.query(Installation)]


def list_installations_names(db_session) -> List[str]:
    return [i.name for i in list_installations(db_session)]


def append_imports(
    import_template_path: str = "templates/import_block.j2", **template_kwargs
):
    """
    Append new import to __init__ file in modules directory
    :param import_template_path: jinja template for import
    :param template_kwargs: kwargs for template render
    """
    # If module already added - just return
    with open("modules/__init__.py") as f:
        if template_kwargs.get("module_folder") in f.read():
            return

    with open(import_template_path) as f:
        template = Template(f.read())

    module_block = "\n" + template.render(**template_kwargs) + "\n"

    with open("modules/__init__.py", "a") as f:
        f.write(module_block)


def delete_installation(installation_name: str, db_session):

    if installation_name not in list_installations_names(db_session):
        raise InstallationNotFound(installation_name)

    db_session.query(Installation).filter_by(name=installation_name).delete()
    db_session.commit()

    return installation_name


def get_installation(
    installation_name: str, db_session
) -> Tuple[Installation, Submodule]:
    if installation_name not in list_installations_names(db_session):
        raise InstallationNotFound(installation_name)

    installation = (
        db_session.query(Installation).filter_by(name=installation_name).first()
    )
    submodule = (
        db_session.query(Submodule).filter_by(id=installation.submodule_id).first()
    )

    return installation, submodule
