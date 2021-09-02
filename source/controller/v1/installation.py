import datetime
import os
from typing import List

from controller.v1.pathdir import download_tar
from controller.v1.pathdir import extract_data_from_tar
from jinja2 import Template
from models import Installation
from models import Submodule


def create_installation(
    installation_name: str, submodule_name: str, version: str, db_session
):
    """Creates a new installation from scanned submodule"""

    if installation_name in list_installations_names(db_session):
        raise Exception(f"Installation with name {installation_name} already exists.")

    p_key = submodule_name + version

    submodule_data = db_session.query(Submodule).filter_by(id=p_key).first()

    if not submodule_data:
        pass

    p_key = p_key.replace(".", "_")
    if p_key.replace(".", "_") not in os.listdir("./modules/"):
        tar_path = download_tar(submodule_data.files_url)
        extract_data_from_tar(tar_path, f"./modules/{p_key}")

    append_imports(functions=submodule_data.functions, module_folder=p_key)

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
