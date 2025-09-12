from typing import Annotated, Iterator, Tuple, List
from fastapi import APIRouter, Path, Request, Body, WebSocket

from domain.initiative.service import InitiativeService
from infrastructure.database.sql.models.task import Task
from infrastructure.database.sql.models.initiative import Initiative
from infrastructure.routers.models.request.generic import GenericResponse
from infrastructure.routers.models.request.initiative import \
    CreateInitiativeRequest, CreateInitiativeTypeRequest
from infrastructure.routers.models.request.knowledge import CreateKnowledgeRequest
from infrastructure.routers.models.response.knowledge import KnowledgeResponse
from infrastructure.security.permission.account_admin import check_account_admin
from infrastructure.security.permission.app_admin import check_admin

router = APIRouter(
    prefix="/initiative",
    tags=["initiative"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/{initiative_id}",
    response_model=List[KnowledgeResponse]
)
async def get_initiative(
        initiative_id: Annotated[int, Path()],
        request: Request
) -> List[KnowledgeResponse]:
    return []


@router.post("/", response_model=KnowledgeResponse)
async def create_initiative(
        create_initiative_request: Annotated[
            List[CreateInitiativeRequest], Body(...)],
        request: Request
):
    service = InitiativeService()
    service.create_initiative(create_initiative_request)
    return KnowledgeResponse()


@router.post("/", response_model=KnowledgeResponse)
async def create_initiative_type(
        create_initiative_type_request: Annotated[
            List[CreateInitiativeTypeRequest], Body(...)],
        request: Request
):
    service = InitiativeService()
    service.create_initiative_type(create_initiative_type_request)
    return KnowledgeResponse()


@router.patch("/", response_model=KnowledgeResponse)
async def update_initiative(
        initiative_data: Annotated[CreateKnowledgeRequest, Body(...)],
        request: Request
):
    return KnowledgeResponse()


@router.websocket("/show")
async def get_initiative_long(websocket: WebSocket, request: Request):

    await websocket.accept()
    while flsh_crds:
        await websocket.send_json(flsh_crds.pop(0).__dict__)
        result = await websocket.receive_json()
        if result['correct']:
            statistics[result['word']] = True
        else:
            statistics[result['word']] = False

    await websocket.send_text('Test have been finish')
    return GenericResponse(message='object have been updated')