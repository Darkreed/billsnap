from fastapi import FastAPI

from app.routers import bills
from app.ocr import router as ocr_router

app = FastAPI(title="BillSnap", version="0.1.0")

app.include_router(bills.router)
app.include_router(ocr_router.router)

@app.get("/health")
async def health():
    return {"status" : "ok"}
