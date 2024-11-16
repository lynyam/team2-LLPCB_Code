from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import json
from modelApp.logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()
log = get_logger()

app = FastAPI()

# Pydantic models for request/response
class TextInput(BaseModel):
    text: str

class Manipulation(BaseModel):
    instance: str
    explanation: str

class ArgumentManipulations(BaseModel):
    ad_populum: List[Manipulation]
    unspecified_authority_fallacy: List[Manipulation]
    appeal_to_pride: List[Manipulation]
    false_dilemma: List[Manipulation]
    cherry_picking_data: List[Manipulation]
    stork_fallacy: List[Manipulation]
    fallacy_of_composition: List[Manipulation]
    fallacy_of_division: List[Manipulation]
    hasty_generalization: List[Manipulation]
    texas_sharpshooter_fallacy: List[Manipulation]

class Argument(BaseModel):
    _type: str
    statement: str
    connection_to_hypothesis: str
    manipulations: ArgumentManipulations

class AnalysisOutput(BaseModel):
    thesis: str
    arguments: List[Argument]

class ArgumentAnalysisAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert argument analysis agent. Your task is to:
1. Analyze the given text carefully
2. Identify the main hypothesis
3. Extract supporting arguments
4. Structure your response in JSON format

Your analysis should be thorough and precise."""),
            ("human", """### TASK
Analysis Request: Generate JSON Analysis of Text Hypothesis and Arguments

Please analyze the provided text and return the results in the following JSON structure:

### TEST
{text}

### OUTPUT
{{
    "main_hypothesis": {{
        "statement": "<text>"
    }},
    "arguments": [
        {{
            "_type": "<primary|secondary>",
            "statement": "<text>",
            "connection_to_hypothesis": "<text>"
        }},
    ]
}}""")
        ])

    async def analyze(self, text: str) -> dict:
        """Run the argument analysis."""
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"text": text})
        
        try:
            json_str = response.content.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:-3]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse JSON response: {str(e)}", "raw_response": response.content}

class ManipulationAnalysisAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in detecting manipulation and persuasion techniques in text. Your task is to:
                1. Analyze the given text for manipulation techniques
                """),
            ("human", """### TASK
                Focus only on the following manipulation technique:
                {manipulation_technique}

                Analysis Request: Generate JSON Analysis of Manipulation Techniques

                Please analyze the provided text and return the results in the following JSON structure:

                ### TEXT
                {text}

                The arguments of the text are
                arguments: {arguments}

                ### OUTPUT
                {{
                    "main_thesis": "<str>",
                    "arguments": [
                        {{ 
                            "argument_text": "<str>", exactly written as received in the arguments
                            "contains_manipulation": <true|false>,
                            "manipulations": [
                                {{
                                    "instance": "<str>",
                                    "explanation": "<str>"
                                }}
                            ]
                        }}
                    ]
                }}""")
        ])

    async def analyze(self, manipulation_technique: str, text: str, arguments: str) -> dict:
        """Run the manipulation analysis."""
        chain = self.prompt | self.llm
        response = await chain.ainvoke({
            "manipulation_technique": manipulation_technique,
            "text": text,
            "arguments": arguments
        })
        
        try:
            json_str = response.content.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:-3]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse JSON response: {str(e)}", "raw_response": response.content}

