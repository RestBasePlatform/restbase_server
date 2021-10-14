import json

import pytest
from httpx import AsyncClient
from models.user import Group
from models.user import User
from sqlalchemy.orm import Session
from user_groups.fixtures import *  # noqa: F403, F401


@pytest.mark.asyncio
async def test_create_user(
    test_client: AsyncClient,
    db_test_session: Session,
    create_user_success_body: str,
    create_user_success_response_response: dict,
):
    response = (
        await test_client.post("/v1/user/", data=create_user_success_body)
    ).json()
    json_body = json.loads(create_user_success_body)
    assert response == create_user_success_response_response
    row = db_test_session.query(User).filter_by(id=response["id"]).first()
    assert row.id == response["id"]
    user_data = row.get_user_data()
    assert user_data.username == json_body["username"]
    assert user_data.password == json_body["password"]


@pytest.mark.asyncio
async def test_create_user_already_exists(
    client_with_user: AsyncClient,
    create_user_success_body: str,
    create_user_already_exists_error_response: dict,
):
    response = await client_with_user.post("/v1/user/", data=create_user_success_body)
    assert response.status_code == 400
    assert response.json() == create_user_already_exists_error_response


@pytest.mark.asyncio
async def test_delete_user(client_with_user: AsyncClient, db_test_session: Session):
    response = await client_with_user.delete("/v1/user/1")
    assert response.status_code == 200
    row = db_test_session.query(User).filter_by(id=1).first()
    assert not row


@pytest.mark.asyncio
async def test_edit_user(
    client_with_user: AsyncClient,
    db_test_session: Session,
    edit_user_success_body: str,
    edit_user_success_response_response: dict,
):
    json_body = json.loads(edit_user_success_body)
    response = await client_with_user.patch("/v1/user/1", data=edit_user_success_body)
    assert response.status_code == 200
    assert response.json() == edit_user_success_response_response
    row = db_test_session.query(User).filter_by(id=1).first()
    assert row.id == response.json()["id"]
    user_data = row.get_user_data()
    assert user_data.username == json_body["username"]
    assert user_data.password == json_body["password"]


@pytest.mark.asyncio
async def test_delete_user_with_group_check(
    client_with_group_with_user_and_user: AsyncClient,
    db_test_session: Session,
):
    response = await client_with_group_with_user_and_user.delete("/v1/user/1")
    assert response.status_code == 200
    group_row = db_test_session.query(Group).filter_by(id=1).first()
    assert not group_row.user_list
