from fastapi.responses import JSONResponse
from models.user import Group
from models.user import User
from models.utils import get_user_list_names_by_ids


def successful_user_answer(user: User):
    return JSONResponse(
        content={"id": user.id, "name": user.get_username(), "comment": user.comment},
        status_code=200,
    )


def successful_group_answer(group_id: int, user_list: str):
    return (
        JSONResponse(
            content=f"Group created. ID: {group_id}. User id's: {user_list}",
            status_code=200,
        )
        if user_list
        else JSONResponse(content=f"Group created. ID: {group_id}.")
    )


def get_group_answer(group: Group) -> dict:
    return {
        "id": group.id,
        "name": group.name,
        "comment": group.comment,
        "users": get_user_list_names_by_ids(group.user_list),
    }
