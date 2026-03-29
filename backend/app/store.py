import uuid
from datetime import datetime, timezone

from app.schemas import BillCreate, BillResponse, BillStatus


class BillNotFound(Exception):
    pass


class MemoryStore:
    def __init__(self):
        self._bills: dict[str, BillResponse] = {}

    def create(self, req: BillCreate) -> BillResponse:
        id = str(uuid.uuid4())
        status = BillStatus.unpaid
        created_at = datetime.now(timezone.utc)
        bill = BillResponse(
            id=id,
            status=status,
            created_at=created_at,
            **req.model_dump()
        )
        self._bills[id] = bill
        
        return bill


    def list(self) -> list[BillResponse]:
        return list(self._bills.values())

    def get(self, id: str) -> BillResponse:
        result = self._bills.get(id)
        if result is None:
            raise BillNotFound
        return result


    def delete(self, id: str) -> None:
        result = self._bills.get(id)
        if result is None:
            raise BillNotFound
        self._bills.pop(id)
        return