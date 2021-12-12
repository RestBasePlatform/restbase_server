import pytest
from httpx import AsyncClient
from utils import load_static_json


@pytest.fixture(scope="session")
def create_credentials_success_body() -> str:
    return load_static_json(
        "tests/server/static/requests/create_server_credentials.json",
        convert_to_dict=False,
    )


@pytest.fixture(scope="session")
def create_credentials_success_response() -> dict:
    return load_static_json(
        "tests/server/static/responses/create_server_credentials.json"
    )


@pytest.fixture(scope="session")
def patch_credentials_success_body() -> str:
    return load_static_json(
        "tests/server/static/requests/patch_server_credentials.json",
        convert_to_dict=False,
    )


@pytest.fixture(scope="session")
def patch_credentials_success_response() -> dict:
    return load_static_json(
        "tests/server/static/responses/patch_server_credentials.json"
    )


@pytest.fixture(scope="session")
def get_credentials_success_response() -> dict:
    return load_static_json("tests/server/static/responses/get_server_credentials.json")


@pytest.fixture(scope="function")
async def client_with_server_credentials(
    test_client: AsyncClient,
    create_credentials_success_body: str,
):
    await test_client.post(
        "/v1/server/credentials/", data=create_credentials_success_body
    )

    try:
        yield test_client
    except Exception as e:
        print(e)
    finally:
        await test_client.aclose()
