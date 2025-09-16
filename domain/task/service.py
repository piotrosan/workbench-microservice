from typing import List, Any, Sequence
from uuid import UUID

from sqlalchemy.engine.result import Result, Row, _TP as _TP

from infrastructure.database.sql.api.task import TaskDBAPI
from infrastructure.routers.models.request.task import CreateTaskRequest, \
    UpdateTaskRequest


class InitiativeService:

    def __init__(self):
        self.ci_db_api = TaskDBAPI()


    def create_tasks(self, create_task_request: List[CreateTaskRequest]):
        return self.ci_db_api.insert_objects(create_task_request)


    def update_tasks(self, update_task_request: List[UpdateTaskRequest]):
        return self.ci_db_api.update_tasks(update_task_request)


    def get_tasks_for_initiatives_or_and_users(
            self,
            ids_initiatives: List[int],
            uuid_users: List[UUID],
            page: int = None
    ) -> Sequence[Row[_TP]]:
        result: Result[Any] =  self.ci_db_api.query_tasks_for_user_and_or_initiative(
            ids_initiatives,
            uuid_users,
            page
        )
        return result.fetchall()