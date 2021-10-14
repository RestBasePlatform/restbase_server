from controller.v1.users import create_group
from controller.v1.users import create_user
from controller.v1.users import delete_user
from controller.v1.users import edit_user
from controller.v1.users import get_group
from controller.v1.users import get_group_names
from controller.v1.users import add_user_to_group
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from models.utils import get_db_session
from views.v1.user_group import get_group_answer
from views.v1.user_group import successful_user_answer

from .schemas import CreateGroupSchema
from .schemas import CreateUserSchema
from .schemas import EditUserSchema

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/")
async def _create_user(user: CreateUserSchema, db_session=Depends(get_db_session)):
    try:
        user = await create_user(user, db_session)
        return successful_user_answer(user)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@user_router.patch("/{user_id}")
async def _edit_user(
    user_id: int, user: EditUserSchema, db_session=Depends(get_db_session)
):
    try:
        user = await edit_user(user_id, user, db_session)
        return successful_user_answer(user)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@user_router.delete("/{user_id}")
async def _delete_user(user_id: int, db_session=Depends(get_db_session)):
    try:
        await delete_user(user_id, db_session)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


group_router = APIRouter(prefix="/group", tags=["Groups"])


@group_router.post("/")
async def _create_group(group: CreateGroupSchema, db_session=Depends(get_db_session)):
    try:
        group = await create_group(
            group.name, group.user_list, db_session, group.comment
        )
        return get_group_answer(group)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@group_router.get("/")
async def _list_groups(db_session=Depends(get_db_session)):
    try:
        return {"groups": await get_group_names(db_session)}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@group_router.get("/{group_name}")
async def get_group_data(group_name: str, db_session=Depends(get_db_session)):
    try:
        return get_group_answer(await get_group(group_name, db_session))
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@group_router.post("/{group_name}/add_user/{user_id}")
async def _add_user_to_group(group_name: str, user_id: int, db_session=Depends(get_db_session)):
    try:
        await add_user_to_group(user_id, "name", group_name, db_session)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)
