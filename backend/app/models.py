import uuid
from datetime import date, datetime

from sqlalchemy import Enum as SAEnum, String, Float, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.schemas import BillStatus


class Bill(Base):
    __tablename__ = "bills"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    biller: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[BillStatus] = mapped_column(SAEnum(BillStatus), default=BillStatus.unpaid)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    billing_month: Mapped[date | None] = mapped_column(Date, nullable=True)
    recipient: Mapped[str | None] = mapped_column(String, nullable=True)
    currency: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    calendar_event_id: Mapped[str | None] = mapped_column(String, nullable=True)

    # TODO: add image_path: Mapped[str | None] for when we store uploaded images
