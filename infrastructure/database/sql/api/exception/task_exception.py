from fastapi import HTTPException


class TaskHttpException(HTTPException):
    status_code = 400
    detail = "Problem with work on test knowledge"