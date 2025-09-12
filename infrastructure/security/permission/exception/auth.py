from fastapi import HTTPException


class PermissionHTTPException(HTTPException):
    detail = 'Do not have permission'