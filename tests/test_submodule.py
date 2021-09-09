import pytest
from fastapi.testclient import TestClient
from models import Submodule
from sqlalchemy.orm import Session


@pytest.mark.parametrize("full_update", [False, True])
def test_update_module_list(
    full_update,
    test_client: TestClient,
    db_test_session: Session,
    latest_test_module_config: dict,
):
    test_client.get(
        "/v1/submodule/update_module_list", params={"full_update": full_update}
    )

    row_id = latest_test_module_config["name"] + latest_test_module_config["version"]
    row = db_test_session.query(Submodule).filter_by(id=row_id).first()

    assert row
    assert row.name == latest_test_module_config["name"]
    assert row.version == latest_test_module_config["version"]
    assert row.min_module_version == "0.2"
    assert (
        row.files_url
        == "https://api.github.com/repos/RestBaseApi/TestModule/tarball/1.5"
    )


#
# def test_get_submodule_list(test_client: TestClient, latest_test_module_config: dict):
#     test_client.get("/v1/submodule/update_module_list", params={"full_update": True})
#     module_list = test_client.get("/v1/submodule/list").json()
#     print(module_list)
#     assert 0
