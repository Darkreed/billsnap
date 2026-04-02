from fastapi import APIRouter, HTTPException, UploadFile, Depends
from PIL import Image
import io

from app.schemas import BillCreate, BillResponse
from app.store import BillNotFound, MemoryStore

from app.ocr.extractor import OCRExtractor
from app.ocr.router import get_extractor
from app.parser.parser import BillParser
from app.parser.router import get_parser


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

@router.post("/upload", response_model=BillResponse)
async def upload_bill(file: UploadFile, extractor: OCRExtractor = Depends(get_extractor), parser: BillParser = Depends(get_parser)):
    try:
        file_contents = await file.read()
        img = Image.open(io.BytesIO(file_contents))
        extracted_text = extractor.extract_text(img)
    except Exception:
        raise HTTPException(400)
    try:
        bill_create = parser.parse(extracted_text)
        return _store.create(bill_create)
    except Exception:
        raise HTTPException(422)



