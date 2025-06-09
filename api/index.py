import logging


from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers.card_routers import router as card_router
from api.routers.login_router import router as login_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hanabi Server",
        description="API for hyanabi application",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "https://*.vercel.app"],
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions."""
        logger.error(f"Unexpected error: {exc!s}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {exc!s}")

    app.include_router(card_router, prefix="/api")
    app.include_router(login_router, prefix="/api")
    return app


app = create_app()
