import json

import asynctest  # noqa: F401
import pytest
from httpx import AsyncClient
from installation.fixtures import *  # noqa: F403, F401
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
    print(installation_row)
    assert installation_row


@pytest.mark.asyncio
async def test_create_installation_name_already_exists(
    client_with_submodules: AsyncClient,
    create_installation_success_body: dict,
    create_installation_name_already_exists_response: dict,
):
    (
        await client_with_submodules.post(
            "/v1/installation/", data=create_installation_success_body
        )
    ).json()
    response = (
        await client_with_submodules.post(
            "/v1/installation/", data=create_installation_success_body
        )
    ).json()
    assert response == create_installation_name_already_exists_response
