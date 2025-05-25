import logging


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.card_routers import router as card_router

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
    app.include_router(card_router, prefix = "/api")
    return app


app = create_app()
