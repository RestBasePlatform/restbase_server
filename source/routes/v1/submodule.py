from controller.v1.submodule import get_submodule_data
from controller.v1.submodule import get_submodule_list
from controller.v1.submodule import update_module_list
from fastapi import APIRouter
from fastapi import Depends
from models.utils import get_db_session
from views.v1.installations import present_submodule_data


submodule_router = APIRouter(prefix="/submodule", tags=["Submodule"])


@submodule_router.post("/update_module_list")
async def _update_submodule_list(
    full_update: bool = False, db_session=Depends(get_db_session)
):
    await update_module_list(db_session, full_update=full_update)
    return 200


@submodule_router.get("/")
async def _get_submodule_data(
    submodule_name: str, version: str, db_session=Depends(get_db_session)
):
    submodule = await get_submodule_data(submodule_name, version, db_session)
    return present_submodule_data(submodule)


@submodule_router.get("/list")
async def _get_submodule_list(db_session=Depends(get_db_session)):
    submodule_list = await get_submodule_list(db_session)
    print(submodule_list)
    return [present_submodule_data(i) for i in submodule_list]


@submodule_router.get("/listNames")
async def _get_submodule_names_list(db_session=Depends(get_db_session)):
    submodule_list = await get_submodule_list(db_session)
    return [i.name for i in submodule_list]


@submodule_router.get("/{submodule_name}/versions")
async def _get_submodule_versions(
    submodule_name: str, db_session=Depends(get_db_session)
):
    submodule_list = await get_submodule_list(db_session)
    return [i.version for i in submodule_list if i.name == submodule_name]
