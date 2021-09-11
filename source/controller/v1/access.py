from exceptions import GroupNotFoundError
from exceptions import UserNotFoundError
from models import AccessRule
from models import Base
from models import Installation
from models import User
from sqlalchemy.orm import Session

from .database import get_database_object_by_address


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


async def grant_access_to_user(
    user_id: int,
    database_object_address: dict,
    installation: Installation,
    access_string: str,
    db_session: Session,
) -> int:
    user_row = db_session.query(User).filter_by(id=user_id).first()
    if not user_row:
        raise UserNotFoundError("id", user_id)

    database_object = await get_database_object_by_address(
        installation, db_session, **database_object_address
    )

    access_rule = await add_access_rule(
        user_row,
        database_object,
        access_string,
        db_session,
    )

    return access_rule.id
