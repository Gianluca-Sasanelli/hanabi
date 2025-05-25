import logging


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.card_routers import router as card_router

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
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(card_router)
    return app


app = create_app()
