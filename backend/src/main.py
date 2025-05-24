import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.shared.response import BaseError, ProcessingError
from src.routers.game_starter import router as game_starter_router
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="NesAI API",
        description="API for NesAI application",
        version="0.2.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(BaseError)
    async def base_error_handler(request: Request, exc: BaseError):
        """Handle all custom BaseError exceptions."""
        logger.error(f"BaseError: {exc.detail}")
        return exc.to_response(request)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions."""
        logger.error(f"Unexpected error: {exc!s}", exc_info=True)
        error = ProcessingError(f"An unexpected error occurred: {exc!s}")
        return error.to_response(request)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors from Pydantic models."""
        logger.error(f"Validation error: {exc!s}")
        from src.shared.response import ValidationError

        error = ValidationError(f"Validation error: {exc.errors()!s}")
        return error.to_response(request)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    app.include_router(game_starter_router)

    return app


app = create_app()
