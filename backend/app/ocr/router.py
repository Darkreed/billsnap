from fastapi import APIRouter, HTTPException, UploadFile
from PIL import Image
import io

from app.ocr.extractor import TesseractExtractor

router = APIRouter(prefix="/api/v1/ocr", tags=["ocr"])

extractor = TesseractExtractor()


@router.post("/extract")
async def extract_text(file: UploadFile):
    try:
        file_contents = await file.read()
        image = Image.open(io.BytesIO(file_contents))
        extracted_text = extractor.extract_text(image)
        return {"text": extracted_text}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")
