from models.server import ServerCredentials
from models.server import Servers
from sqlalchemy.orm import Session


def present_server_credential_data(obj: ServerCredentials) -> dict:
    return {
        "id": obj.id,
        "username": obj.username,
        "password": "***" if obj.password else "No password",
        "ssh_key": "***" if obj.ssh_key else "Not defined",
    }


def present_server_data(
    server_obj: Servers, db_session: Session, retry_count: int = None
) -> dict:
    credentials_obj = (
        db_session.query(ServerCredentials)
        .filter_by(id=server_obj.credential_id)
        .first()
    )

    credentials_response = present_server_credential_data(credentials_obj)

    response = {
        "name": server_obj.name,
        "host": server_obj.host,
        "port": server_obj.port,
        "connection_kwargs": server_obj.connection_kwargs,
        "status": server_obj.server_status,
        "credentials": credentials_response,
    }

    if retry_count:
        response = {**response, **{"retry_count": retry_count}}

    return response


def present_server_health_check_data(status: bool, retry_count: int) -> dict:
    return {"status": status, "retry_count": retry_count}
