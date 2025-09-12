from fastapi import HTTPException


class RawStatementHttpException(HTTPException):
    status_code = 400
    detail = "Problem with raw statement"