from typing import List

from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

from infrastructure.database.sql.models.task import FlashCard


class KnowledgeResponse(BaseModel):
    id: int = None
    planned_start: datetime = None
    user_identifier: str = None
    create_at: datetime = None
    updated_at: datetime = None
    flash_cards: List[dict] = None
