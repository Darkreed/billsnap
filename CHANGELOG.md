# Changelog

All notable changes to this project will be documented in this file.

Format: `[version] - YYYY-MM-DD`
Types: `Added`, `Changed`, `Fixed`, `Removed`

---

## [0.3.0] - 2026-04-07

### Added
- Google Calendar OAuth2 integration — creates payment reminder events on bill save
- `auth_google.py` standalone script for one-time OAuth flow (non-blocking)
- Prompt tuning for Japanese era date conversion (令和/平成)
- Prompt tuning to extract 合計請求金額 as the total amount in Japanese bills
- Currency inference from biller context when symbol is absent in OCR output
- Image resizing before OCR (max 1024px) — reduced OCR time from ~180s to ~33s
- Module-level PaddleOCR initialization — eliminated per-request model reload

### Changed
- Switched local LLM from qwen2.5 to gemma4 for better structured output
- OllamaParser date normalization handles DD-MM-YYYY and other non-ISO formats

---

## [0.2.0] - 2026-04-03

### Added
- PostgreSQL database with SQLAlchemy async ORM
- Alembic migrations (`create bills table`)
- `database.py` — async engine, session factory, `get_db` dependency
- `models.py` — SQLAlchemy `Bill` ORM model
- CORS middleware allowing requests from `localhost:5173`

### Changed
- Replaced in-memory `MemoryStore` with PostgreSQL-backed DB operations
- All bill endpoints now use `AsyncSession = Depends(get_db)`

### Removed
- `store.py` in-memory store

---

## [0.1.0] - 2026-03-28

### Added
- FastAPI project scaffold with health check endpoint
- Bill CRUD endpoints: `POST /`, `GET /`, `GET /{id}`, `DELETE /{id}`
- Pydantic schemas: `BillCreate`, `BillResponse`, `BillStatus`
- PaddleOCR extractor with abstract `OCRExtractor` base class
- Claude API parser with Ollama (local LLM) fallback
- `/api/v1/bills/upload` pipeline: OCR → parse → store
- Interface-based design for OCR, parser, and calendar (swappable via DI)
