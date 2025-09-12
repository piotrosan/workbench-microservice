from pydantic import BaseModel

from infrastructure.routers.models.request.permission import \
    FullPermissionDataRequest


class UserPermissionResponse(FullPermissionDataRequest):
    pass
