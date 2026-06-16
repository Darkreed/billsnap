# billsnap

A full-stack bill processing application with OCR, AI parsing, and calendar sync.

## Stack

**Backend:**
- FastAPI + async SQLAlchemy
- PostgreSQL database
- PaddleOCR + Claude API + Ollama fallback
- Google Calendar OAuth2

**Frontend:**
- React 19 + TypeScript
- Tailwind CSS
- Vite

## Features

- Receipt/bill image upload
- Automatic extraction with AI
- Japanese bill support (era dates, amount fields)
- Payment reminders via Google Calendar
- PostgreSQL persistence

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev