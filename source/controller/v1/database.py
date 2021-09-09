from typing import List

from controller.v1.submodule import execute_submodule_function
from models import ColumnList
from models import DatabaseConnectionData
from models import DatabaseList
from models import Installation
from models import SchemaList
from models import Submodule
from models import TableList
from models.utils import get_pkey_referenced_row
from restbase_types import DatabaseTable
from sqlalchemy.orm import Session


async def refresh_database_data(installation: Installation, db_session: Session):
    """Refresh database structure data in local database.

    Parameters
    ----------
    installation : Installation
        Object of installation for correct duplicate search.
    db_session : Session
        SQLAlchemy ORM session.
    """
    table_data = await scan_database_for_installation(installation, db_session)
    for table in table_data:
        if not is_table_row_exists(table, installation, db_session):
            db_id = await create_database_row(
                table.database.name, installation.name, db_session
            )
            schema_id = await create_schema_row(table.schema.name, db_id, db_session)
            table_id = await create_table_row(table.name, schema_id, db_session)
            for column in table.column_list:
                await create_column_row(
                    column.name, table_id, column.data_type, db_session
                )


async def scan_database_for_installation(
    installation: Installation, db_session: Session
) -> List[DatabaseTable]:
    """Executes function in submodule and returns full installation structure.

    Parameters
    ----------
    installation : Installation
        Object of installation to scan.
    db_session : Session
        SQLAlchemy ORM session.

    Returns
    -------
    List[DatabaseTable]
        List of full config data from database.
    """
    tables_list = await execute_submodule_function(
        get_pkey_referenced_row(
            installation, "submodule_id", Submodule, db_session, attr_to_get="id"
        ),
        "common",
        "get_table_data",
        db_session,
        db_con_data=get_pkey_referenced_row(
            installation,
            "connection_data_id",
            DatabaseConnectionData,
            db_session,
            function_to_execute="get_connection_data",
        ),
    )

    return tables_list


def is_table_row_exists(
    _table: DatabaseTable, installation: Installation, db_session: Session
) -> bool:
    """Check if table was already added in local database.

    Parameters
    ----------
    _table : DatabaseTable
        Object get after database scan.
    installation : Installation
        Object of installation for correct duplicate search.
    db_session : Session
        SQLAlchemy ORM session.

    Returns
    -------
    [bool]
        Is table from same installation/database/schema already exists in local database.
    """
    for exist_table in get_full_table_data_list(installation.name, db_session):
        if (_table.name == exist_table["table_name"]) and (
            _table.schema.name == exist_table["schema_name"]
            and (_table.database.name == exist_table["database_name"])
        ):
            return True
    return False


def get_full_table_data_list(installation_name: str, db_session: Session) -> List[dict]:
    """Extract full current database structure for installation from local database.

    Parameters
    ----------
    installation_name : str
        Installation name.
    db_session : Session
        SQLAlchemy ORM session.

    Returns
    -------
    List[dict]
        List of dictionary with database.
        Dict loooks like: {"table_name": "name", "schema_name": "name", "database_name": "name"}
    """
    with open("templates/get_table_data_request.sql") as f:
        request = f.read()
        request = request.replace("INSTALLATION_NAME", installation_name)

    return [
        {"table_name": i[0], "schema_name": i[1], "database_name": i[2]}
        for i in db_session.execute(request).fetchall()
    ]


async def create_database_row(
    db_name: str, installation_name: str, db_session: Session
) -> int:
    db_row = (
        db_session.query(DatabaseList)
        .filter_by(name=db_name, installation=installation_name)
        .first()
    )
    if not db_row:
        db_row = DatabaseList(name=db_name, installation=installation_name)
        db_session.add(db_row)
        db_session.commit()
    return db_row.id


async def create_schema_row(
    schema_name: str, database_id: int, db_session: Session
) -> int:
    row = (
        db_session.query(SchemaList)
        .filter_by(name=schema_name, database=database_id)
        .first()
    )
    if not row:
        row = SchemaList(name=schema_name, database=database_id)
        db_session.add(row)
        db_session.commit()
    return row.id


async def create_table_row(table_name: str, schema_id: int, db_session: Session) -> int:
    row = (
        db_session.query(TableList).filter_by(name=table_name, schema=schema_id).first()
    )
    if not row:
        row = TableList(name=table_name, schema=schema_id)
        db_session.add(row)
        db_session.commit()
    return row.id


async def create_column_row(
    column_name: str, table_id: int, data_type: str, db_session: Session
) -> int:
    row = (
        db_session.query(ColumnList).filter_by(name=column_name, table=table_id).first()
    )
    if not row:
        row = ColumnList(name=column_name, table=table_id, datatype=data_type)
        db_session.add(row)
        db_session.commit()
    return row.id
