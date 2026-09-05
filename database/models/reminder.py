from datetime import datetime, timezone

from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime

class Reminder(BaseModel):
    __tablename__ = "remiders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    remind_at: Mapped[datetime | None] = mapped_column(nullable=True)
    is_sent: Mapped[bool] = mapped_column(default=False, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    task: Mapped["Task"] = relationship("Task", back_populates="reminders")