from datetime import date, time, datetime

from database.models import BaseModel
# from database.models.user import User
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

class Task(BaseModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[str]
    priority: Mapped[int]
    due_date: Mapped[date]
    due_time: Mapped[time]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    user: Mapped["User"] = relationship("User", back_populates="tasks")