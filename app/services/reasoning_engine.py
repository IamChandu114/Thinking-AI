import datetime
import json
import os
import re
from app.memory.decision_store import store_decision
from google import genai

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def safe_parse_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except:
        return None

class ReasoningEngine:
    def think(self, request):
        input_text = request.input_text.strip()

        if not input_text:
            result = {
                "prediction": "Unclear Fit",
                "confidence": 0.0,
                "reasoning": "No input provided.",
                "needs_clarification": True,
                "clarification_questions": ["Please provide resume or candidate details."],
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            store_decision(result)
            return result

        prompt = f"""
You are an expert AI candidate evaluator.
Analyze the following input text and output JSON **only**.
Do not include explanations outside JSON.

The JSON must contain:
- prediction: "Potential Fit" | "Unclear Fit" | "Low Fit"
- confidence: float between 0 and 1
- reasoning: string (step-by-step)
- needs_clarification: true/false
- clarification_questions: list of strings

Input text:
\"\"\"{input_text}\"\"\"
"""

        try:
            # Gemini call without temperature / max_output_tokens
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            result_text = response.text
            result = safe_parse_json(result_text)

            # Retry once if parsing fails
            if not result:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                result = safe_parse_json(response.text)

        except Exception as e:
            result = None
            error_msg = str(e)

        if not result:
            result = {
                "prediction": "Unclear Fit",
                "confidence": 0.4,
                "reasoning": "Gemini output was not valid JSON.",
                "needs_clarification": True,
                "clarification_questions": ["Please provide clearer resume details."]
            }
            if 'error_msg' in locals():
                result["reasoning"] += f" [Error: {error_msg}]"

        result["timestamp"] = datetime.datetime.utcnow().isoformat()
        store_decision(result)

        return result
