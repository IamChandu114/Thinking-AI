# app/services/reasoning_engine.py
import os
import json
from google.genai import Client  # <-- change here

class ReasoningEngine:
    def __init__(self):
        # Initialize Gemini client with API key
        self.client = Client(api_key=os.getenv("GEMINI_API_KEY"))

    def analyze_candidate(self, input_text: str):
        try:
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

            result_text = response.content[0].text
            return json.loads(result_text)

        except Exception as e:
            return {
                "prediction": "Error",
                "confidence": 0,
                "reasoning": f"Error occurred: {str(e)}",
                "clarification_needed": True,
                "questions": []
            }
