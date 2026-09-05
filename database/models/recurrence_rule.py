from datetime import date, datetime

from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, DateTime

class RecurrenceRule(BaseModel):
    __tablename__ = "recurrence_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    interval: Mapped[int] = mapped_column(nullable=False)
    weekdays: Mapped[list] = mapped_column(int, nullable=False)
    day_of_month: Mapped[date] = mapped_column(nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    next_run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    task: Mapped["Task"] = relationship("Task", back_populates="reminders")