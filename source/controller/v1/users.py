from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from controller.v1.submodule import execute_submodule_function
from exceptions import AlreadyExistsError
from exceptions import GroupNotFoundError
from exceptions import InstallationNotFound
from exceptions import UserNotFoundError
from models import DatabaseConnectionData
from models import Groups
from models import Installation
from models import Users
from models.utils import get_pkey_referenced_row
from restbase_types import DatabaseConnectionData
from restbase_types import UserData
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

    user_id_list = get_user_ids(db_session)

    for user in user_list:
        if user in user_id_list:
            await add_user_to_group(user, "id", group.id, db_session)
        else:
            UserNotFoundError("id", user)

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


async def get_user_ids(db_session: Session) -> List[int]:
    return [i.id for i in db_session.query(Users).all()]


async def inject_user_in_installation(
    user_id: int, installation_name: str, db_session: Session
):
    installation = (
        db_session.query(Installation).filter_by(name=installation_name).first()
    )

    if not installation:
        raise InstallationNotFound(installation_name)

    user = db_session.query(Users).filter_by(id=user_id).first()

    if not user:
        raise UserNotFoundError("id", user_id)
    db_connection_row = get_pkey_referenced_row(
        installation, "connection_data_id", DatabaseConnectionData, db_session
    )

    await execute_submodule_function(
        installation.submodule_id,
        "user",
        "create",
        db_session,
        user_data=user.get_user_data(),
        connection_data=DatabaseConnectionData(
            **db_connection_row.get_connection_data()
        ),
    )