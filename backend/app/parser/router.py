import os

from fastapi import APIRouter, HTTPException, Depends

from app.parser.parser import BillParser, ClaudeParser, MockParser, OllamaParser
from app.schemas import BillCreate

router = APIRouter(prefix="/api/v1/parse", tags=["parser"])


def get_parser() -> BillParser:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        return ClaudeParser(api_key=api_key)
    return OllamaParser()


@router.post("/", response_model=BillCreate)
async def parse_bill(payload: dict, parser: BillParser = Depends(get_parser)):
    try:
        text = payload["text"]
        parsed_text = parser.parse(text)
        return parsed_text
    except KeyError:
        raise HTTPException(400)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
