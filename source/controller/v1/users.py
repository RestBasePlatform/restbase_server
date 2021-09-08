from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from exceptions import AlreadyExistsError
from exceptions import GroupNotFoundError
from models import Groups
from models import Users
from sqlalchemy.orm import Session


async def create_user(
    username: str,
    password: str,
    group_list: List[str],
    db_session: Session,
    comment: str,
) -> int:
    user = Users(username=username, password=password, comment=comment)
    db_session.add(user)
    db_session.commit()

    for group in group_list:
        await add_user_to_group(user.id, "id", group, db_session)

    return user.id


async def create_group(
    name: str,
    user_list: List[int],
    db_session: Session,
    comment: str,
) -> Groups:
    if name in await get_group_names(db_session):
        raise AlreadyExistsError("Group", name)

    group = Groups(name=name, user_list="", comment=comment)
    db_session.add(group)
    db_session.commit()

    for user in user_list:
        await add_user_to_group(user, "id", group.id, db_session)

    return group


async def add_user_to_group(
    user_id: int,
    identifier: str,
    identifier_value: Union[str, int],
    db_session: Session,
):
    group = db_session.query(Groups).filter_by(**{identifier: identifier_value}).first()

    if not group:
        raise GroupNotFoundError(identifier, identifier_value)
    if group.user_list:
        group.user_list = ",".join(group.user_list.split(",") + [str(user_id)])
    else:
        group.user_list = str(user_id)
    db_session.commit()


async def get_group_names(db_session: Session) -> List[str]:
    return [i.name for i in db_session.query(Groups).all()]
