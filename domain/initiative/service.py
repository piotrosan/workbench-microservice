from typing import List

from infrastructure.database.sql.api.initiative import InitiativeDBAPI
from infrastructure.routers.models.request.initiative import \
    CreateInitiativeRequest, CreateInitiativeTypeRequest


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
            update_initiative_request: List[CreateInitiativeRequest]
    ):
