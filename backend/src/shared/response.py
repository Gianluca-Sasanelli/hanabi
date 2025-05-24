from datetime import datetime
from functools import wraps
from typing import Any, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, Response  # Changed from starlette.responses
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError


class APIResponse(JSONResponse):

    def __init__(
        self,
        request: Request,
        success: bool = True,
        data: Any = None,
        status_code: int = 200,
        headers: Optional[dict[str, str]] = None,
        error: Optional[dict] = None,
    ):
        meta = {
          "timestamp": datetime.now().isoformat(),
        #     "request_id": request.state.request_id,
        #     "user_id": request.state.user_id,
         }
        content = {"success": success, "data": data, "error": error, "meta": meta}
        if not success and status_code < 400:
            status_code = 400

        super().__init__(content=content, status_code=status_code, headers=headers)


def success_response(
    request: Request,
    data: Any = None,
    status_code: int = 200,
) -> APIResponse:

    return APIResponse(success=True, data=data, error=None, status_code=status_code, request=request)


def error_response(
    request: Request,
    code: str,
    message: str,
    details: Any = None,
    status_code: int = 400,
) -> APIResponse:
    error = {"code": code, "message": message, "details": details}

    return APIResponse(success=False, data=None, error=error, status_code=status_code, request=request)


# validating that the response is in the correct format and transform to
# a success response. If there's an errors is catched by the global error handler
def validate_and_encapsulate(response_model: type[BaseModel]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            try:
                if isinstance(result, dict):
                    data = response_model.model_validate(result)
                else:
                    raise ValidationError(
                        f"Response must be a dictionary with data and total count. Got {type(result)}"
                    )

                return success_response(request=kwargs["request"], data=data.model_dump(mode="json"))
            except PydanticValidationError as e:
                print("Got an error with pydantic response validation")
                raise ValidationError(f"Response validation failed: {e!s}")

        return wrapper

    return decorator


class BaseError(HTTPException):
    """Base exception class for application errors with HTTP status codes."""

    error_code = "INTERNAL_SERVER_ERROR"

    def __init__(self, status_code: int = 500, detail: str = "An internal server error occurred"):
        self.error_code = self.__class__.error_code
        super().__init__(status_code=status_code, detail=detail)

    def to_response(self, request: Request) -> APIResponse:
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


# custom errors


class TemplateNotFoundError(BaseError):
    error_code = "TEMPLATE_NOT_FOUND"

    def __init__(self, detail: str = "The requested template was not found"):
        super().__init__(status_code=515, detail=detail)


class DepthNotFoundError(BaseError):
    error_code = "DEPTH_NOT_FOUND"

    def __init__(self, detail: str = "The requested depth was not found"):
        super().__init__(status_code=516, detail=detail)


class ModelEndpointError(BaseError):
    error_code = "MODEL_ENDPOINT_ERROR"

    def __init__(self, detail: str = "Error connecting to the model endpoint"):
        super().__init__(status_code=517, detail=detail)


class AzureStorageError(BaseError):
    error_code = "AZURE_STORAGE_ERROR"

    def __init__(self, detail: str = "Error interacting with Azure Storage"):
        super().__init__(status_code=518, detail=detail)


# Is in the error class so it gets handled by the global error
# handler and not as an usual response
class NoUpdatesError(BaseError):
    error_code = "NO_UPDATES"

    def __init__(self, detail: str = "No updates found"):
        super().__init__(status_code=204, detail=detail)

    def to_response(self, request: Request) -> Response:
        response = Response(status_code=204)
        return response
