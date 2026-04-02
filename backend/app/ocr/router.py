from fastapi import APIRouter, HTTPException, UploadFile, Depends
from PIL import Image
import io

from app.ocr.extractor import OCRExtractor, TesseractExtractor, PaddleOCRExtractor

router = APIRouter(prefix="/api/v1/ocr", tags=["ocr"])

def get_extractor() -> OCRExtractor:
    return PaddleOCRExtractor()

@router.post("/extract")
async def extract_text(file: UploadFile, extractor: OCRExtractor = Depends(get_extractor)):
    try:
        file_contents = await file.read()
        image = Image.open(io.BytesIO(file_contents))
        extracted_text = extractor.extract_text(image)
        return {"text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image {e}")
