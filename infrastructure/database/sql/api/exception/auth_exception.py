from fastapi import HTTPException


class AuthHttpException(HTTPException):
    status_code = 400
    detail = "Problem with work on user permission"