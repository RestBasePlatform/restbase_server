from controller.v1.installation import create_installation
from controller.v1.installation import delete_installation
from controller.v1.installation import get_installation
from controller.v1.installation import list_installations_names
from views.v1.installations import present_installation_data
from fastapi import APIRouter
from fastapi import Depends
from models.utils import get_db_session


installation_router = APIRouter(prefix="/installation", tags=["Installation"])


@installation_router.post("/create")
async def _create_installation(
    installation_name: str,
    module_name: str,
    version: str,
    db_session=Depends(get_db_session),
):
    create_installation(installation_name, module_name, version, db_session)
    return 200


@installation_router.delete("/")
async def _delete_installation(
    installation_name: str,
    db_session=Depends(get_db_session),
):
    delete_installation(installation_name, db_session)
    return 200


@installation_router.get("/list")
async def _list_installations(
    db_session=Depends(get_db_session),
):
    return {"available_installations": list_installations_names(db_session)}


@installation_router.get("/")
async def _get_installation(
    installation_name: str,
    db_session=Depends(get_db_session),
):
    installation, submodule = get_installation(installation_name, db_session)
    return present_installation_data(installation, submodule)
