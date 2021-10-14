import json

import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session")
def create_user_success_body():
    with open("tests/user_groups/static/requests/create_user_body.json") as f:
        return f.read()


@pytest.fixture(scope="session")
def create_group_no_users_success_body():
    with open("tests/user_groups/static/requests/create_group_body_no_users.json") as f:
        return f.read()


@pytest.fixture(scope="session")
def create_group_no_users_success_response():
    with open(
        "tests/user_groups/static/responses/create_group_no_users_response.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def create_group_with_users_success_body():
    with open(
        "tests/user_groups/static/requests/create_group_body_with_users.json"
    ) as f:
        return f.read()


@pytest.fixture(scope="session")
def create_group_with_users_success_response():
    with open("tests/user_groups/static/responses/create_group_with_users.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def create_group_with_not_exist_users_response():
    with open(
        "tests/user_groups/static/responses/create_group_with_not_exist_users.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def create_user_success_response_response():
    with open(
        "tests/user_groups/static/responses/create_user_success_response_id_1.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def edit_user_success_body():
    with open("tests/user_groups/static/requests/edit_user_body.json") as f:
        return f.read()


@pytest.fixture(scope="session")
def edit_user_success_response_response():
    with open(
        "tests/user_groups/static/responses/edit_user_success_response_id_1.json"
    ) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def create_user_already_exists_error_response():
    with open(
        "tests/user_groups/static/responses/create_user_already_exists_error.json"
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


@pytest.fixture(scope="function")
async def client_with_group(test_client: AsyncClient, create_user_success_body: dict):
    await test_client.post("/v1/group/", data=create_group_with_users_success_body)
    try:
        yield test_client
    except Exception as e:
        print(e)
    finally:
        await test_client.aclose()


@pytest.fixture(scope="function")
async def client_with_group_and_user(
    client_with_user: AsyncClient, create_group_with_users_success_body: dict
):
    await client_with_user.post("/v1/group/", data=create_group_with_users_success_body)
    try:
        yield client_with_user
    except Exception as e:
        print(e)
    finally:
        await client_with_user.aclose()
