from exceptions import GroupNotFoundError
from exceptions import UserNotFoundError
from models import AccessRule
from models import Base
from models import Installation
from sqlalchemy.orm import Session

from .database import get_database_object_by_address
from controller.v1.users import get_user_id_by_username


async def add_access_rule(
    entity_object: Base, database_object: Base, access_string: str, db_session: Session
) -> AccessRule:
    access_row = AccessRule(
        access_owner_type=entity_object.__tablename__,
        access_owner_id=entity_object.id,
        access_object_type=database_object.__tablename__,
        access_object_id=database_object.id,
        access_type=access_string,
        session=db_session,
    )
    db_session.add(access_row)
    db_session.commit()
    return access_row


async def grant_access(
    granter_name: str,
    granter_type: str,
    database_object_address: dict,
    installation_name: str,
    access_string: str,
    db_session: Session,
) -> int:

    for k in database_object_address:
        database_object_address[k.replace('_', '')] = database_object_address[k]
    print(database_object_address)
    installation_obj = db_session.query(Installation).filter_by(name=installation_name).first()
    granter_orm_object = getattr(__import__("models"), granter_type)

    if granter_type == "User":
        granter_id = get_user_id_by_username(granter_name, db_session)

    granter_row = (
        db_session.query(granter_orm_object)
        .filter_by(id=granter_id)
        .first()
    )
    if not granter_row:
        if granter_type == "User":
            raise UserNotFoundError("id", granter_id)
        elif granter_type == "Group":
            raise GroupNotFoundError("id", granter_id)
        else:
            raise ValueError(f"{granter_type} with id {id} not found")

    database_object = await get_database_object_by_address(
        installation_obj, db_session, **database_object_address
    )

    access_rule = await add_access_rule(
        granter_row,
        database_object,
        access_string,
        db_session,
    )

    return access_rule.id
