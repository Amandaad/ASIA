from sqlalchemy import String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped[str] = mapped_column(String(30), index=True)
    external_id: Mapped[str] = mapped_column(String(160), index=True)
    name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=__import__("sqlalchemy").func.now())

class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int | None] = mapped_column(nullable=True)
    service_name: Mapped[str] = mapped_column(String(120))
    start_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)
    end_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    google_event_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="confirmed")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped[str] = mapped_column(String(30))
    external_id: Mapped[str] = mapped_column(String(160), index=True)
    message: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)
    handed_off: Mapped[bool] = mapped_column(Boolean, default=False)
