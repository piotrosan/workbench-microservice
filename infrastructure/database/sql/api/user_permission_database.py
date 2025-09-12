import logging
from typing import Iterable, List, cast, Generator, Iterator, Tuple

from sqlalchemy.engine.result import Result
from sqlalchemy.orm import contains_eager, joinedload
from typing_extensions import Any

from sqlalchemy import select, text, and_
from sqlalchemy import exc

from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.api.exception.auth_exception import \
    AuthHttpException
from infrastructure.database.sql.models import UserGroup
from infrastructure.database.sql.models.auth import User, Role, AssociationUserGroupUser
from infrastructure.database.sql.api.exception.test_knowledge_exception import TestKnowledgeHttpException
from infrastructure.routers.models.request.permission import UserGroupAndRole

logger = logging.getLogger("root")


class CreateUserPermissionsDBAPIMixin(DBEngineAbstract):

    def insert(
            self,
            full_permission_data: dict
    ) -> User:
        try:
            user = User(
                hash_identifier=full_permission_data['hash_identifier']
            )

            groups = []
            for g in full_permission_data['user_groups']:
                ug = UserGroup(name=g['name'])
                list_roles = []
                for r in g['roles']:
                    ro = Role(
                        name=r['name'],
                        user_group_id=ug
                    )
                    list_roles.append(ro)
                ug.roles = list_roles
                groups.append(ug)

            associations = [
                AssociationUserGroupUser(user=user, user_group=g)
                for g in groups
            ]

            self.insert_objects([user] + associations)
            return user
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert user permission -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert user permission",
                status_code=400
            )

    def insert_group_and_role(
            self,
            groups_and_role: List[UserGroupAndRole],
    ) -> List[UserGroup]:
        try:
            groups = []
            for g in groups_and_role:
                ug = UserGroup(name=g.name)
                list_roles = []
                for r in g.roles:
                    ro = Role(
                        name=r.name,
                        user_group_id=ug
                    )
                    list_roles.append(ro)
                ug.roles = list_roles
                groups.append(ug)

            self.insert_objects(groups)
            return groups

        except exc.SQLAlchemyError as e:
            g: UserGroupAndRole
            logger.critical(
                f"Problem wile insert user group with role -> {e}"
                f"data -> {[
                    g.model_dump(mode='python') for g in groups_and_role
                ]}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert user group with role",
                status_code=400
            )


    def insert_user(
            self,
            hash_identifier: str,
    ) -> User:
        try:
            user: User = User(hash_identifier=hash_identifier)
            self.insert_objects([user])
            return user
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert user -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not insert user group with role",
                status_code=400
            )


    def add_user_to_group(
            self,
            groups_and_roles: List[UserGroup],
            user: User
    ) -> int:
        try:
            associations = [
                AssociationUserGroupUser(user=user, user_group=g[0])
                for g in groups_and_roles
            ]

            self.insert_objects(associations)
            return len(associations)
        except exc.SQLAlchemyError as e:
            g: UserGroupAndRole
            logger.critical(
                f"Problem wile add user to group -> {e}"
                f" -> {[
                    g.model_dump(mode='python') for g in groups_and_roles
                ]}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not add user to group",
                status_code=400
            )
        except IndexError as e:
            logger.critical(
                f"Problem wile add user to group, groups is empty -> {e}"
            )
            raise TestKnowledgeHttpException(
                detail="Can not add user to group",
                status_code=400
            )

class GetUserPermissionDBAPIMixin(DBEngineAbstract):
    def _select_all_test_knowledge_sql(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(User)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select

    def _select_user_with_permisison_sql(
            self,
            hash_identifier: str
    ):
        return (
            select(User)
            .join_from(
                User,
                UserGroup,
                User.user_groups.any(
                    and_(
                        AssociationUserGroupUser.left_user_id == User.id,
                        AssociationUserGroupUser.right_user_group_id == UserGroup.id,
                        User.hash_identifier == hash_identifier
                    )
                )
            )
            .join_from(
                UserGroup,
                Role,
                and_(
                    UserGroup.id == Role.user_group_id
                )
            )
            .where(
                cast(
                    "ColumnElement[bool]",
                    User.hash_identifier == hash_identifier
                )
            )
            .options(joinedload(User.user_groups).joinedload(UserGroup.roles))
        )

    def query_user_with_permission_paginate_generator(
            self,
            hash_identifier: str,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_user_with_permisison_sql(hash_identifier),
                page=page
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                "Problem wile select query"
                f" user with permission - {e}")
            raise AuthHttpException(
                detail="Can not select user",
                status_code=400
            )


    def _select_user_groups_for_names_sql(
            self,
            groups: List[str]
    ):
        sql = (
            select(UserGroup)
            .where(UserGroup.name.in_(groups))
        )
        return sql


    def query_groups_for_names(
            self,
            groups: list[str],
            page=None
    ) -> List[UserGroup]:
        try:
            return list(self.query_statement(
                self._select_user_groups_for_names_sql(group),
                page=page
            ))
        except exc.SQLAlchemyError as e:
            logger.critical(
                "Problem wile select query"
                f" user groups - {e}")
            raise AuthHttpException(
                detail="Can not select user groups",
                status_code=400
            )


    def _select_user_for_hash_sql(
            self,
            hash_identifier: str
    ):
        return (
            select(User)
            .where(
                cast(
                    "ColumnElement[bool]",
                    User.hash_identifier == hash_identifier
                )
            )
        )

    def query_user_from_hash(self, hash_identifier: str, page=None) -> Any:
        try:
            users: Tuple[User] = next(self.query_statement(
                self._select_user_for_hash_sql(hash_identifier),
                page=page
            ))
            return users[0]
        except exc.SQLAlchemyError as e:
            logger.critical(
                "Problem wile select query"
                f" user - {e}")
            raise AuthHttpException(
                detail="Can not select user",
                status_code=400
            )
        except IndexError as e:
            logger.critical(
                f"Empty selected user, hash ->{hash_identifier}, exec -> {e}"
            )
            raise AuthHttpException(
                detail="Can not select user",
                status_code=400
            )


class UpdateUserPermissionDBAPIMixin(DBEngineAbstract):
    def update_group_from_id(
            self,
            group_id: int,
            new_name: str
    ) -> bool:
        try:
            return self.update_object(
                UserGroup,
                [{'id': group_id, 'name': new_name}]
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                "Problem wile update user group"
                f" - {e}")
            raise AuthHttpException(
                detail="Can not update user group",
                status_code=400
            )

    def update_role_from_id(
            self,
            role_id: int,
            new_name: str
    ) -> bool:
        try:
            return self.update_object(
                Role,
                [{'id': role_id, 'name': new_name}]
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                "Problem wile update"
                f" role - {e}")
            raise AuthHttpException(
                detail="Can not update role",
                status_code=400
            )


class UserPermissionDBAPI(
    CreateUserPermissionsDBAPIMixin,
    GetUserPermissionDBAPIMixin,
    UpdateUserPermissionDBAPIMixin,
    DBEngine
):
    pass