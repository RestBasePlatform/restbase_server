import os
from typing import List

import yaml
from exceptions import RowNotFoundError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv("DB_URL", "sqlite:///database.db"))
_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db_session = _Session()
    return db_session


def get_pkey_referenced_row(
    row_with_fk,
    fk_col_name: str,
    fk_column_orm_link,
    db_session: Session,
    *,
    attr_to_get: str = None,
    function_to_execute: str = None
):
    """Returns the row referenced by the FK in the passed string

    Parameters
    ----------
    row_with_fk : Base
        Row with ForeignKey column.
    fk_col_name : str
        ForeignKey column name
    fk_column_orm_link : Base
        ORM Object that referenced in ForeignKey
    db_session : Session
        SQLAlchemy ORM session
    attr_to_get : str, optional
        Attribute to exctract from fk_column_orm_link, by default None
    function_to_execute : str, optional
        Function to call in fk_column_orm_link object, by default None
    """
    orm_fk_row = (
        db_session.query(fk_column_orm_link)
        .filter_by(id=getattr(row_with_fk, fk_col_name))
        .first()
    )

    if attr_to_get:
        return getattr(orm_fk_row, attr_to_get)
    elif function_to_execute:
        return getattr(orm_fk_row, function_to_execute)()
    else:
        return orm_fk_row


def initialize_data_in_tables(db_session: Session, *, cfg_path="./config/"):
    """Fill database tables with data from config folder.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy ORM session
    cfg_path : str, optional
        Path to folder with yaml configs, by default "./config/"
    """

    for file in os.listdir(cfg_path):
        filename = file.split(".")[0]
        with open(cfg_path + file) as f:
            data = yaml.load(f.read())

            for row in data:
                db_class = getattr(__import__("models"), filename)
                exist_row = db_session.query(db_class).filter_by(id=row["id"])
                if exist_row:
                    exist_row.delete()
                    db_session.commit()
                db_obj = db_class(**row)
                db_session.add(db_obj)
                db_session.commit()


def get_id_by_name(db_object, name: str, db_session: Session) -> int:
    row = db_session.query(db_object).filter_by(name=name).first()
    if not row:
        raise RowNotFoundError(name, db_object.__tablename__)

    return getattr(row, "id", None)


async def get_user_list_names_by_ids(
    user_id_list: List[int], db_session: Session
) -> List[str]:
    user_names = []
    from models.user import User

    for u_id in user_id_list:
        user_name = getattr(db_session.query(User).filter_by(id=u_id).first(), "name")
        if user_name:
            user_names.append(user_name)

    return user_names
