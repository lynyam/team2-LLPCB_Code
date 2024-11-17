from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import json
import asyncio
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

### TEXT
{text}

### OUTPUT
{{
    "main_hypothesis": {{
        "statement": "<text>"
    }},
    "arguments": [
        {{
            "_type": "<primary|secondary>",
            "statement": "<text>", write the statement in the original language of the text
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
1. Analyze the given text for manipulation techniques that are used to support or strengthen arguments
2. Focus specifically on how arguments are presented and supported, not whether the arguments themselves are inherently manipulative

                """),
            ("human", """### 
             
                ### TASK
                Focus only on the following manipulation technique:
                {manipulation_technique}

                Analysis Request: Generate JSON Analysis of Manipulation Techniques

                For each provided argument:
                1. Examine the text surrounding and supporting this argument
                2. Identify specific instances where the above stated manipulation technique is used to:
                - Support the argument
                - Strengthen its persuasiveness
                - Convince readers of its validity
                3. For each identified instance:
                - Extract the exact manipulative text
                - Explain how it uses this manipulation to support the argument
                - Note: Focus on HOW the argument is supported, not WHETHER the argument itself is manipulative

                Example distinction:
                - Argument: "We should reduce carbon emissions"
                - Don't analyze: Whether this argument itself is manipulative
                - Do analyze: Whether manipulation techniques are used to support this argument

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
                                    "instance": "<str>", keep the instance in the original language of the text
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
    - Argumentum ad populum (Appeal to the People): Claims something is true because many/most people believe it.
            Core concept: Substitutes popular opinion for evidence
            Examples: 'Most people believe in ghosts, so they must exist'
                     'Everyone says this restaurant is the best, so it must be'
            Counter: Popularity doesn't determine truth - many widely held beliefs have been proven wrong"""

        self.unspecified_authority_fallacy = """
        - Unspecified Authority fallacy: References unnamed or vague authorities to support claims.
                Core concept: Creates false credibility through anonymous expertise
                Examples: 'Scientists say this product is revolutionary'
                        'Research has shown that...' (without citing specific studies)
                Counter: Ask for specific sources and credentials of the claimed authorities"""

        self.appeal_to_pride = """
        - Appeal to Pride: Manipulates audience by associating agreement with positive qualities.
                Core concept: Exploits desire to belong to a "superior" group
                Examples: 'Sophisticated people understand why this art is valuable'
                        'Any true patriot would support this policy'
                Counter: Evaluate claims on their merits, not on implied social status"""

        self.false_dilemma = """
        - False Dilemma (Black and White Thinking): Reduces complex situations to only two opposing options.
                Core concept: Artificially limits choices to force a particular conclusion
                Examples: 'Either support this war or you're against our troops'
                        'You're either with us or against us'
                Counter: Identify and explore other possible alternatives"""

        self.cherry_picking_data = """
        - Cherry-Picking Data: Selectively presents favorable evidence while omitting contradictory data.
                Core concept: Creates misleading conclusions through incomplete evidence
                Examples: 'Our product worked for these 10 selected customers' (ignoring 90 failures)
                        'Crime dropped during my term' (ignoring areas where it increased)
                Counter: Ask for complete data sets and contrary evidence"""

        self.stork_fallacy = """
        - Correlation vs. Causality (Stork fallacy): Mistakes correlation for causation.
                Core concept: Assumes that when two things occur together, one must cause the other
                Examples: 'Sales increased when we changed the logo, so the logo caused higher sales'
                        'Violent crime rises with ice cream sales, so ice cream causes violence'
                Counter: Investigate other potential causes and confounding variables"""

        self.fallacy_of_composition = """
        - Fallacy of Composition: Incorrectly applies properties of parts to the whole.
                Core concept: Assumes what's true of components must be true of the entire system
                Examples: 'Each player on the team is a star, so this must be the best team'
                        'Every part of this machine is light, so the machine must be light'
                Counter: Consider how parts interact and combine in the whole"""

        self.fallacy_of_division = """
        - Fallacy of Division: Wrongly attributes properties of the whole to individual parts.
                Core concept: Assumes what's true of the whole must be true of all parts
                Examples: 'This company is rich, so all its employees must be rich'
                        'Humans are conscious beings, so all human cells must be conscious'
                Counter: Examine whether the property can logically apply to individual components"""

        self.hasty_generalization = """
        - Hasty Generalization: Draws broad conclusions from insufficient evidence.
                Core concept: Makes sweeping claims based on small or unrepresentative samples
                Examples: 'My friend got food poisoning at a Mexican restaurant, so Mexican food is unsafe'
                        'It snowed in April, so climate change must be fake'
                Counter: Ask about sample size and representativeness"""

        self.texas_sharpshooter_fallacy = """
        - Texas Sharpshooter Fallacy: Cherry-picks data clusters while ignoring scattered data.
                Core concept: Finds patterns in randomness by focusing only on clustered results
                Examples: 'Looking at only successful stock trades to prove trading strategy works'
                        'Noting cancer clusters without considering population density'
                Counter: Examine all data points and consider broader context"""

    async def analyze_text(self, text: str) -> dict:
        """Perform analysis and return in API format"""
        raw_results = await self._analyze_raw(text)
        return self.raw_data_to_api_format(raw_results)

    async def _analyze_raw(self, text: str) -> dict:
        """Perform both argument and manipulation analysis on the text concurrently."""
        # First get the argument analysis since other analyses depend on it
        argument_analysis = await self.argument_agent.analyze(text)
        
        # Define all manipulation techniques and their corresponding definitions
        manipulation_tasks = {
            "ad_populum": self.ad_populum,
            "unspecified_authority_fallacy": self.unspecified_authority_fallacy,
            "appeal_to_pride": self.appeal_to_pride,
            "false_dilemma": self.false_dilemma,
            "cherry_picking_data": self.cherry_picking_data,
            "stork_fallacy": self.stork_fallacy,
            "fallacy_of_composition": self.fallacy_of_composition,
            "fallacy_of_division": self.fallacy_of_division,
            "hasty_generalization": self.hasty_generalization,
            "texas_sharpshooter_fallacy": self.texas_sharpshooter_fallacy
        }
        
        # Create coroutines for each manipulation analysis
        async def analyze_manipulation(name: str, definition: str) -> tuple:
            """Helper function to run manipulation analysis and return result with its name"""
            result = await self.manipulation_agent.analyze(definition, text, str(argument_analysis))
            return (name, result)
        
        # Gather all manipulation analysis tasks
        tasks = [
            analyze_manipulation(name, definition) 
            for name, definition in manipulation_tasks.items()
        ]
        
        # Run all manipulation analyses concurrently
        manipulation_results = await asyncio.gather(*tasks)
        
        # Combine results into final dictionary
        manipulation_analyses = {
            "argument_analysis": argument_analysis,
            **dict(manipulation_results)
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

        self.print_anaysis(analysis)

        return analysis
    
    def print_anaysis(self, analysis: dict) -> None:
        thesis = analysis.get('thesis')
        log.debug(f'Thesis: {thesis}')
        an_args = analysis.get('arguments')
        for arg in an_args:
            statement = arg.get('statement')
            _type = arg.get('_type')
            manipulations = arg.get('manipulations')
            ad_populum = manipulations.get('ad_populum')
            unspecified_authority_fallacy = manipulations.get('unspecified_authority_fallacy')
            appeal_to_pride = manipulations.get('appeal_to_pride')
            false_dilemma = manipulations.get('false_dilemma')
            cherry_picking_data = manipulations.get('cherry_picking_data')
            stork_fallacy = manipulations.get('stork_fallacy')
            fallacy_of_composition = manipulations.get('fallacy_of_composition')
            fallacy_of_division = manipulations.get('fallacy_of_division')
            hasty_generalization = manipulations.get('hasty_generalization')
            texas_sharpshooter_fallacy = manipulations.get('texas_sharpshooter_fallacy')
            log.trace(f'argument: {statement}')
            log.trace(f'type: {_type}')
            log.info(f'ad_populum: {ad_populum}')
            log.info(f'unspecified_authority_fallacy: {unspecified_authority_fallacy}')
            log.info(f'appeal_to_pride: {appeal_to_pride}')
            log.info(f'false_dilemma: {false_dilemma}')
            log.info(f'cherry_picking_data: {cherry_picking_data}')
            log.info(f'stork_fallacy: {stork_fallacy}')
            log.info(f'fallacy_of_composition: {fallacy_of_composition}')
            log.info(f'fallacy_of_division: {fallacy_of_division}')
            log.info(f'hasty_generalization: {hasty_generalization}')
            log.info(f'texas_sharpshooter_fallacy: {texas_sharpshooter_fallacy}')
            print('\n')

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