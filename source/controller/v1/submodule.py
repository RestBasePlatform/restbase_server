import datetime
import os
from typing import List

import requests
import yaml
from controller.v1.pathdir import extract_data_from_tar
from controller.v1.rb_requests import send_request
from exceptions import SubmoduleNotFound
from models import Submodule


async def update_module_list(db_session, *, full_update: bool = False, org_name="RestBaseApi") -> List[dict]:
    """
    Refresh submodules list from github org
    :param db_session: Database Session
    :param full_update: Delete old data than update
    :param org_name: GitHub org name with modules
    :return:
    """
    answer = await send_request(f"https://api.github.com/orgs/{org_name}/repos", "get")

    module_names = [i["name"] for i in answer if i["name"].endswith("Module")]

    available_modules = []

    if full_update:
        db_session.query(Submodule).delete()
        db_session.commit()

    for module_name in module_names:
        releases_answer = await send_request(f"https://api.github.com/repos/RestBaseApi/{module_name}/releases", "get")

        for release in releases_answer:

            config = get_config_from_tar(tar_url=release["tarball_url"])

            row = (
                db_session.query(Submodule)
                .filter_by(id=module_name + release["tag_name"])
                .first()
            )
            if not row:
                db_session.add(
                    Submodule(
                        id=module_name + release["tag_name"],
                        name=module_name,
                        version=release["tag_name"],
                        functions=await parse_functions_from_config(
                            config.get("functions", {})
                        ),
                        min_module_version=config.get("min_version", "NOT_SET"),
                        release_date=datetime.datetime.strptime(
                            release["published_at"], "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        files_url=release["tarball_url"],
                    )
                )
            db_session.commit()

            available_modules.append(
                {
                    "module_name": module_name,
                    "version": release["tag_name"],
                    "release_date": release["published_at"],
                    "config": config,
                }
            )
    return available_modules


def get_config_from_tar(*, tar_path: str = None, tar_url: str = None) -> dict:

    archive_path = "/tmp/archive.tgz"
    if tar_url:
        r = requests.get(tar_url, stream=True)

        with open(archive_path, "wb") as f:
            f.write(r.raw.read())

        tar_path = archive_path

    extract_data_from_tar(tar_path, "/tmp/tar_tmp")

    with open("/tmp/tar_tmp/restabse_cfg.yaml") as f:
        config = yaml.load(f, Loader=yaml.Loader)

    os.system(f"rm -r /tmp/tar_tmp")
    return config


async def parse_functions_from_config(config_functions_block: dict) -> List[dict]:
    functions_config = []
    for module in config_functions_block:
        for function in config_functions_block.get(module, []):
            functions_config.append({**function, **{"block_name": module}})

    return functions_config


async def get_submodule_data(submodule_name: str, version: str, db_session) -> Submodule:
    submodule = db_session.query(Submodule).filter_by(id=submodule_name+version).first()
    if not submodule:
        raise SubmoduleNotFound(submodule_name+version)

    return submodule
