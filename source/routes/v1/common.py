from controller.v1.common import get_object_types_list
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.utils import get_db_session

common_router = APIRouter(prefix="/common")


@common_router.get("get_object_names/{object_type}", tags=["Access"])
async def _get_object_names(object_type: str, db_session=Depends(get_db_session)):
    try:
        return await get_object_types_list(object_type, db_session)
    except BaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
