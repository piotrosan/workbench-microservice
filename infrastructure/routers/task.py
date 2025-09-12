from typing import Annotated, List, Iterable, Tuple

from fastapi import APIRouter, Path, Request, Body

from domain.flash_card.service import FashCardService
from infrastructure.database.sql.api.initiative import FlashCardDBAPI
from infrastructure.database.sql.models import FlashCard
from infrastructure.database.sql.models.task import Language
from infrastructure.routers.models.request.initiative import (
    CreateFlashCardRequest,
    CreateLanguageRequest
)
from infrastructure.routers.models.response.flash_card import (
    FlashCardResponse,
    LanguageResponse
)
from infrastructure.security.permission.app_admin import check_admin
from infrastructure.security.permission.user import check_user

router = APIRouter(
    prefix="/task",
    tags=["task"],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={404: {"description": "Not found"}},
)


@router.get("/{task_id}", response_model=FlashCardResponse)
async def get_task(
        task_id: Annotated[int, Path()],
        request: Request
):
    return []


@router.post("/", response_model=FlashCardResponse)
async def create_tasks(
        request: Request,
        tasks_data: Annotated[List[CreateFlashCardRequest], Body(...)]
):

    return []


@router.post(
    "/{task_id}",
    response_model=LanguageResponse
)
def update_task(
        request: Request,
        task_id: Annotated[int, Path()],
        task_data: Annotated[CreateFlashCardRequest, Body(...)]
):
    return []


@router.websocket("/show")
async def get_initiative_long(websocket: WebSocket, request: Request):
    dbapi = TestKnowledgeDBAPI()
    service = TestKnowledgeService(dbapi)
    statistics = {}
    test_knowledge_with_content: Iterator[TestKnowledge] = \
        service.get_random_tsts_know_with_cards_for_user(request.user)
    test = next(test_knowledge_with_content)
    flsh_crds: List[FlashCard] = test.flash_cards

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