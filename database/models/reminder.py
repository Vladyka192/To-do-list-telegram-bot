from datetime import date, time, datetime

from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

class Reminder(BaseModel):
    __tablename__ = "remiders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    remind_at: Mapped[datetime | None] = mapped_column(datetime, nullable=True)
    is_sent: Mapped[bool]
    sent_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    tasks: Mapped["Task"] = relationship("Task", back_populates="reminders")