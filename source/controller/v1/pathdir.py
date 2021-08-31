import glob
import os
import tarfile
import shutil
import datetime
import hashlib


def extract_data_from_tar(tar_path: str, source_dir: str) -> str:
    tmp_dir = f"/tmp/{hashlib.md5(datetime.datetime.now().strftime('%d-%m-%Y %H-%M').encode()).hexdigest()}"

    tar = tarfile.open(tar_path, "r:gz")
    tar.extractall(path=tmp_dir)

    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    else:
        os.system(f"rm -r {source_dir}")
        os.makedirs(source_dir)

    dst = source_dir

    tmp_path = tmp_dir + "/" + os.listdir(tmp_dir)[0]
    files = glob.iglob(os.path.join(tmp_path, "*"))
    for file in files:
        if os.path.isfile(file):
            shutil.move(file, dst)

    os.system(f"rm -r {tmp_dir}")

    return source_dir
