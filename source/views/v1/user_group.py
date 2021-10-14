from fastapi.responses import JSONResponse
from models.user import Group
from models.user import User


def successful_user_answer(user: User):
    return JSONResponse(
        content={"id": user.id, "name": user.get_user_data().username, "comment": user.comment},
        status_code=200,
    )


def get_group_answer(group: Group) -> dict:
    return {
        "id": group.id,
        "name": group.name,
        "comment": group.comment,
        "users": group.user_list,
    }