class TextAnalysisSystem:
    def __init__(self):
        self.argument_agent = ArgumentAnalysisAgent()
        self.manipulation_agent = ManipulationAnalysisAgent()
        
        # Fallacy definitions
        self.ad_populum = """
        - Argumentum ad populum: to present a belief as true simply because it is widely accepted.         
                Examples: 'Most people believe,' 'Everyone knows,' 'Everyone agrees'."""
        self.unspecified_authority_fallacy = """
        - Unspecified Authority fallacy: Relies on a vague or unnamed authority to lend credibility to a claim.
                Examples: 'Experts say,' 'Studies show' without specific sources."""
        self.appeal_to_pride = """
        - Appeal to Pride: flatters the audience by implying that only intelligent, patriotic, etc. people agree. 
                Examples: 'Only smart people know', 'Real patriots understand'."""
        self.false_dilemma = """
        - False Dilemma: presents two choices as if they were the only possibilities, when other options exist. 
                Examples: 'The only option is...' 'Either we act now or we lose everything'."""
        self.cherry_picking_data = """
        - Cherry-Picking Data: selects only the data that supports the argument while ignoring contrary evidence.
                Examples: 'Studies show 90 percent success rate, proving it works'."""
        self.stork_fallacy = """
        - Correlation vs. Causality (Stork fallacy): assumes that correlation necessarily means causation.
                Examples: 'Ice cream sales and drowning deaths both increase in summer, therefore ice cream causes drownings'."""
        self.fallacy_of_composition = """
        - Fallacy of Composition: assumes that if each part of a whole has a quality, the whole must also have that quality.
                Examples.: 'this bag contains feathers, feathers are light, therefore this bag is light'."""
        self.fallacy_of_division = """
        - Fallacy of Division: assumes that if a whole has a quality, all its parts must have that quality too.
                Examples: 'This boat floats, therefore every piece of this boat floats'."""
        self.hasty_generalization = """
        - Hasty Generalization: extends characteristics of a small sample to a larger group.
                Examples: 'I know two people from Chicago who are rude, therefore all people from Chicago must be rude'."""
        self.texas_sharpshooter_fallacy = """
        - Texas Sharpshooter Fallacy: a fallacy which is committed when differences in data are ignored, but similarities are overemphasized.
                Example: 'A company claims their training program is highly effective by only highlighting the 5 employees who got promotions'."""

    async def analyze_text(self, text: str) -> dict:
        """Perform analysis and return in API format"""
        raw_results = await self._analyze_raw(text)
        return self.raw_data_to_api_format(raw_results)

    async def _analyze_raw(self, text: str) -> dict:
        """Perform both argument and manipulation analysis on the text."""
        argument_analysis = await self.argument_agent.analyze(text)
        
        # Run all manipulation analyses concurrently
        manipulation_analyses = {
            "argument_analysis": argument_analysis,
            "ad_populum": await self.manipulation_agent.analyze(self.ad_populum, text, str(argument_analysis)),
            "unspecified_authority_fallacy": await self.manipulation_agent.analyze(self.unspecified_authority_fallacy, text, str(argument_analysis)),
            "appeal_to_pride": await self.manipulation_agent.analyze(self.appeal_to_pride, text, str(argument_analysis)),
            "false_dilemma": await self.manipulation_agent.analyze(self.false_dilemma, text, str(argument_analysis)),
            "cherry_picking_data": await self.manipulation_agent.analyze(self.cherry_picking_data, text, str(argument_analysis)),
            "stork_fallacy": await self.manipulation_agent.analyze(self.stork_fallacy, text, str(argument_analysis)),
            "fallacy_of_composition": await self.manipulation_agent.analyze(self.fallacy_of_composition, text, str(argument_analysis)),
            "fallacy_of_division": await self.manipulation_agent.analyze(self.fallacy_of_division, text, str(argument_analysis)),
            "hasty_generalization": await self.manipulation_agent.analyze(self.hasty_generalization, text, str(argument_analysis)),
            "texas_sharpshooter_fallacy": await self.manipulation_agent.analyze(self.texas_sharpshooter_fallacy, text, str(argument_analysis))
        }
        
        return manipulation_analyses


    def raw_data_to_api_format(self, raw_analysis_dict: dict) -> dict:
        """Convert raw analysis data to API format"""

        argument_analysis = raw_analysis_dict.pop('argument_analysis')
        thesis = argument_analysis.get('main_hypothesis').get('statement')
        analysis = {
            'thesis': thesis,
            'arguments': []
        }
        # Construct the main frame of the analaysis dictionary response
        arguments = argument_analysis.get('arguments')
        for argument in arguments:
            _type = argument.get('_type')
            statememt = argument.get('statement')
            connection_to_hypothesis = argument.get('connection_to_hypothesis')
            arg_object = {
                '_type': _type,
                'statement': statememt,
                'connection_to_hypothesis': connection_to_hypothesis,
                'manipulations': {
                    'ad_populum': [],
                    'unspecified_authority_fallacy': [],
                    'appeal_to_pride': [],
                    'false_dilemma': [],
                    'cherry_picking_data': [],
                    'stork_fallacy': [],
                    'fallacy_of_composition': [],
                    'fallacy_of_division': [],
                    'hasty_generalization': [],
                    'texas_sharpshooter_fallacy': [],
                }
            }
            analysis["arguments"].append(arg_object)            

        arguments_processed = analysis.get('arguments')

        # Loop over raw manipulations data, meaning first ad_populum, then unspecified authority fallacy, etc
        for manipulation_name, manipulation_details in raw_analysis_dict.items():
            # Loop over constructed arguments response, meaning in the fnal analysis go over each argument 
            for processed_argument in arguments_processed:
                # Find current argument in the raw manipulation data
                # these are all the arguments
                raw_manipulations_per_argument = manipulation_details.get('arguments')
                # text of current proccessed argument 
                current_processed_argument_text = processed_argument.get('statement')
                for raw_argument in raw_manipulations_per_argument:
                    #get the text of the raw argument
                    raw_arg_text = raw_argument.get('argument_text')
                    is_current_argument = raw_arg_text == current_processed_argument_text
                    contains_manipulation = raw_argument.get('contains_manipulation')
                    # check if the raw_arguments is the same as the current processed argument
                    if is_current_argument and contains_manipulation:
                        processed_argument_manipulations = processed_argument.get('manipulations')
                        current_manipulation_processed = processed_argument_manipulations.get(manipulation_name)
                        raw_argument_manipulations = raw_argument.get('manipulations')
                        for raw_argument_manipulation in raw_argument_manipulations:
                            current_manipulation_processed.append(raw_argument_manipulation)
                        break
                    else:
                        continue

        
        an_args = analysis.get('arguments')
        for arg in an_args:
            log.info(f'{arg}\n')

        return analysis
# Initialize the analysis system
analysis_system = TextAnalysisSystem()

@app.post("/analyze", response_model=AnalysisOutput)
async def analyze_text_route(input_data: TextInput):
    """
    Analyze text for arguments and manipulation techniques
    """
    try:
        result = await analysis_system.analyze_text(input_data.text)
        return result
    except Exception as e:
        log.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)