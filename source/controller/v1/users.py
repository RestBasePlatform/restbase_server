from typing import List
from typing import Union

from controller.v1.submodule import execute_submodule_function
from exceptions import AlreadyExistsError
from exceptions import GroupNotFoundError
from exceptions import InstallationNotFound
from exceptions import UserNotFoundError
from models import DatabaseConnectionData
from models import Group
from models import Installation
from models import User
from models.utils import get_pkey_referenced_row
from routes.v1.schemas import CreateUserSchema
from routes.v1.schemas import EditUserSchema
from sqlalchemy.orm import Session


async def create_user(
    user: CreateUserSchema,
    db_session: Session,
) -> User:
    """Create user for future inject in database

    Parameters
    ----------
    user : CreateUserSchema
        Object from request body
    db_session : Session
        SQL Alchemy ORM Session

    Returns
    -------
    User
        SQL Alchemy ORM User object

    Raises
    ------
    AlreadyExistsError
        If user.username found in database
    """

    if user.username in [
        i.get_user_data().username for i in db_session.query(User).all()
    ]:
        raise AlreadyExistsError("User", user.username)

    user_row = User(
        username=user.username, password=user.password, comment=user.comment
    )
    db_session.add(user_row)
    db_session.commit()

    for group in user.group_list:
        await add_user_to_group(user_row.id, "id", group, db_session)

    return user_row


async def edit_user(
    user_id: int,
    user: EditUserSchema,
    db_session: Session,
) -> User:
    """Edit user data in database.

    Parameters
    ----------
    user_id : int
        User id in database
    user : EditUserSchema
        Object from request body
    db_session : Session
        SQL Alchemy ORM Session

    Returns
    -------
    User
        SQL Alchemy ORM User object

    Raises
    ------
    UserNotFoundError
        If user_id not exists in database
    """
    user_row = db_session.query(User).filter_by(id=user_id).first()

    if not user_row:
        raise UserNotFoundError("id", user_id)

    for field in user.dict():
        if getattr(user, field):
            if field in ["username", "password"]:
                user_row.set_secret(field, getattr(user, field))
            else:
                setattr(user_row, field, getattr(user, field))

    db_session.commit()

    return user_row


async def create_group(
    name: str,
    user_list: List[int],
    db_session: Session,
    comment: str,
) -> Group:
    if name in await get_group_names(db_session):
        raise AlreadyExistsError("Group", name)

    group = Group(name=name, user_list="", comment=comment)
    db_session.add(group)
    db_session.commit()

    user_id_list = await get_user_ids(db_session)

    for user in user_list:
        if user in user_id_list:
            await add_user_to_group(user, "id", group.id, db_session)
        else:
            db_session.delete(group)
            db_session.commit()
            raise UserNotFoundError("id", user)

    return group


async def add_user_to_group(
    user_id: int,
    identifier: str,
    identifier_value: Union[str, int],
    db_session: Session,
):
    """Add user to group

    Parameters
    ----------
    user_id : int
        User id in database
    identifier : str
        "id" or "name" depends on identifier_value
    identifier_value : Union[str, int]
        "id" or "name" depends on identifier
    db_session : Session
        SQL Alchemy ORM User object

    Raises
    ------
    GroupNotFoundError
        If identifier_value, identifier of group not exists in database
    UserNotFoundError
        If user_id not exists in database
    """
    group = db_session.query(Group).filter_by(**{identifier: identifier_value}).first()
    user = db_session.query(User).filter_by(id=user_id).first()

    if not group:
        raise GroupNotFoundError(identifier, identifier_value)
    if not user:
        raise UserNotFoundError("id", user_id)
    if group.user_list:
        group.user_list = ",".join(group.user_list.split(",") + [str(user_id)])
    else:
        group.user_list = str(user_id)
    db_session.commit()


async def get_group_names(db_session: Session) -> List[str]:
    return [i.name for i in db_session.query(Group).all()]


async def get_group(group_name: str, db_session: Session) -> Group:
    return next(db_session.query(Group).filter_by(name=group_name))


async def get_user_ids(db_session: Session) -> List[int]:
    return [i.id for i in db_session.query(User).all()]


async def inject_user_in_installation(
    user_id: int, installation_name: str, db_session: Session
):
    """Crete user with data from user_id in installation

    Parameters
    ----------
    user_id : int
        User id in database
    installation_name : str
        Name of installation
    db_session : Session
        SQL Alchemy ORM User object

    Raises
    ------
    InstallationNotFound
        If installation name not exists in database
    UserNotFoundError
        If user_id not exists in database
    """
    installation = (
        db_session.query(Installation).filter_by(name=installation_name).first()
    )

    if not installation:
        raise InstallationNotFound(installation_name)

    user = db_session.query(User).filter_by(id=user_id).first()

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


def get_user_id_by_username(username: str, db_session: Session) -> int:
    for user in db_session.query(User).all():
        if username == user.get_user_data().username:
            return user.id


async def delete_user(user_id: int, db_session: Session):
    user_row = db_session.query(User).filter_by(id=user_id).first()

    if not user_row:
        raise UserNotFoundError("id", user_id)

    for group in db_session.query(Group).all():
        await remove_user_from_group(user_id, "id", group.id, db_session)

    db_session.delete(user_row)
    db_session.commit()


async def remove_user_from_group(
    user_id: int,
    identifier: str,
    identifier_value: Union[str, int],
    db_session: Session,
):
    group = db_session.query(Group).filter_by(**{identifier: identifier_value}).first()
    user_row = db_session.query(User).filter_by(id=user_id).first()

    if not user_row:
        raise UserNotFoundError("id", user_id)

    if not group:
        raise GroupNotFoundError(identifier, identifier_value)

    group_row = db_session.query(Group).filter_by(id=group.id).first()

    group_row_user_list = group_row.user_list.split(",")
    group_row_user_list.remove(str(user_id))
    group_row.user_list = ",".join(group_row_user_list)
    db_session.commit()
