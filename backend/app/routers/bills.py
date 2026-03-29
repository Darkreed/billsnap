from fastapi import APIRouter, HTTPException

from app.schemas import BillCreate, BillResponse
from app.store import BillNotFound, MemoryStore

router = APIRouter(prefix="/api/v1/bills", tags=["bills"])

_store = MemoryStore()


@router.post("/", response_model=BillResponse, status_code=201)
async def create_bill(req: BillCreate):
    return _store.create(req)


@router.get("/", response_model=list[BillResponse])
async def list_bills():
    return _store.list()


@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(bill_id: str):
    try:
        return _store.get(bill_id)
    except BillNotFound:
        raise HTTPException(status_code=404, detail="bill not found")


@router.delete("/{bill_id}", status_code=204)
async def delete_bill(bill_id: str):
    try:
        _store.delete(bill_id)
    except BillNotFound:
        raise HTTPException(status_code=404, detail="bill not found")
