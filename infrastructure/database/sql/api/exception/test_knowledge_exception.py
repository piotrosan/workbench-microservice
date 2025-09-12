from fastapi import HTTPException


class TestKnowledgeHttpException(HTTPException):
    status_code = 400
    detail = "Problem with work on test knowledge"