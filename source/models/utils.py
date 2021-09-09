import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///database.db")
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

    Returns
    -------
    [type]
        [description]
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
