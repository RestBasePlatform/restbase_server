from fastapi import APIRouter

from .installation import installation_router
from .submodule import submodule_router
from .user_group import group_router
from .user_group import user_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(submodule_router)
v1_router.include_router(installation_router)
v1_router.include_router(user_router)
v1_router.include_router(group_router)
