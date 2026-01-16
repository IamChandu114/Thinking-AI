# app/services/reasoning_engine.py
import os
import json
from google import genai

class ReasoningEngine:
    def __init__(self):
        # Initialize Gemini client with API key from environment variable
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def analyze_candidate(self, input_text: str):
        """
        Analyze candidate input and return structured reasoning output.
        """
        try:
            # Send input to Gemini and request structured JSON response
            response = self.client.generate_content(
                model="gemini-2.5",
                prompt=f"""
You are a reasoning-first AI assistant. Analyze this candidate's input and respond in valid JSON format.
Candidate Input: "{input_text}"

Output JSON format:
{{
  "prediction": "Potential Fit | Unclear Fit | Not Fit",
  "confidence": 0-100,
  "reasoning": "Explain reasoning step by step",
  "clarification_needed": true/false,
  "questions": ["Optional clarification questions"]
}}
"""
            )

            # Gemini returns a text; parse it into JSON
            result_text = response.content[0].text
            result_json = json.loads(result_text)
            return result_json

        except Exception as e:
            # Return fallback structured error
            return {
                "prediction": "Error",
                "confidence": 0,
                "reasoning": f"Error occurred: {str(e)}",
                "clarification_needed": True,
                "questions": []
            }
