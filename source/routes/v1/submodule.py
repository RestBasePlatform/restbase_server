from controller.v1.submodule import update_module_list
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.utils import get_db_session


submodule_router = APIRouter(prefix="/submodule")


@submodule_router.post("/update_module_list")
async def _update_module_list(full_update: bool = False, db_session=Depends(get_db_session)):
    update_module_list(db_session, full_update=full_update)
    return 200
