from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BigInteger

class Task(BaseModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    