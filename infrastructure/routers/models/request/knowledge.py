from typing import List

from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class CreateKnowledgeRequest(BaseModel):
    planned_start: datetime = None
    user_identifier: str
    list_flash_cards: List[int]


class UpdateKnowledgeRequest(BaseModel):
    id: int
    planned_start: datetime = None
    user_identifier: str = None
