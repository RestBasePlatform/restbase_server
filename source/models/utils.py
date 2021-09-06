import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db_session = Session()
    return db_session


def get_pkey_referenced_row(
    row_with_fk,
    fk_col_name: str,
    fk_column_orm_link,
    db_session,
    *,
    attr_to_get: str = None,
    function_to_execute: str = None
):
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
