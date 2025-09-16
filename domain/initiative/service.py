from typing import List, Any, Sequence

from sqlalchemy.engine.result import Result, Row, _TP

from infrastructure.database.sql.api.initiative import InitiativeDBAPI
from infrastructure.database.sql.models import Initiative, InitiativeType
from infrastructure.routers.models.request.initiative import \
    CreateInitiativeRequest, CreateInitiativeTypeRequest, \
    UpdateInitiativeRequest, UpdateInitiativeTypeRequest


class InitiativeService:

    def __init__(self):
        self.ci_db_api = InitiativeDBAPI()

    def create_initiative(
            self,
            create_initiative_request: List[CreateInitiativeRequest]
    ) -> List[Initiative]:
        return list(self.ci_db_api.insert(create_initiative_request))

    def create_initiative_type(
            self,
            create_initiative_type_request: List[CreateInitiativeTypeRequest]
    ) -> List[InitiativeType]:
        return list(
            self.ci_db_api.insert_initiative_type(
                create_initiative_type_request
            )
        )

    def update_initiative(
            self,
            update_initiative_request: List[UpdateInitiativeRequest]
    ):
        for initiative in update_initiative_request:
            self.ci_db_api.update_object(
                Initiative,
                initiative.model_dump()
            )

    def update_initiative_type(
            self,
            update_initiative_type_request: List[UpdateInitiativeTypeRequest]
    ):
        for initiative_type in update_initiative_type_request:
            self.ci_db_api.update_object(
                InitiativeType,
                initiative_type.model_dump()
            )

    def get_initiative_for_account(
            self,
            id_account: int,
            page: int
    ) -> Sequence[Row[_TP]]:
        result: Result[Any] =  self.ci_db_api.query_initiatives_for_account_generator(
            id_account,
            page
        )
        return result.fetchall()

    def get_initiatives_with_task_from_ids(
            self,
            ids_initiative: List[int],
            page: int = None
    ) -> Sequence[Row[_TP]]:
        result: Result[Any] = self.ci_db_api.query_initiatives_with_task_from_ids(
            ids_initiative,
            page
        )
        return result.fetchall()