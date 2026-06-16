from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class BillStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    overdue = "overdue"

class BillCreate(BaseModel):
    biller: str
    amount: float
    due_date: date | None = None
    billing_month: date | None = None
    recipient: str | None = None
    currency: str | None = None
    language: str | None = None
    calendar_event_id: str | None = None

class BillResponse(BaseModel):
    id: UUID
    status: BillStatus
    biller: str
    amount: float
    due_date: date | None = None
    billing_month: date | None = None
    created_at: datetime
    recipient: str | None = None
    currency: str | None = None
    language: str | None = None
    calendar_event_id: str | None = None

    model_config = {"from_attributes": True}
