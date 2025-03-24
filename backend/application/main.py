from logging import getLogger
from time import strftime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


from .api.main import api_router
from .api.deps import (
    redis_dependency,
)
from .core.config import settings

logger = getLogger(__name__)


@asynccontextmanager
async def func_lifespan(app: FastAPI) -> object:
    """
    func_lifespan Allows to run code when the application starts and stops.

    Function to run code when the application starts and stops.

    Args:
        app (FastAPI): FastAPI instance
    """

    try:
        logger.info(strftime("%Y-%m-%d %H:%M:%S") + " - App started")
        await redis_dependency.init()
        yield
    finally:
        await redis_dependency.redis.close()
        logger.info(strftime("%Y-%m-%d %H:%M:%S") + " - App stopped")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG,
    lifespan=func_lifespan,
    # Generate unique id for each route
    generate_unique_id_function=lambda route: f"{route.tags[0]}-{route.name}",
    dependencies=[],
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router)
