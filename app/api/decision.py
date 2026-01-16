# app/api/decision.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.reasoning_engine import ReasoningEngine

router = APIRouter()
engine = ReasoningEngine()  # Initialize the reasoning engine

class CandidateInput(BaseModel):
    input_text: str

@router.post("/analyze")
def analyze(input_data: CandidateInput):
    """
    Endpoint to analyze candidate input.
    Returns prediction, reasoning, confidence, and clarification questions.
    """
    result = engine.analyze_candidate(input_data.input_text)
    return result
