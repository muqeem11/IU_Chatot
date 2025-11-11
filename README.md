# Integral University Chatbot

A full‑stack web application providing a question‑answering chatbot for Integral University. The backend is built with FastAPI (Python), and the frontend is built with React + Vite (TypeScript). The model uses a TF‑IDF + Logistic Regression pipeline and composes multi‑intent answers.

## Table of Contents
1. Overview
2. Features
3. Architecture
4. Project Structure
5. Prerequisites
6. Quick Start (Local)
7. API Reference
8. Frontend Details
9. Content & Data
10. Development Notes
11. Troubleshooting
12. Deployment (Basics)
13. Contributing

---

## 1) Overview
- **Name**: Integral University Chatbot
- **Type**: Full-stack web app (FastAPI backend, React/Vite frontend)
- **Local Dev URLs**:
  - **Backend**: http://localhost:8000
  - **Frontend**: http://localhost:5173

## 2) Features
- **FastAPI backend** with simple, typed endpoints.
- **ML pipeline**: TF‑IDF + Logistic Regression for intent classification.
- **Multi‑intent aggregation**: combines top 2–3 intents (≥0.25 probability) into a single answer body.
- **React + Vite frontend** with TypeScript and a simple chat UI.
- **Content overrides** via JSON for quick updates.

## 3) Architecture
- **Backend**: Exposes REST endpoints, handles text normalization, predicts intents, and generates composed answers from intent‑wise templates.
- **Frontend**: Single‑page app that sends messages to the backend and renders responses (with optional TTS in `en‑IN`).

## 4) Project Structure
```
newbot/
├─ backend/
│  ├─ app.py              # FastAPI app, CORS, router registration
│  ├─ routes.py           # Endpoints: GET /health, POST /chat
│  ├─ schemas.py          # Pydantic models (ChatRequest, ChatResponse)
│  ├─ nlp.py              # Text normalization, mappings
│  ├─ model.py            # TF‑IDF + Logistic Regression pipeline
│  ├─ answers.py          # Intent → answer builders
│  ├─ data.py             # Default content + overrides from data/faqs.json
│  ├─ main.py             # Entrypoint exporting `app`
│  ├─ requirements.txt    # Python dependencies
│  └─ data/
│     └─ faqs.json        # Customizable content overrides
│
├─ frontend/
│  ├─ src/
│  │  ├─ main.tsx         # App entry
│  │  └─ components/      # UI components
│  ├─ index.html
│  ├─ package.json        # Scripts: start, build, preview
│  ├─ tsconfig.json
│  └─ vite.config.ts      # Vite config (port 5173)

## 5) Prerequisites
- **Windows (PowerShell)** – commands below are provided for Windows.
- **Python**: 3.11 recommended.
- **Node.js**: 18+ recommended (LTS is fine) and npm.

## 6) Quick Start (Local)

### 6.1 Backend (FastAPI)
- Option A: Use the provided virtual environment directly (recommended if already present):

```powershell
# Install deps if needed
c:\newbot\backend\.venv\Scripts\python.exe -m pip install --upgrade pip
c:\newbot\backend\.venv\Scripts\python.exe -m pip install -r c:\newbot\backend\requirements.txt

# Run development server (auto‑reload)
c:\newbot\backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

- Option B: Create a fresh virtual environment (if the bundled one is missing):

```powershell
# Create and activate venv
python -m venv c:\newbot\backend\.venv
c:\newbot\backend\.venv\Scripts\Activate.ps1

# Install deps
pip install --upgrade pip
pip install -r c:\newbot\backend\requirements.txt

# Run dev server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at http://localhost:8000.

### 6.2 Frontend (React + Vite)
```powershell
Set-Location c:\newbot\frontend

# Install dependencies (use npm ci if you want lockfile‑exact installs)
npm install

# Start dev server (default port 5173)
npm run start
```
Open http://localhost:5173 in your browser.

## 7) API Reference

### 7.1 Health Check
- **GET** `/health`
- Response:
```json
{ "status": "ok" }
```

### 7.2 Chat
- **POST** `/chat`
- **Request (application/json)**:
```json
{ "message": "Your question here" }
```
- **Response**:
```json
{
  "intent": "admissions",
  "answer": "...composed answer with possibly multiple sections...",
  "confidence": 0.87
}
```
- **Behavior**: The backend may combine the top 2–3 intents (each ≥ 0.25 probability) into a single answer. `intent`/`confidence` represent the top class.

- Example (PowerShell + curl):
```powershell
curl -X POST "http://localhost:8000/chat" `
  -H "Content-Type: application/json" `
  -d '{"message":"What are the admission requirements and fees?"}'
