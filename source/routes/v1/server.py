from controller.v1.sshkeys import add_server_credentials
from controller.v1.sshkeys import delete_server_credentials
from controller.v1.sshkeys import list_ssh_keys
from controller.v1.sshkeys import update_server_credentials
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi.exceptions import HTTPException
from models.utils import get_db_session
from views.v1.server import present_server_credential_data

from .schemas import ServerCredentialSchema


server_router = APIRouter(prefix="/server", tags=["Server"])


@server_router.post("/credentials/")
async def create_credentials(
    credentials: ServerCredentialSchema, db_session=Depends(get_db_session)
):
    try:
        credential = await add_server_credentials(credentials, db_session)
        return present_server_credential_data(credential)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.get("/credentials/")
async def get_credentials(db_session=Depends(get_db_session)):
    try:
        credentials = await list_ssh_keys(db_session)
        return [present_server_credential_data(i) for i in credentials]
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.patch("/credentials/{credential_id}")
async def update_credentials(
    credential_id: int,
    credentials: ServerCredentialSchema,
    db_session=Depends(get_db_session),
):
    try:
        await update_server_credentials(credential_id, credentials, db_session)
        return Response(status_code=200, content="Successfully updated.")
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.delete("/credentials/{credential_id}")
async def delete_credentials(
    credential_id: int,
    db_session=Depends(get_db_session),
):
    try:
        await delete_server_credentials(credential_id, db_session)
        return Response(status_code=200, content="Successfully deleted.")
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)
