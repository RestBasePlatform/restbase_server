"""Utils to work with directories and archives"""

import datetime
import glob
import hashlib
import os
import shutil
import tarfile

import requests
from loguru import logger


def extract_data_from_tar(tar_path: str, target_dir: str) -> str:
    """
    :param tar_path: Path to tar archive
    :param target_dir: Directory where put extracted files
    :return: Path to extracted files
    """
    tmp_dir = f"/tmp/{hashlib.md5(datetime.datetime.now().strftime('%d-%m-%Y %H-%M').encode()).hexdigest()}"

    tar = tarfile.open(tar_path, "r:gz")
    tar.extractall(path=tmp_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        os.system(f"rm -r {target_dir}")
        os.makedirs(target_dir)

    dst = target_dir

    tmp_path = tmp_dir + "/" + os.listdir(tmp_dir)[0]
    files = glob.iglob(os.path.join(tmp_path, "*"))
    for file in files:
        if os.path.isfile(file):
            shutil.move(file, dst)

    os.system(f"rm -r {tmp_dir}")

    return target_dir


def download_tar(tar_url: str, *, source_path: str = None) -> str:
    """
    Get tar from web and put in in source_path
    :param tar_url: Tar link
    :param source_path: Path to put tat
    :return: Path to tar
    """
    r = requests.get(tar_url, stream=True)
    if not source_path:
        source_path = "/tmp/" + hashlib.md5(tar_url.encode()).hexdigest() + ".tgz"

    if os.path.exists(source_path):
        logger.warning(f"Archive from url: '{tar_url}' already downloaded.")
        return source_path

    with open(source_path, "wb") as f:
        f.write(r.raw.read())

    return source_path
