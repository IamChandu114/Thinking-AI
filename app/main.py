# app/main.py
from fastapi import FastAPI
from app.api.decision import router as decision_router

app = FastAPI(
    title="Thinking AI",
    description="AI system that reasons, detects uncertainty, explains decisions, and keeps memory",
    version="1.0.0"
)

# Include the decision-making router
app.include_router(decision_router, prefix="/api")
