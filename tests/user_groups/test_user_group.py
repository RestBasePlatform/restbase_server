import asynctest
import pytest
from httpx import AsyncClient
from models.user import Group
from sqlalchemy.orm import Session
from user_groups.fixtures import *  # noqa: F403, F401


@pytest.mark.asyncio
async def test_add_user_to_group(
    client_with_group_with_no_users_and_user: AsyncClient,
    db_test_session: Session,
):
    response = await client_with_group_with_no_users_and_user.post(
        "/v1/group/test-group-1/add_user/1"
    )
    assert response.status_code == 200
    group_row = db_test_session.query(Group).filter_by(id=1).first()
    print(group_row.id)
    assert group_row.user_list


@pytest.mark.asyncio
async def test_remove_user_from_group(
    client_with_group_with_user_and_user: AsyncClient,
    db_test_session: Session,
):
    response = await client_with_group_with_user_and_user.post(
        "/v1/group/test-group-1/remove_user/1"
    )
    assert response.status_code == 200
    group_row = db_test_session.query(Group).filter_by(id=1).first()
    assert not group_row.user_list


@pytest.mark.asyncio
async def test_inject_user_in_installation(
    client_wit_user_and_installation: AsyncClient,
    db_test_session: Session,
):
    with asynctest.patch(
        "controller.v1.users.execute_submodule_function"
    ) as execute_submodule_function_mock:
        execute_submodule_function_mock.side_effect = [True]

        response = await client_wit_user_and_installation.post(
            "/v1/user/1/inject/test-1"
        )

        assert response.status_code == 200
