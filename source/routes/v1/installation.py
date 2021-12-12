from controller.v1.installation import create_installation
from controller.v1.installation import delete_installation
from controller.v1.installation import get_installation
from controller.v1.installation import list_installations_names
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.utils import get_db_session
from views.v1.installations import present_installation_data

from .schemas import CreateInstallationModel


installation_router = APIRouter(prefix="/installation", tags=["Installation"])


@installation_router.post("/")
async def _create_installation(
    body: CreateInstallationModel,
    db_session=Depends(get_db_session),
):
    try:
        installation = await create_installation(
            body.installation_name,
            body.submodule_name,
            body.submodule_version,
            db_session,
            **body.get_db_con_data()
        )
        return {"name": installation.name}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@installation_router.delete("/{installation_name}")
async def _delete_installation(
    installation_name: str,
    db_session=Depends(get_db_session),
):
    delete_installation(installation_name, db_session)
    return 200


@installation_router.get("/")
async def _list_installations(
    db_session=Depends(get_db_session),
):
    return list_installations_names(db_session)


@installation_router.get("/{installation_name}")
async def _get_installation(
    installation_name: str,
    with_credentials: bool,
    db_session=Depends(get_db_session),
):
    installation, submodule, db_con_data = await get_installation(
        installation_name, with_credentials, db_session
    )
    return present_installation_data(installation, submodule, db_con_data)
