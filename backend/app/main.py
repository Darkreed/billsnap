from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import bills
from app.ocr import router as ocr_router
from app.parser import router as parser_router

app = FastAPI(title="BillSnap", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bills.router)
app.include_router(ocr_router.router)
app.include_router(parser_router.router)
@app.get("/health")
async def health():
    return {"status" : "ok"}
