import json

import asynctest  # noqa: F401
import pytest
from httpx import AsyncClient
from installation.conftest import *  # noqa: F403, F401
from models.sublodules import Installation
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_create_installation(
    client_with_submodules: AsyncClient,
    db_test_session: Session,
    create_installation_success_body: str,
    create_installation_success_response: dict,
):
    response = (
        await client_with_submodules.post(
            "/v1/installation/", data=create_installation_success_body
        )
    ).json()
    assert response == create_installation_success_response
    body_dict = json.loads(create_installation_success_body)
    installation_row = (
        db_test_session.query(Installation)
        .filter_by(name=body_dict["installation_name"])
        .first()
    )
    assert installation_row


@pytest.mark.asyncio
async def test_create_installation_name_already_exists(
    client_with_test_installation: AsyncClient,
    create_installation_success_body: dict,
    create_installation_name_already_exists_response: dict,
):
    response = (
        await client_with_test_installation.post(
            "/v1/installation/", data=create_installation_success_body
        )
    ).json()
    assert response == create_installation_name_already_exists_response


@pytest.mark.parametrize(
    "with_credentials, expected_response",
    [
        (False, get_installation_no_credentials_response),  # noqa: F405
        (True, get_installation_with_credentials_response),  # noqa: F405
    ],
)
@pytest.mark.asyncio
async def get_installation(
    with_credentials: bool,
    expected_response: dict,
    client_with_test_installation: AsyncClient,
):
    response = (
        await client_with_test_installation.get(
            "/v1/installation/test-1", params={"with_credentials": with_credentials}
        )
    ).json()
    assert response == expected_response
