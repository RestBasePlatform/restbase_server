from controller.v1.users import create_group
from controller.v1.users import create_user
from controller.v1.users import delete_user
from controller.v1.users import get_group
from controller.v1.users import get_group_names
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from models.utils import get_db_session
from views.v1.user_group import get_group_answer
from views.v1.user_group import successful_group_answer
from views.v1.user_group import successful_user_answer

from .schemas import CreateGroupSchema
from .schemas import CreateUserSchema

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/")
async def _create_user(user: CreateUserSchema, db_session=Depends(get_db_session)):
    try:
        user_id = await create_user(
            user.username, user.password, user.group_list, db_session, user.comment
        )
        return successful_user_answer(user_id)
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
        return successful_group_answer(group.id, group.user_list)
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
