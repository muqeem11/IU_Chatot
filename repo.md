# Repository Overview

## Project
- **Name**: Integral University Chatbot
- **Type**: Full-stack web app (FastAPI backend, React/Vite frontend)
- **Local dev URLs**:
  - **Backend**: http://localhost:8000
  - **Frontend**: http://localhost:5173

## How to Run
1. Backend (in one terminal):
   - `c:\newbot\backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload`
2. Frontend (in another terminal):
   - `Set-Location c:\newbot\frontend; npm run start`

## Backend Structure (c:\newbot\backend)
- **app.py**: FastAPI app, CORS, router registration
- **routes.py**: Endpoints: `GET /health`, `POST /chat`; multi-intent aggregation
- **schemas.py**: Pydantic models
  - `ChatRequest { message: string }`
  - `ChatResponse { intent: string, answer: string, confidence: number }`
- **nlp.py**: Text normalization, mappings
- **model.py**: TF-IDF + Logistic Regression pipeline
- **answers.py**: Intent → answer builders (composes response paragraphs)
- **data.py**: Default content + overrides from `data/faqs.json`
- **main.py**: Thin entrypoint exporting `app`
- **requirements.txt**: Python deps
- **data/faqs.json**: Content overrides

## API
- **GET /health** → `{ status: "ok" }`
- **POST /chat** (application/json)
  - Request: `{ "message": string }`
  - Response: `{ "intent": string, "answer": string, "confidence": number }`
  - Behavior: combines top 2–3 intents (≥0.25 probability) into a single answer body (paragraphs separated by blank lines). `intent`/`confidence` are the top class.

## Frontend (c:\newbot\frontend)
- **Stack**: React 18, Vite 5, TypeScript
- **Scripts**: `{ start: "vite", build: "vite build", preview: "vite preview" }`
- **Entry**: `src/main.tsx`
- **Config**: `vite.config.ts` (port 5173, strict)
- **Notes**: TTS currently single-language (`en-IN`); previous multilingual TTS and `language` field were reverted.

## Notes & Next Steps
- Consider re-adding same-language replies (API `language` + frontend TTS switching) when desired.
- Expand training data and Hindi/Hinglish aliases for accuracy.
- Optionally return `intents: string[]` for labeled UI sections.
- Add caching/spinners for voice UX.