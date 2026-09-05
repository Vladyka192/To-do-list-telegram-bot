from datetime import datetime, timezone
from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger, String, DateTime

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Almaty", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")