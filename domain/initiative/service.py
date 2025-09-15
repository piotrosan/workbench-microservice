from typing import List

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
    ):
        self.ci_db_api.insert(create_initiative_request)

    def create_initiative_type(
            self,
            create_initiative_type_request: List[CreateInitiativeTypeRequest]
    ):
        self.ci_db_api.insert_initiative_type(create_initiative_type_request)


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


    def get_initiative_for_account(self, id_account: int, page: int):
        return self.ci_db_api.query_initiatives_for_account_generator(
            id_account,
            page
        )