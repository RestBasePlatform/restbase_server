import json

import asynctest
import pytest
from httpx import AsyncClient
from mocks import submodule_request_mock


@pytest.fixture(scope="function")
async def client_with_submodules(test_client: AsyncClient) -> AsyncClient:
    with asynctest.patch("controller.v1.submodule.send_request") as send_request_mock:
        send_request_mock.side_effect = submodule_request_mock
        await test_client.post(
            "/v1/submodule/update_module_list", params={"full_update": True}
        )

    try:
        yield test_client
    except Exception as e:
        print(e)
    finally:
        await test_client.aclose()


@pytest.fixture()
def create_installation_success_body():
    with open(
        "tests/installation/static/requests/create_installation_success.json"
    ) as f:
        return f.read()


@pytest.fixture()
def create_installation_success_response():
    with open(
        "tests/installation/static/responses/create_installation_success.json"
    ) as f:
        return json.load(f)


@pytest.fixture()
def create_installation_name_already_exists_response():
    with open(
        "tests/installation/static/responses/test_create_installation_name_already_exists.json"
    ) as f:
        return json.load(f)
