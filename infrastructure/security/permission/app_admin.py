from typing import List

from infrastructure.database.sql.models import UserGroup
from infrastructure.database.sql.models.auth import User


def check_admin(user: User) -> bool:
    ugs: List[UserGroup] = user.user_groups

    result = [
        ug.name == 'admin'
        for ug in ugs
    ]
    return all(result)


def check_role_modify(user: User) -> bool:
    ugs: List[UserGroup] = user.user_groups

    result = [
        ug.name == 'modify'
        for ug in ugs
    ]
    return all(result)


def check_role_delete(user: User) -> bool:
    ugs: List[UserGroup] = user.user_groups

    result = [
        ug.name == 'delete'
        for ug in ugs
    ]
    return all(result)

