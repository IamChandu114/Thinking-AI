from fastapi import APIRouter
from app.schemas.decision_schema import DecisionRequest, DecisionResponse
from app.services.reasoning_engine import ReasoningEngine
from app.memory.decision_store import get_all_decisions

router = APIRouter()
engine = ReasoningEngine()


@router.post("/analyze", response_model=DecisionResponse)
def analyze_decision(request: DecisionRequest):
    return engine.think(request)


@router.get("/history")
def decision_history():
    return {
        "total_decisions": len(get_all_decisions()),
        "decisions": get_all_decisions()
    }
