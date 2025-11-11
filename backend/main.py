# Thin entrypoint to run the FastAPI app
from backend.app import app  # noqa: F401

# Run: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload