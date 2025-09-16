import logging
from typing import Iterable, List, cast, Generator, Iterator, Dict, Tuple
from uuid import UUID

from sqlalchemy.engine.result import Result
from typing_extensions import Any

from sqlalchemy import select, text, and_
from sqlalchemy import exc

from infrastructure.database.sql.api.analytics import AnalyticsSQLMixin
from infrastructure.database.sql.api.engine import DBEngine, DBEngineAbstract
from infrastructure.database.sql.api.exception.task_exception import TaskHttpException
from infrastructure.database.sql.models import Initiative, Task, User
from infrastructure.routers.models.request.task import CreateTaskRequest, \
    UpdateTaskRequest

logger = logging.getLogger("root")


class CreateTaskDBAPIMixin(DBEngineAbstract):

    def insert(
            self,
            create_task_request: list[CreateTaskRequest],
    ) -> List[Task]:
        try:
            users = []
            tasks = []
            for ctr in create_task_request:
                i = Initiative(id=ctr.initiative)
                for user in ctr.users:
                    users.append(User(hash_identifier=user))
                tasks.append(
                    Task(
                        title=ctr.title,
                        description=ctr.description,
                        priority=ctr.priority,
                        start_at=ctr.start_at,
                        end_at=ctr.end_at,
                        initiative=i,
                        users=users
                    )
                )
            self.insert_objects(tasks)
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile insert tasks {e}"
            )
            raise TaskHttpException(
                detail="Can not insert tasks",
                status_code=400
            )
        else:
            return tasks


class GetTaskDBAPIMixin(DBEngineAbstract):

    @staticmethod
    def _select_tasks_flex_sql(
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(Task)

        if column:
            tmp_select.column(*[text(col) for col in column])

        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select

    @staticmethod
    def _select_tasks_for_initiatives_or_and__users_sql(
            id_initiatives: List[int] = None,
            uuid_users: List[UUID] = None
    ):
        tmp_select = (select(Task))
        if id_initiatives:
            tmp_select = tmp_select.where(
                cast(
                    "ColumnElement[bool]",
                    Task.initiative_id.in_(id_initiatives)
                )
            )
        if uuid_users:
            tmp_select = tmp_select.where(
                cast(
                    "ColumnElement[bool]",
                    Task.users.in_(uuid_users)
                )
            )
        return tmp_select


    def query_all_tests_knowledge_generator(
            self,
            column: List[str] = None,
            order: List[str] = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_tasks_flex_sql(column, order)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all tasks")
            raise TaskHttpException(
                detail="Can not select tasks",
                status_code=400
            )

    def query_tasks_for_user_and_or_initiative(
            self,
            ids_initiatives: List[int],
            uuid_users: List[UUID],
            page: int = None
    ) -> Result[Any]:
        try:
            return self.query_statement(
                self._select_tasks_for_initiatives_or_and__users_sql(
                    ids_initiatives,
                    uuid_users,
                ),
                page=page
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select tasks")
            raise TaskHttpException(
                detail="Can not select tasks",
                status_code=400
            )


class UpdateTaskDBAPIMixin(DBEngineAbstract):

    def update_tasks(
        self,
        update_task_request: List[UpdateTaskRequest],
    ) -> List[Tuple[int, bool]]:
        result = []
        try:
            for utr in update_task_request:
                result.append((
                    utr.id,
                    self.update_object(
                        Task,
                        utr.model_dump()
                    )
                ))
            return result
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile update Task {e}"
            )
            raise TaskHttpException(
                detail=f"Can not update tasks, result -> {result}",
                status_code=400
            )



class TaskDBAPI(
    CreateTaskDBAPIMixin,
    GetTaskDBAPIMixin,
    UpdateTaskDBAPIMixin,
    AnalyticsSQLMixin,
    DBEngine
):
    pass