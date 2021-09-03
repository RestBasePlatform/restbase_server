import json
import os

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import Submodule


def test_install_from_github(test_client: TestClient, db_test_session: Session, latest_test_module_config: dict):
    test_client.get("/v1/submodule/update_module_list")

    row_id = latest_test_module_config["name"] + latest_test_module_config["version"]
    row = db_test_session.query(Submodule).filter_by(id=row_id).first()

    assert row
    assert row.name == "TestModule"
    assert row.version == "1.5"
    assert row.min_module_version == "0.2"
    assert row.files_url == "https://api.github.com/repos/RestBaseApi/TestModule/tarball/1.5"
