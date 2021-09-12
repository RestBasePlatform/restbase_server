from controller.v1.access import grant_access
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.utils import get_db_session

from .schemas import GrantAccessSchema


access_router = APIRouter(prefix="/access", tags=["Access"])


@access_router.post("/")
async def _grant_access(body: GrantAccessSchema, db_session=Depends(get_db_session)):
    access_id = await grant_access(
        body.granter_type_name,
        body.granter_type,
        body.database_address.dict(by_alias=True),
        body.installation_name,
        body.access_string,
        db_session,
    )

    return access_id
