from abc import ABC, abstractmethod
from datetime import date

from app.schemas import BillCreate
import json

class BillParser(ABC):
    """Abstract base class for LLM bill parsers."""

    @abstractmethod
    def parse(self, text: str) -> BillCreate:
        ...


class MockParser(BillParser):
    """Returns hardcoded data. Used in tests and when no API key is available."""

    def parse(self, text: str) -> BillCreate:
        return BillCreate(
            biller="Mock Biller",
            amount=1000.0,
            currency="JPY",
            due_date=date(2026, 5, 1),
        )


class ClaudeParser(BillParser):

    def __init__(self, api_key: str):
        import anthropic
        self._client = anthropic.Anthropic(api_key=api_key)

    def parse(self, text: str) -> BillCreate:
        try:
            prompt = (
                "Extract the following fields from this bill text and return ONLY valid JSON, "
                "no explanation, no markdown:\n"
                "Fields: biller, amount, currency, language, due_date (YYYY-MM-DD format)\n\n"
                f"{text}"
            )
            
            claude_response = self._client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}]
            )

            parsed_data = json.loads(claude_response.content[0].text)
            bill = BillCreate(**parsed_data)
            return bill

        except Exception as e:
            raise ValueError(f"Failed to parse bill: {e}")


class OllamaParser(BillParser):
    
    def __init__(self, model: str = "qwen2.5"):
        import ollama
        self._client = ollama.Client()
        self._model = model

    def parse(self, text: str) -> BillCreate:
        try:
            prompt = (
                "Extract the following fields from this bill text:\n"
                "no explanation, no markdown:\n"
                "Fields: biller, amount, currency, language (language of the text), due_date (YYYY-MM-DD format)\n\n"
                f"{text}"
            )
            llm_response = self._client.chat(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            
            bill_data = json.loads(llm_response.message.content)

            bill = BillCreate(**bill_data)
            return bill
        
        except Exception:
            raise ValueError(f"Failed to parse bill")