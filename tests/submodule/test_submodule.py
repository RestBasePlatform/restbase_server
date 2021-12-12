import json
from datetime import datetime

import asynctest
import pytest
import responses
from httpx import AsyncClient
from mocks import submodule_request_mock
from models.sublodules import Submodule
from sqlalchemy.orm import Session


@pytest.mark.asyncio
@pytest.mark.parametrize("full_update", [False, True])
async def test_update_module_list(
    full_update,
    test_client: AsyncClient,
    db_test_session: Session,
    latest_test_module_config: dict,
):
    with asynctest.patch("controller.v1.submodule.send_request") as send_request_mock:
        send_request_mock.side_effect = submodule_request_mock
        response = await test_client.post(
            "/v1/submodule/update_module_list", params={"full_update": full_update}
        )
        assert response.status_code == 200
        row_id = (
            latest_test_module_config["name"] + latest_test_module_config["version"]
        )
        row = db_test_session.query(Submodule).filter_by(id=row_id).first()

        assert row
        assert row.name == latest_test_module_config["name"]
        assert row.version == latest_test_module_config["version"]
        assert row.min_module_version == "0.2"
        assert (
            row.files_url
            == "https://api.github.com/repos/RestBasePlatform/TestModule/tarball/0.4"
        )


@pytest.mark.asyncio
async def test_get_submodule_list(test_client: AsyncClient):
    with asynctest.patch(
        "routes.v1.submodule.get_submodule_list"
    ) as get_submodule_list_mock:
        get_submodule_list_mock.return_value = [
            Submodule(
                id=1,
                name="SomeModule",
                version="1.0",
                functions={},
                min_module_version="0.1",
                release_date=datetime.strptime("2021-01-01", "%Y-%m-%d"),
                files_url="some-url",
                database_type="TestType",
            )
        ]
        module_list = (await test_client.get("/v1/submodule/")).json()
        with open("tests/submodule/static/submodule_list_response.json") as f:
            expected_response = json.load(f)
        assert module_list == expected_response


@pytest.mark.asyncio
@responses.activate
async def test_add_submodule_by_github_url(
    test_client: AsyncClient,
    add_submodule_by_github_url_success_body: str,
    db_test_session: Session,
):
    with open("tests/submodule/static/TestModule-master.zip", "rb") as f:
        responses.add(
            responses.GET,
            "https://github.com/RestBasePlatform/TestModule/archive/refs/heads/master.zip",
            body=f.read(),
            status=200,
            stream=True,
        )

        response = await test_client.put(
            "/v1/submodule/add_submodule_by_github_url",
            data=add_submodule_by_github_url_success_body,
        )
        add_submodule_by_github_url_success_body = json.loads(
            add_submodule_by_github_url_success_body
        )
        assert response.status_code == 200
        row_id = (
            add_submodule_by_github_url_success_body["submodule_name"]
            + add_submodule_by_github_url_success_body["tag"]
        )
        row = db_test_session.query(Submodule).filter_by(id=row_id).first()
        assert row
        assert row.name == add_submodule_by_github_url_success_body["submodule_name"]
        assert row.version == add_submodule_by_github_url_success_body["tag"]
        assert row.files_url == add_submodule_by_github_url_success_body["github_url"]
