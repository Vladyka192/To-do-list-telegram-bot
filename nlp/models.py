from datetime import date, time
from enum import Enum

from pydantic import BaseModel

class Priority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class ParsedTask(BaseModel):
    title: str
    date: date | None
    time: time | None
    priority: Priority = Priority.MEDIUM