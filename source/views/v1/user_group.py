from fastapi import Response
from models.user import Group
from models.utils import get_user_list_names_by_ids


def successful_user_answer(user_id: int):
    return Response(content=f"User created. ID: {user_id}", status_code=200)


def successful_group_answer(group_id: int, user_list: str):
    return (
        Response(
            content=f"Group created. ID: {group_id}. User id's: {user_list}",
            status_code=200,
        )
        if user_list
        else Response(content=f"Group created. ID: {group_id}.")
    )


def get_group_answer(group: Group) -> dict:
    return {
        "id": group.id,
        "name": group.name,
        "comment": group.comment,
        "users": get_user_list_names_by_ids(group.user_list),
    }
