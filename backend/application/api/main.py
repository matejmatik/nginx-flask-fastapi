from fastapi import APIRouter

from .routes import info
from ..models import Tags

api_router = APIRouter()
api_router.include_router(info.router, prefix="/info", tags=[Tags.INFO])
