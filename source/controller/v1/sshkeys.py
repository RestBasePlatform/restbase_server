from typing import List

from exceptions import AlreadyExistsError
from exceptions import CredentialsNotFoundError
from models.server import ServerCredentials
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
            setattr(db_row, field, getattr(update_data, field))

    db_session.commit()
    return True


async def delete_server_credentials(cred_id: int, db_session: Session) -> bool:
    if cred_id not in [i.id for i in await list_ssh_keys(db_session)]:
        raise CredentialsNotFoundError("id", cred_id)

    db_row = db_session.query(ServerCredentials).filter_by(id=cred_id).first()

    db_session.delete(db_row)
    db_session.commit()
    return True
