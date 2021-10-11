from user_groups.fixtures import *  # noqa: F403, F401
from httpx import AsyncClient
import pytest
from sqlalchemy.orm import Session
from models.user import User


@pytest.mark.asyncio
async def test_create_user(
    test_client: AsyncClient,
    db_test_session: Session,
    create_user_success_body: str,
    create_user_success_response_response: dict
):
    response = (
        await test_client.post("/v1/user/", data=create_user_success_body)
    ).json()
    json_body = json.loads(create_user_success_body)
    assert response == create_user_success_response_response
    row = db_test_session.query(User).filter_by(id=response["id"]).first()
    assert row.id == response["id"]
    user_data = row.get_user_data()
    assert user_data.username == json_body['username']
    assert user_data.password == json_body['password']
