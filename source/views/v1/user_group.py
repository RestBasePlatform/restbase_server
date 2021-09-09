from fastapi import Response


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
