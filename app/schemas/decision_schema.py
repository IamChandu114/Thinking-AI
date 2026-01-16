from pydantic import BaseModel
from typing import Optional, List


class DecisionRequest(BaseModel):
    input_text: str


class DecisionResponse(BaseModel):
    prediction: str
    confidence: float
    reasoning: str
    needs_clarification: bool
    clarification_questions: Optional[List[str]] = None
