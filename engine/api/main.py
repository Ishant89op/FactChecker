import asyncio
import logging
import sys

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.settings import settings
from api.firebase import init_firebase
from api.middleware import APIKeyMiddleware
from api.routes import router as verify_router
from api.history import router as history_router
from api.job_store import job_store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FactChecker API",
    description="Model 3 fact-verification backend with Playwright scraper + dual LLM reasoning",
    version="3.0.0",
)


@app.on_event("startup")
async def startup():
    logger.info("Loading secrets...")
    settings.load()

    logger.info("Initializing Firebase...")
    init_firebase(
        service_account_json=settings.firebase_service_account,
        service_account_path=settings.firebase_service_account_path,
    )

    # Start periodic cleanup task
    asyncio.create_task(_cleanup_loop())

    logger.info("FactChecker API v3 ready")


async def _cleanup_loop():
    """Runs every 30 minutes to clean up expired in-memory jobs."""
    while True:
        await asyncio.sleep(1800)
        await job_store.cleanup_old_jobs()


# CORS
origins = [o.strip() for o in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key gate
app.add_middleware(APIKeyMiddleware)

# Routers
app.include_router(verify_router)
app.include_router(history_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
