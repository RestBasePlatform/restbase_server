import json

import pytest
from httpx import AsyncClient
from models.server import ServerCredentials
from restbase_types.server import ServerConnectionCredentials
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_create_server_credentials(
    test_client: AsyncClient,
    db_test_session: Session,
    create_credentials_success_body: str,
    create_credentials_success_response: dict,
):
    response = await test_client.post(
        "/v1/server/credentials/", data=create_credentials_success_body
    )
    row = (
        db_test_session.query(ServerCredentials)
        .filter_by(id=response.json()["id"])
        .first()
    )
    create_credentials_success_body_json = json.loads(create_credentials_success_body)
    server_connection = ServerConnectionCredentials(
        **create_credentials_success_body_json
    )

    server_connection_in_db = row.get_server_credentials()
    assert response.status_code == 200
    assert response.json() == create_credentials_success_response
    assert row
    assert server_connection_in_db == server_connection


@pytest.mark.asyncio
async def test_patch_server_credentials(
    client_with_server_credentials: AsyncClient,
    db_test_session: Session,
    patch_credentials_success_body: str,
    patch_credentials_success_response: dict,
):
    response = await client_with_server_credentials.patch(
        "/v1/server/credentials/1", data=patch_credentials_success_body
    )
    assert response.status_code == 200
    assert response.text == "Successfully updated."

    row = db_test_session.query(ServerCredentials).filter_by(id=1).first()
    assert row

    create_credentials_success_body_json = json.loads(patch_credentials_success_body)
    server_connection = ServerConnectionCredentials(
        **create_credentials_success_body_json
    )
    server_connection_in_db = row.get_server_credentials()

    assert row
    assert server_connection_in_db == server_connection


@pytest.mark.asyncio
async def test_delete_server_credentials(
    client_with_server_credentials: AsyncClient,
    db_test_session: Session,
):
    response = await client_with_server_credentials.delete("/v1/server/credentials/1")
    assert response.status_code == 200
    assert response.text == "Successfully deleted."

    row = db_test_session.query(ServerCredentials).filter_by(id=1).first()
    assert not row


@pytest.mark.asyncio
async def test_get_server_credentials(
    client_with_server_credentials: AsyncClient,
    db_test_session: Session,
    get_credentials_success_response: dict,
):
    response = await client_with_server_credentials.get("/v1/server/credentials/")
    assert response.status_code == 200
    assert response.json() == get_credentials_success_response
