from controller.v1.installation import create_installation
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.utils import get_db_session


installation_router = APIRouter(prefix="/installation", tags=["Installation"])


@installation_router.post(f"/create")
async def _create_installation(
    installation_name: str,
    module_name: str,
    version: str,
    db_session=Depends(get_db_session),
):
    create_installation(installation_name, module_name, version, db_session)
    return 200
