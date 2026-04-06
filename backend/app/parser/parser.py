from abc import ABC, abstractmethod
from datetime import datetime, date

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
                "currency: string — infer from context if not explicit (airtel.in/Indian biller → 'INR', Japanese biller → 'JPY', etc.) or null if truly unknown\n"
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
    
    def __init__(self, model: str = "gemma4"):
        import ollama
        self._client = ollama.Client()
        self._model = model

    def parse(self, text: str) -> BillCreate:
        try:
            prompt = (
                "You are a bill data extractor. Extract structured data from the bill text below.\n"
                "Return ONLY a JSON object with exactly these fields:\n"
                "  biller: string (company or person issuing the bill)\n"
                "  amount: number (total amount due, no currency symbol)\n"
                "  currency: string — infer from context if not explicit (airtel.in/Indian biller → 'INR', Japanese biller → 'JPY', etc.) or null if truly unknown\n"
                "  language: 'ja', 'en', or 'mixed'\n"
                "  due_date: date string in YYYY-MM-DD format, or null if not found\n"
                "If a field cannot be determined from the text, use null.\n"
                "The bill may be in Japanese — extract data regardless of language.\n\n"
                "  currency: infer from context if not explicit (e.g. Indian companies → 'INR', Japanese → 'JPY')\n"
                f"Bill text:\n{text}"
            )

            llm_response = self._client.chat(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            print("LLM Response:"+llm_response.message.content)
            bill_data = json.loads(llm_response.message.content)
            if bill_data.get("due_date"):
                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%d/%m/%Y"):
                    try:
                        bill_data["due_date"] = datetime.strptime(bill_data["due_date"], fmt).strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
            bill = BillCreate(**bill_data)
            return bill
        
        except Exception:
            raise ValueError(f"Failed to parse bill")