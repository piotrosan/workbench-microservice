from typing import List

from infrastructure.database.sql.models import UserGroup
from infrastructure.database.sql.models.auth import User
from infrastructure.security.permission.exception.auth import \
    PermissionHTTPException


def check_user(user: User) -> None:
    ugs: List[UserGroup] = user.user_groups

    result = [
        ug.name == 'user'
        for ug in ugs
    ]
    if all(result):
        raise PermissionHTTPException(
            status_code=400,
            detail='Do not have simple permission'
        )
