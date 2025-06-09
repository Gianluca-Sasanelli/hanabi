from datetime import datetime
from functools import wraps
from typing import Any, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, Response  # Changed from starlette.responses


def success_response(
    request: Request,
    data: Any = None,
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(content={"data": data})

def error_response(
    request: Request,
    code: str,
    message: str,
    details: Any = None,
    status_code: int = 400,
) -> JSONResponse:
    error = {"code": code, "message": message, "details": details}

    return JSONResponse(content={"error": error}, status_code=status_code)



class BaseError(HTTPException):
    """Base exception class for application errors with HTTP status codes."""

    error_code = "INTERNAL_SERVER_ERROR"

    def __init__(self, status_code: int = 500, detail: str = "An internal server error occurred"):
        self.error_code = self.__class__.error_code
        super().__init__(status_code=status_code, detail=detail)

    def to_response(self, request: Request) -> JSONResponse:
        return error_response(code=self.error_code, message=self.detail, status_code=self.status_code, request=request)


class AuthenticationError(BaseError):
    error_code = "AUTHENTICATION_ERROR"

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=401, detail=detail)


class AuthorizationError(BaseError):
    error_code = "AUTHORIZATION_ERROR"

    def __init__(self, detail: str = "You don't have permission to access this resource"):
        super().__init__(status_code=403, detail=detail)


class NotFoundError(BaseError):
    error_code = "NOT_FOUND"

    def __init__(self, detail: str = "The requested resource was not found"):
        super().__init__(status_code=404, detail=detail)


class ConflictError(BaseError):
    error_code = "CONFLICT"

    def __init__(self, detail: str = "The resource already exists or conflicts with current state"):
        super().__init__(status_code=409, detail=detail)


class ValidationError(BaseError):
    error_code = "VALIDATION_ERROR"

    def __init__(self, detail: str = "Invalid input data"):
        super().__init__(status_code=422, detail=detail)


class ProcessingError(BaseError):
    error_code = "PROCESSING_ERROR"

    def __init__(self, detail: str = "Error processing the request"):
        super().__init__(status_code=500, detail=detail)

