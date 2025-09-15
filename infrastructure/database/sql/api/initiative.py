import logging
from encodings.aliases import aliases
from typing import Iterable, List, cast, Iterator

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.util import aliased
from typing_extensions import Any

from sqlalchemy import select, text
from sqlalchemy import exc

from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.models import User
from infrastructure.database.sql.models.initiative import Initiative, \
    InitiativeType

from infrastructure.database.sql.api.exception.initiative_exception import InitiativeHttpException
from infrastructure.database.sql.models.task import Task
from infrastructure.routers.models.request.initiative import (
    CreateInitiativeRequest, CreateInitiativeTypeRequest
)


logger = logging.getLogger("root")


class CreateInitiativeDBAPI(DBEngineAbstract):

    def insert(
            self,
            create_initiative_request: List[CreateInitiativeRequest],
    ) -> Iterable[Initiative]:
        try:

            return self.insert_objects([
                Initiative(**cir.model_dump(mode='python'))
                for cir in create_initiative_request
            ])
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile insert initiative -> {e}")
            raise InitiativeHttpException(
                detail="Can not insert initiative",
                status_code=400
            )

    def insert_initiative_type(
            self,
            create_initiative_type_request: List[CreateInitiativeTypeRequest],
    ) -> Iterable[CreateInitiativeTypeRequest]:
        try:

            return self.insert_objects([
                InitiativeType(**citr.model_dump(mode='python'))
                for citr in create_initiative_type_request
            ])
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile insert initiative type -> {e}")
            raise InitiativeHttpException(
                detail="Can not insert initiative type",
                status_code=400
            )


class GetInitiativeDBAPI(DBEngineAbstract):

    @staticmethod
    def _select_all_initiative_for_sql(
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(Initiative)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select


    @staticmethod
    def _select_initiatives_for_account(id_account: int):
        user_table = aliased(User)
        try:
            return select(Initiative).where(
                cast(
                    "ColumnElement[bool]",
                    Initiative.users.any(user_table.account_id==id_account)
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select initiative from id {e}")
            raise InitiativeHttpException(
                detail="Can not select initiative",
                status_code=400
            )


    @staticmethod
    def _select_initiative_with_all_tasks(ids_initiative: List[int]):
        try:
            return select(Initiative).where(
                cast(
                    "ColumnElement[bool]",
                    Initiative.id.in_(ids_initiative)
                )
            ).options(
                    joinedload(Initiative.tasks)
                    .joinedload(Initiative.type)
                )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select Initiative with tasks {e}")
            raise InitiativeHttpException(
                detail="Can not select initiative with task",
                status_code=400
            )

    def query_all_initiatives_flex_generator(
            self,
            column: List[str] = None,
            order: List[str] = None,
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_initiative_for_sql(column, order),
                Initiative,
                page
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all flasgh")
            raise InitiativeHttpException(
                detail="Can not select flash cards with attchments",
                status_code=400
            )

    def query_initiatives_with_task_from_ids(
            self,
            ids_initiative: List[int],
            page: int = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                    self._select_initiative_with_all_tasks(ids_initiative),
                    Initiative,
                    page
                )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select initiatives {ids_initiative} -> {e}"
            )
            raise InitiativeHttpException(
                detail=f"Can not select initiatives {ids_initiative}",
                status_code=400
            )

    def query_initiatives_for_account_generator(
            self,
            id_account: int,
            page_id: int
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                    self._select_initiatives_for_account(id_account),
                    Initiative,
                    page_id
            )
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select flash cards -> {e}"
            )
            raise InitiativeHttpException(
                detail=f"Can not select flash cards",
                status_code=400
            )


class UpdateInitiativeDBAPI(DBEngineAbstract):
    pass


class InitiativeDBAPI(
    CreateInitiativeDBAPI,
    GetInitiativeDBAPI,
    UpdateInitiativeDBAPI,
    DBEngine
):
    pass