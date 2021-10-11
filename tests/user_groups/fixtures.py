import json

import pytest
from httpx import AsyncClient


@pytest.fixture()
def create_user_success_body():
    with open("tests/user_groups/static/requests/create_user_body.json") as f:
        return f.read()


@pytest.fixture(scope="session")
def create_user_success_response_response():
    with open(
        "tests/user_groups/static/responses/create_user_success_response_id_1.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="function")
async def client_with_user(test_client: AsyncClient, create_user_success_body: dict):
    await test_client.post("/v1/user/", data=create_user_success_body)
    try:
        yield test_client
    except Exception as e:
        print(e)
    finally:
        await test_client.aclose()
