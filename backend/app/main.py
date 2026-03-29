from fastapi import FastAPI

from app.routers import bills

app = FastAPI(title="BillSnap", version="0.1.0")

app.include_router(bills.router)


@app.get("/health")
async def health():
    return {"status" : "ok"}
