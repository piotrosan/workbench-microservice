from typing import List
from uuid import UUID

from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class CreateTaskRequest(BaseModel):
    start_at: datetime = None
    end_at: datetime = None
    title: str
    description: str
    priority: int
    initiative: int
    users: list[UUID]

class UpdateTaskRequest(BaseModel):
    id: int
    start_at: datetime = None
    end_at: datetime = None
    title: str = None
    description: str = None
    priority: int = None
    initiative: int = None
