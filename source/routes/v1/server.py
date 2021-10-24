from controller.v1.sshkeys import add_server
from controller.v1.sshkeys import add_server_credentials
from controller.v1.sshkeys import check_server
from controller.v1.sshkeys import delete_server
from controller.v1.sshkeys import delete_server_credentials
from controller.v1.sshkeys import list_servers
from controller.v1.sshkeys import list_ssh_keys
from controller.v1.sshkeys import update_server
from controller.v1.sshkeys import update_server_credentials
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi.exceptions import HTTPException
from models.utils import get_db_session
from views.v1.server import present_server_credential_data
from views.v1.server import present_server_data
from views.v1.server import present_server_health_check_data

from .schemas import CreateServerSchema
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


@server_router.post("/")
async def create_server(
    request: CreateServerSchema,
    db_session=Depends(get_db_session),
):
    try:
        server, retry_count = await add_server(request, db_session)
        return present_server_data(server, db_session, retry_count=retry_count)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.get("/")
async def _list_servers(
    db_session=Depends(get_db_session),
):
    try:
        servers = await list_servers(db_session)
        return [present_server_data(i, db_session) for i in servers]
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.delete("/{name}")
async def _delete_server(name: str, db_session=Depends(get_db_session)):
    try:
        await delete_server(name, db_session)
        return Response(status_code=200, content="Successfully deleted.")
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.patch("/{name}")
async def _update_server(
    name: str, request: CreateServerSchema, db_session=Depends(get_db_session)
):
    try:
        server, retry_count = await update_server(name, request, db_session)
        return present_server_data(server, db_session, retry_count=retry_count)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.post("/health_check/{name}")
async def _check_server_by_name(name: str, db_session=Depends(get_db_session)):
    try:
        server_status, retry_count = await check_server(db_session, name=name)
        return present_server_health_check_data(server_status, retry_count)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@server_router.post("/health_check/")
async def _check_server_by_schema(
    request: CreateServerSchema, db_session=Depends(get_db_session)
):
    try:
        server_status, retry_count = await check_server(db_session, server_data=request)
        return present_server_health_check_data(server_status, retry_count)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)
