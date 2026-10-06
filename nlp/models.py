from datetime import date, time
from enum import Enum

from pydantic import BaseModel

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ParsedTask(BaseModel):
    title: str
    date: date | None
    time: time | None
    priority: Priority = Priority.MEDIUM