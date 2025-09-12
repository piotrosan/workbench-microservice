from fastapi import HTTPException


class InitiativeHttpException(HTTPException):
    status_code = 400
    detail = "Problem with work on initiative"