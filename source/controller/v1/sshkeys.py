import os
from io import StringIO
from typing import List
from typing import Tuple

import paramiko
from exceptions import AlreadyExistsError
from exceptions import CredentialsNotFoundError
from exceptions import ServerNotFoundError
from models.server import ServerCredentials
from models.server import Servers
from restbase_types.server import ServerConnectionData
from routes.v1.schemas import CreateServerSchema
from routes.v1.schemas import ServerCredentialSchema
from sqlalchemy.orm import Session


async def list_ssh_keys(db_session: Session) -> List[ServerCredentials]:
    return db_session.query(ServerCredentials).all()


async def add_server_credentials(
    request_data: ServerCredentialSchema, db_session: Session
) -> ServerCredentials:
    if request_data.username in [i.username for i in await list_ssh_keys(db_session)]:
        raise AlreadyExistsError("UserData", request_data.username)

    new_row = ServerCredentials(**request_data.dict())
    db_session.add(new_row)
    db_session.commit()

    return new_row


async def update_server_credentials(
    cred_id: int, update_data: ServerCredentialSchema, db_session: Session
) -> bool:
    if cred_id not in [i.id for i in await list_ssh_keys(db_session)]:
        raise CredentialsNotFoundError("id", cred_id)

    db_row = db_session.query(ServerCredentials).filter_by(id=cred_id).first()

    for field in update_data.dict():
        if getattr(update_data, field):
            if field in db_row.secret_attrs:
                db_row.set_secret_attr(field, getattr(update_data, field))
            else:
                setattr(db_row, field, getattr(update_data, field))

    db_session.commit()
    return True


async def delete_server_credentials(cred_id: int, db_session: Session) -> bool:
    if cred_id not in [i.id for i in await list_ssh_keys(db_session)]:
        raise CredentialsNotFoundError("id", cred_id)

    if db_session.query(Servers).filter_by(credential_id=cred_id).all():
        raise ValueError(
            f"Credentials in used. Please remove all servers with credential id = {cred_id} first."
        )

    db_row = db_session.query(ServerCredentials).filter_by(id=cred_id).first()

    db_session.delete(db_row)
    db_session.commit()
    return True


async def check_server(
    db_session: Session, *, name: str = None, server_data: CreateServerSchema = None
) -> Tuple[bool, int]:
    if not (name or server_data):
        raise ValueError("'name' or 'server_connection_data' must be specified")

    server_connection_data = None
    if name:
        server_row = db_session.query(Servers).filter_by(name=name).first()
        server_connection_data = server_row.get_server_credentials()
    elif server_data:
        credentials = (
            db_session.query(ServerCredentials)
            .filter_by(id=server_data.credential_id)
            .first()
        )
        server_connection_data = ServerConnectionData(
            host=server_data.host,
            port=server_data.port,
            connection_kwargs=server_data.connection_kwargs,
            connection_data=credentials,
        )

    return await check_server_availability(server_connection_data)


async def check_server_availability(
    server_connection_data: ServerConnectionData,
) -> Tuple[bool, int]:

    max_retry_count = os.getenv("MAX_CONNECTION_RETRY", 5)
    current_retry_count = 0
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key_file = StringIO(server_connection_data.connection_data.ssh_key)

    key = paramiko.RSAKey.from_private_key(private_key_file)
    while current_retry_count <= max_retry_count:
        try:
            client.connect(
                hostname=server_connection_data.host,
                port=server_connection_data.port,
                username=server_connection_data.connection_data.username,
                password=server_connection_data.connection_data.password,
                pkey=key,
            )

            return True, current_retry_count
        except Exception as e:
            print(e)
            current_retry_count += 1

    return False, current_retry_count


async def add_server(
    request_data: CreateServerSchema, db_session: Session
) -> Tuple[Servers, int]:
    if request_data.name in [i.name for i in await list_servers(db_session)]:
        raise AlreadyExistsError("Server", request_data.name)

    db_credential_row = (
        db_session.query(ServerCredentials)
        .filter_by(id=request_data.credential_id)
        .first()
    )

    if not db_credential_row:
        raise CredentialsNotFoundError("id", request_data.credential_id)

    server_row = Servers(**request_data.dict())

    is_server_available, retry_count = await check_server_availability(
        server_row.get_server_connection_data(db_session)
    )

    if is_server_available:
        server_row.server_status = "Available"
    else:
        server_row.server_status = "Not Available"

    db_session.add(server_row)
    db_session.commit()

    return server_row, retry_count


async def list_servers(db_session: Session) -> List[Servers]:
    return db_session.query(Servers).all()


async def delete_server(server_name: str, db_session: Session):
    server_row = db_session.query(Servers).filter_by(name=server_name).first()

    db_session.delete(server_row)
    db_session.commit()


async def update_server(
    server_name: str, update_data: CreateServerSchema, db_session: Session
) -> Tuple[Servers, int]:
    if server_name not in [i.name for i in await list_servers(db_session)]:
        raise ServerNotFoundError("name", server_name)

    server_row = db_session.query(Servers).filter_by(name=server_name).first()

    for field in update_data.dict():
        if field == "credential_id" and getattr(update_data, field):
            if getattr(update_data, field) not in [
                i.id for i in await list_ssh_keys(db_session)
            ]:
                raise CredentialsNotFoundError("id", getattr(update_data, field))
        if getattr(update_data, field):
            setattr(server_row, field, getattr(update_data, field))

    is_server_available, retry_count = await check_server_availability(
        server_row.get_server_connection_data(db_session)
    )

    if is_server_available:
        server_row.server_status = "Available"
    else:
        server_row.server_status = "Not Available"

    db_session.commit()
    return server_row, retry_count
