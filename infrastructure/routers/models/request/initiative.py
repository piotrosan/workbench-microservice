from typing import List

from pydantic import BaseModel


class CreateInitiativeRequest(BaseModel):
    title: str
    description: str
    custom_notes: str

class CreateInitiativeTypeRequest(BaseModel):
    name: str
    type: str