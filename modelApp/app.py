from typing import List, Dict
import google.generativeai as genai
import json
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@dataclass
class AnalysisResult:
    manipulation_score: float
    rhetorical_devices: List[Dict]
    main_arguments: List[str]
    reasoning_patterns: List[str]
    verification_questions: List[str]

class GeminiAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)

        # Configure the model with safety settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]

        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        self.chat = self.model.start_chat(history=[])
        self.setup_prompts()

    def setup_prompts(self):
        self.analysis_prompt = """
                Perform a detailed rhetorical analysis of the following text. You must provide a complete analysis for ALL categories.

Text to analyze:
{text}

Instructions:
1. You MUST analyze and provide findings for EACH category below
2. If a category appears empty, explain WHY in that field
3. The analysis_score MUST be between 1-10 based on the depth of available rhetorical content
4. EVERY rhetorical device found MUST include type and specific context
5. Minimum of 3 entries required for each array if content permits

Required Output Format (provide ONLY this JSON with no other text):
{{
    "analysis_score": <score 1-10>,
    "rhetorical_devices": [
        {{
            "device": "<name of device>",
            "type": "<category of device>",
            "context": "<specific quote or description>"
        }}
    ],
    "main_arguments": [
        "<full argument description>"
    ],
    "reasoning_patterns": [
        "<specific pattern with example>"
    ],
    "source_attributions": [
        "<attribution detail>"
    ]
}}

Validation Rules:
- analysis_score must be numeric 1-10
- All arrays must contain entries if content permits
- Empty arrays must include explanation why
- No field may be omitted
- No quotes or comments outside JSON structure
- Context must be specific, not generic
"""

        self.verification_prompt = """
    Generate objective verification questions for fact-checking the following text.

    Text:
    {text}

    Provide response in JSON format:
    {{
        "verification_questions": [],
        "reference_suggestions": [],
        "evaluation_criteria": []
    }}

    Focus on factual verification and source credibility.
    Provide only the JSON object, no additional text.
    """

    def handle_response(self, response) -> str:
        """Safely handle model response"""
        try:
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates'):
                for candidate in response.candidates:
                    if hasattr(candidate, 'content'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text'):
                                return part.text
            raise ValueError("Could not extract text from response")
        except Exception as e:
            print(f"Error accessing response text: {str(e)}")
            raise

    def analyze_text(self, text: str) -> AnalysisResult:
        """Main analysis function with improved error handling"""
        try:
            analysis_response = self.model.generate_content(
                self.analysis_prompt.format(text=text)
            )
            analysis_text = self.handle_response(analysis_response)
            analysis_data = json.loads(analysis_text)
            return AnalysisResult(
                manipulation_score=analysis_data.get("analysis_score", 0),
                rhetorical_devices=analysis_data.get("rhetorical_devices", []),
                main_arguments=analysis_data.get("main_arguments", []),
                reasoning_patterns=analysis_data.get("reasoning_patterns", []),
                verification_questions=[]
            )
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            raise

# Pydantic models for FastAPI
class TextInput(BaseModel):
    text: str

class AnalysisOutput(BaseModel):
    manipulation_score: float
    rhetorical_devices: List[Dict]
    main_arguments: List[str]
    reasoning_patterns: List[str]
    verification_questions: List[str]

# Initialize analyzer with your API key
analyzer = GeminiAnalyzer(api_key="AIzaSyBoaHgH2fhKTtuHloOHqHP8Qsbjfbvgysg")

# Define routes
@app.post("/analyze", response_model=AnalysisOutput)
async def analyze_text_route(input_data: TextInput):
    try:
        result = analyzer.analyze_text(input_data.text)
        return result.__dict__  # Convert dataclass to dictionary for JSON response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    # Démarre l'application FastAPI sur le port 8081
    uvicorn.run(app, host="0.0.0.0", port=8081)
