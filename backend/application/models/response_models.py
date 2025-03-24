from enum import Enum

from pydantic import BaseModel


class MessageCategory(str, Enum):
    """Enum for message category."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    MESSAGE = "message"


class Detail(BaseModel):
    msg: str
    category: MessageCategory


class FastApiMsgOut(BaseModel):
    """Base model for FastApi messages."""

    data: dict
    detail: Detail


class FastApiMsgOutListDict(BaseModel):
    """Base model for FastApi messages."""

    data: list[dict]
    detail: Detail
