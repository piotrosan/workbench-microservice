from typing import List, Any, Sequence

from sqlalchemy.engine.result import Result, Row, _TP

from infrastructure.database.sql.api.user_permission_database import \
    UserPermissionDBAPI
from infrastructure.database.sql.models.auth import User, UserGroup, Role
from infrastructure.routers.models.request.permission import \
    FullPermissionDataRequest, UserGroupAndRole, UserAndGroup, Group


class BaseAuthService:
    def __init__(self, infrastructure_db: UserPermissionDBAPI):
        self.infrastructure_db = infrastructure_db


class UserService(BaseAuthService):

    def create_user(self, hash_identifier: str) -> User:
        return self.infrastructure_db.insert_user(hash_identifier)


    def get_user_with_permission(
            self,
            hash_identifier: str
    ) -> Sequence[Row[_TP]]:
        result: Result[Any] = self.infrastructure_db.query_user_with_permission(
                hash_identifier
            )
        return result.fetchall()


class GroupRoleService(BaseAuthService):

    def create_groups_and_roles(
            self,
            groups_and_role: List[UserGroupAndRole]
    ) -> List[UserGroup]:
        return self.infrastructure_db.insert_group_and_role(
            groups_and_role
        )

    def add_user_to_group(
            self,
            user_and_group: UserAndGroup
    ) -> int:
        result_ug: Result[Any]  = self.infrastructure_db.query_groups_for_names(
            [user_and_group.name]
        )
        ug: List[UserGroup] = [ug[0] for ug in result_ug.all()]

        result_user: Result[Any] = self.infrastructure_db.query_user_from_hash(
            user_and_group.hash_identifier)
        users: List[User] = [u[0] for u in result_user.all()]

        amount_of_added = self.infrastructure_db.add_user_to_group(ug, users[0])
        return amount_of_added

    def update_group_from_id(
            self,
            group_id: int,
            new_name: str
    ) -> bool:
        return self.infrastructure_db.update_group_from_id(
            group_id, new_name)

    def update_role_from_id(
            self,
            role_id: int,
            new_name: str
    ) -> bool:
        return self.infrastructure_db.update_role_from_id(
            role_id, new_name)

class AuthService(
    UserService,
    GroupRoleService,
    BaseAuthService
):
    def create_user_permission(
            self,
            full_permission_data: FullPermissionDataRequest
    ) -> User:
        return self.infrastructure_db.insert(
            full_permission_data.model_dump(mode='Python')
        )
