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
    table_data = await scan_database_for_installation(installation, db_session)
    # for table in table_data:
    #     if table.name not in


async def scan_database_for_installation(
    installation: Installation, db_session: Session
) -> List[DatabaseTable]:
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
