import datetime
import glob
import json
import os
import shutil
import tarfile
from typing import List

import git
import requests
import yaml
from models import Submodule
from controller.v1.pathdir import extract_data_from_tar


def get_link_for_raw_file(link: str) -> str:
    link = link.replace("/blob", "")
    return link.replace("github", "raw.githubusercontent")


def get_module_config_from_github(
    repo_link: str, version: str = "stable", version_file="restabse_cfg.yaml"
) -> dict:

    version_branch_converter = {"stable": "master"}

    file_link = (
        repo_link.replace("/blob", "").replace("github", "raw.githubusercontent")
        + "/"
        + version_branch_converter.get(version, "master")
        + "/"
        + version_file
    )
    r = requests.get(file_link)
    return yaml.load(r.text)


def list_modules(org_name="RestBaseApi") -> List[dict]:
    answer = json.loads(
        requests.get(f"https://api.github.com/orgs/{org_name}/repos").text
    )
    module_names = [i["name"] for i in answer if i["name"].endswith("Module")]

    available_modules = []

    for module_name in module_names[:1]:
        releases_answer = json.loads(
            requests.get(
                f"https://api.github.com/repos/RestBaseApi/{module_name}/releases"
            ).text
        )

        for release in releases_answer:

            config = get_config_from_tar(tar_url=release["tarball_url"])

            available_modules.append(
                {
                    "module_name": module_name,
                    "version": release["tag_name"],
                    "release_date": release["published_at"],
                    "config": config
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
        config = yaml.load(f)

    os.system(f"rm -r /tmp/tar_tmp")
    return config
