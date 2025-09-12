from fastapi import HTTPException


class TokenExpired(HTTPException):
    pass


class TokenDifferentAppId(HTTPException):
    pass


class TokenRequestGetter(HTTPException):
    pass