```

## 8) Frontend Details
- **Stack**: React 18, Vite 5, TypeScript.
- **Scripts** (package.json):
  - `start`: `vite`
  - `build`: `vite build`
  - `preview`: `vite preview`
- **Notes**: Text‑to‑Speech (TTS) currently uses a single language (`en‑IN`). Previously supported multilingual TTS and an API `language` field were removed; these can be re‑introduced later.

## 9) Content & Data
- Default content is defined in `backend/data.py`.
- You can override or extend content in `backend/data/faqs.json` without changing code. The backend merges these on startup.
- To add new intents:
  1. Extend mappings/aliases in `backend/nlp.py`.
  2. Add answer builders (sections) in `backend/answers.py`.
  3. Update training data logic in `backend/model.py` if needed.

## 10) Development Notes
- **Code style**: Keep functions small and readable; add docstrings where beneficial.
- **CORS**: Configured in `backend/app.py` to allow the local Vite dev server.
- **Hot reload**: `--reload` for backend; Vite provides HMR for frontend.
- **Type safety**: Pydantic models for requests/responses; TypeScript on the frontend.

## 11) Troubleshooting
- **Port already in use**:
  - Backend (8000): Stop other uvicorn/servers or change `--port`.
  - Frontend (5173): Vite will prompt to use another port or configure in `vite.config.ts`.
- **Pip package errors**:
  - Ensure you are using the correct interpreter: `c:\newbot\backend\.venv\Scripts\python.exe`.
  - Upgrade pip: `python -m pip install --upgrade pip`.
- **Node errors**:
  - Use Node 18+; delete `node_modules` and re‑run `npm install` if needed.
- **CORS issues**:
  - Ensure backend is running on 8000 and frontend on 5173; verify origins in `backend/app.py`.
- **Model accuracy**:
  - Expand aliases and training samples in `nlp.py` / `data.py` / `data/faqs.json`.

## 12) Deployment (Basics)
- **Backend**:
  - Build a production image or run uvicorn/gunicorn behind a reverse proxy (nginx/IIS). Example uvicorn command:
  ```powershell
  c:\newbot\backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```
- **Frontend**:
  - Build static assets and serve via a static server or CDN:
  ```powershell
  Set-Location c:\newbot\frontend
  npm run build
  # Output will be in dist/
  npm run preview # local preview of the build
  ```
- Configure the frontend to call the deployed backend URL (use environment variables or configuration if you externalize URLs).

## 13) Contributing
- Open an issue for significant changes before submitting a PR.
- Follow the existing coding style and keep changes focused.
- Add comments where logic is non‑obvious, and prefer clarity over cleverness.

---

Happy building! If you run into problems, check the Troubleshooting section or open an issue.
## Authentication & Authorization

- Endpoints are protected except `/health` and auth endpoints.
- Obtain a token via `/auth/token` using username/password from `/auth/register`.
- Include the token as a Bearer token in the `Authorization` header.

Example (PowerShell):

```powershell
$base = "http://localhost:8000"
$cred = "username=tester2&password=P@ssw0rd!"
$token = (Invoke-RestMethod -Method POST -Uri "$base/auth/token" -ContentType "application/x-www-form-urlencoded" -Body $cred).access_token
Invoke-RestMethod -Method POST -Uri "$base/chat" -Headers @{ Authorization = "Bearer $token" } -ContentType "application/json" -Body '{"message":"MBA admission process"}'
```

## Environment Configuration

- Backend uses SQLite by default at `c:\newbot\chatbot.db`.
- To change DB, set `DATABASE_URL` environment variable (e.g., `postgresql+psycopg2://user:pass@host:5432/dbname`).
- Security keys are in `backend/auth.py` for local development. For production, set via environment and import from `os.getenv`.

Environment variables:
- `DATABASE_URL` � SQLAlchemy connection string (optional; defaults to SQLite file).
- `SECRET_KEY` � JWT signing key (recommended to set in production).

```powershell
# Example: run backend with a custom DB and secret key
$env:DATABASE_URL = "sqlite:///./dev.db"
$env:SECRET_KEY = "dev-secret-change-me"
c:\newbot\backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
