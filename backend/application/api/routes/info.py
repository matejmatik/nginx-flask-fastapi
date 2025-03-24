from typing import Any

from fastapi import APIRouter, Depends, status  # noqa

from ...core import settings
from ...models import FastApiMsgOut


router = APIRouter()


@router.get(
    settings.BACKEND_HEALTH_CHECK_PATH.replace("/info", ""),
    summary="Service is used to check the health of the application.",
)
async def health_check() -> bool:
    return True


@router.get(
    "/ping",
    summary="Service is used to check the health of the application.",
    response_model=FastApiMsgOut,
    status_code=status.HTTP_200_OK,
)
async def get_ping() -> Any:
    """
    # O metodi

    GET metoda `ping` je namenjena preverjanju delovanja strežnika.

    Vrne `pong` kot potrditev delovanja strežnika.
    """
    # gc.collect() # garbage collection

    return {
        "data": {"ping": "pong"},
        "detail": {
            "msg": "Storitev deluje pravilno.",
            "category": "success",
        },
    }


@router.get(
    "/description",
    summary="Service is used to get the description of the application.",
    response_model=FastApiMsgOut,
    status_code=status.HTTP_200_OK,
)
async def get_description() -> Any:
    """
    # O metodi

    GET metoda `description` je namenjena pridobivanju opisa storitve.

    Vrne opis storitve.
    """
    return {
        "data": {
            "project_info": {
                "name": settings.PROJECT_NAME,
                "version": settings.PROJECT_VERSION,
                "description": settings.DESCRIPTION,
                "environment": settings.ENVIRONMENT,
            },
            "redis": {
                "host": settings.REDIS_HOST,
                "port": settings.REDIS_PORT,
                "uri": settings.REDIS_URL,
            },
        },
        "detail": {
            "msg": "Opis storitve.",
            "category": "success",
        },
    }
