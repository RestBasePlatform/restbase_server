from typing import List

from models import AccessObjectType
from models import AccessOwnerType
from sqlalchemy.orm import Session


async def get_object_types_list(object_type: str, db_session: Session) -> List[str]:
    type_object_dict = {"object": AccessObjectType, "owner": AccessOwnerType}

    if object_type not in type_object_dict:
        raise ValueError("'object_type' must be in ['object', 'owner']")

    return [i.name for i in db_session.query(type_object_dict[object_type]).all()]
