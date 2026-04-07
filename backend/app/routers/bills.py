from fastapi import APIRouter, HTTPException, UploadFile, Depends
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import io

from app.database import get_db
from app.models import Bill
from app.schemas import BillCreate, BillResponse
from app.ocr.extractor import OCRExtractor
from app.calendar.client import CalendarClient

from app.ocr.router import get_extractor
from app.parser.parser import BillParser
from app.parser.router import get_parser
from app.calendar.router import get_calendar_client

router = APIRouter(prefix="/api/v1/bills", tags=["bills"])


@router.post("/", response_model=BillResponse, status_code=201)
async def create_bill(
    req: BillCreate,
    db: AsyncSession = Depends(get_db),
    calendar: CalendarClient = Depends(get_calendar_client),
):
    bill = Bill(**req.model_dump())
    db.add(bill)
    await db.commit()
    await db.refresh(bill)
    if bill.due_date is not None:
        event_title = f"Pay {bill.biller}"
        event_desc = f"{bill.amount} {bill.currency}"
        calendar.create_event(title=event_title, due_date=bill.due_date, description=event_desc)
    return bill


@router.get("/", response_model=list[BillResponse])
async def list_bills(db: AsyncSession = Depends(get_db)):
    bills_select = select(Bill)
    bills_res = await db.execute(bills_select)
    return bills_res.scalars().all()
    


@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(bill_id: str, db: AsyncSession = Depends(get_db)):
    bill = await db.get(Bill, bill_id)
    if bill is None:
        raise HTTPException(404)
    return bill


@router.delete("/{bill_id}", status_code=204)
async def delete_bill(bill_id: str, db: AsyncSession = Depends(get_db)):
    bill = await db.get(Bill, bill_id)
    if bill is None:
        raise HTTPException(404)
    await db.delete(bill)
    await db.commit()
    return


@router.post("/upload", response_model=BillResponse)
async def upload_bill(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    extractor: OCRExtractor = Depends(get_extractor),
    parser: BillParser = Depends(get_parser),
    calendar: CalendarClient = Depends(get_calendar_client),
):
    try:
        file_contents = await file.read()
        img = Image.open(io.BytesIO(file_contents))
        extracted_text = extractor.extract_text(img)
        print(f"OCR output: {extracted_text}")
    except Exception:
        raise HTTPException(400)
    try:
        bill_create = parser.parse(extracted_text)
        bill = Bill(**bill_create.model_dump())
        db.add(bill)
        await db.commit()
        await db.refresh(bill)
        if bill.due_date is not None:
            event_title = f"Pay {bill.biller}"
            event_desc = f"{bill.amount} {bill.currency}"
            calendar.create_event(title=event_title, due_date=bill.due_date, description=event_desc)
        return bill
    except Exception as e:
        raise HTTPException(422, detail=str(e))

