import pytest
from httpx import AsyncClient
from models.user import Group
from sqlalchemy.orm import Session
from user_groups.fixtures import *  # noqa: F403, F401


@pytest.mark.asyncio
async def test_create_group_no_users(
    test_client: AsyncClient,
    db_test_session: Session,
    create_group_no_users_success_body: str,
    create_group_no_users_success_response: dict,
):
    response = (
        await test_client.post("/v1/group/", data=create_group_no_users_success_body)
    ).json()
    assert response == create_group_no_users_success_response
    row = db_test_session.query(Group).filter_by(id=response["id"]).first()
    assert row.id == response["id"]
    assert row.name == response["name"]
    assert row.comment == response["comment"]
    assert row.user_list == response["users"]


@pytest.mark.asyncio
async def test_create_group_with_not_exist_users(
    test_client: AsyncClient,
    db_test_session: Session,
    create_group_with_users_success_body: str,
    create_group_with_not_exist_users_response: dict,
):
    response = await test_client.post(
        "/v1/group/", data=create_group_with_users_success_body
    )
    assert response.status_code == 400
    assert response.json() == create_group_with_not_exist_users_response
    assert not db_test_session.query(Group).first()


@pytest.mark.asyncio
async def test_create_group_with_users(
    client_with_user: AsyncClient,
    db_test_session: Session,
    create_group_with_users_success_body: str,
    create_group_with_users_success_response: dict,
):
    response = (
        await client_with_user.post(
            "/v1/group/", data=create_group_with_users_success_body
        )
    ).json()
    assert response == create_group_with_users_success_response
    row = db_test_session.query(Group).filter_by(id=response["id"]).first()

    assert row.id == response["id"]
    assert row.name == response["name"]
    assert row.comment == response["comment"]
    assert row.user_list == response["users"]
