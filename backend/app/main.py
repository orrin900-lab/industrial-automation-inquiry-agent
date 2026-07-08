from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.inquiries import router as inquiries_router
from app.api.knowledge import router as knowledge_router
from app.db.init_db import init_db


app = FastAPI(
    title="Industrial Inquiry Agent Backend",
    version="0.1.0",
    description="A-stage FastAPI wrapper for the C+ Agent Core.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(inquiries_router, prefix="/api")
app.include_router(knowledge_router, prefix="/api")


@app.on_event("startup")
def initialize_database() -> None:
    init_db()
