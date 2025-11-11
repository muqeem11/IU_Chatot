from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .auth_router import router as auth_router
from .database import engine
from .db_models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Integral University Chatbot API")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(router)