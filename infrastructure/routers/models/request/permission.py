from typing import List
from pydantic import BaseModel

class Role(BaseModel):
    name: str

class UserGroupAndRole(BaseModel):
    name: str
    roles: List[Role]


class FullPermissionDataRequest(BaseModel):
    hash_identifier: str
    user_groups: List[UserGroupAndRole]


class UserAndGroup(BaseModel):
    hash_identifier: str
    name: str

class Group(BaseModel):
    name: str
