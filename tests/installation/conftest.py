import json

import asynctest
import pytest
from httpx import AsyncClient
from mocks import submodule_request_mock


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
        "tests/installation/static/responses/create_installation_name_already_exists.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def get_installation_no_credentials_response():
    with open(
        "tests/installation/static/responses/get_installation_no_credentials.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def get_installation_with_credentials_response():
    with open(
        "tests/installation/static/responses/get_installation_with_credentials.json"
    ) as f:
        return json.load(f)


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


@pytest.fixture(scope="function")
async def client_with_test_installation(
    client_with_submodules: AsyncClient, create_installation_success_body: dict
) -> AsyncClient:
    await client_with_submodules.post(
        "/v1/installation/", data=create_installation_success_body
    )

    try:
        yield client_with_submodules
    except Exception as e:
        print(e)
    finally:
        await client_with_submodules.aclose()
