import json

import pytest
from httpx import AsyncClient
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
async def test_delete_user(client_with_user: AsyncClient, db_test_session: Session):
    response = await client_with_user.delete("/v1/user/1")
    assert response.status_code == 200
    row = db_test_session.query(User).filter_by(id=1).first()
    assert not row
