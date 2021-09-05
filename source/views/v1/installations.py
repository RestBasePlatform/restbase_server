from typing import Optional

from models import DatabaseConnectionData
from models import Installation
from models import Submodule


def present_installation_data(
    installation: Installation,
    submodule: Submodule,
    db_con_data: Optional[DatabaseConnectionData],
) -> dict:
    answer = {
        "Installation name": installation.name,
        "Installation date": installation.installation_date.strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "Submodule": present_submodule_data(submodule),
    }

    if db_con_data:
        answer = {
            **answer,
            **{"Database server info": db_con_data.get_connection_data()},
        }

    return answer


def present_submodule_data(submodule: Submodule) -> dict:
    return {
        "Submodule Name": submodule.name,
        "Submodule version": submodule.version,
        "Minimal module version": submodule.min_module_version,
        "Released at": submodule.release_date.strftime("%d-%m-%Y %H:%M:%S"),
        "Files URL": submodule.files_url,
    }
