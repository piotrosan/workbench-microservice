from typing import List

from pydantic import BaseModel


class CreateInitiativeRequest(BaseModel):
    title: str
    description: str
    custom_notes: str


class UpdateInitiativeRequest(BaseModel):
    id: int
    title: str
    description: str
    custom_notes: str


class CreateInitiativeTypeRequest(BaseModel):
    name: str
    type: str


class UpdateInitiativeTypeRequest(BaseModel):
    id: int
    name: str
    type: str