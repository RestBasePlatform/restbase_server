from controller.v1.users import create_group
from controller.v1.users import create_user
from fastapi import APIRouter
from fastapi import Depends
from models.utils import get_db_session
from views.v1.user_group import successful_group_answer
from views.v1.user_group import successful_user_answer

from .schemas import CreateGroupSchema
from .schemas import CreateUserSchema

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/")
async def _create_user(user: CreateUserSchema, db_session=Depends(get_db_session)):
    user_id = await create_user(
        user.username, user.password, user.group_list, db_session, user.comment
    )
    return successful_user_answer(user_id)


group_router = APIRouter(prefix="/group", tags=["Groups"])


@group_router.post("/")
async def _create_group(group: CreateGroupSchema, db_session=Depends(get_db_session)):
    group = await create_group(group.name, group.user_list, db_session, group.comment)
    return successful_group_answer(group.id, group.user_list)
