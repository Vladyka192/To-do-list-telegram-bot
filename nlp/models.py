from datetime import date, time
from enum import Enum

from pydantic import BaseModel

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ParsedTast(BaseModel):
    title: str
    date: date | None=None
    time: time | None=None
    priority: Priority = Priority.MEDIUM