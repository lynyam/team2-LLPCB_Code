from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import getpass
import os
import json

from logger import get_logger

log = get_logger()

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
            "type": "<primary|secondary>",
            "statement": "<text>",
            "connection_to_hypothesis": "<text>"
        }}
    ]
}}""")
        ])

    def analyze(self, text: str) -> dict:
        """Run the argument analysis."""
        chain = self.prompt | self.llm
        response = chain.invoke({"text": text})
        
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
            ("system", f"""You are an expert in detecting manipulation and persuasion techniques in text. Your task is to:
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
                                    "manipulation_type": {{
                                        "primary": "<str>",
                                        "secondary": "<str>",
                                        "combined_techniques": ["<str>", "<str>"]
                                    }},
                                    "explanation": "<str>"
                                }}
                            ]
                        }}
                    ]
                }}""")
        ])

    def analyze(self, manipulation_technique:str, text: str, arguments: str) -> dict:
        """Run the manipulation analysis."""
        chain = self.prompt | self.llm
        response = chain.invoke({"manipulation_technique": manipulation_technique, "text": text, "arguments": arguments})
        
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
                Examples: 'Ice cream sales and drowning deaths both increase in summer, therefore ice cream causes drownings',
                'Violent crime rates drop when more ice cream is sold, therefore ice cream prevents violence'. """
        self.fallacy_of_composition = """
        - Fallacy of Composition: assumes that if each part of a whole has a quality, the whole must also have that quality.
                Examples.: 'this bag contains feathers, feathers are light, therefore this bag is light'."""
        self.fallacy_of_division = """
        - Fallacy of Division: assumes that if a whole has a quality, all its parts must have that quality too.
                Examples: 'This boat floats, therefore every piece of this boat floats'."""
        self.hasty_generalization = """
        - Hasty Generalization: extends characteristics of a small sample to a larger group.
                Examples: 'I know two people from Chicago who are rude, therefore all people from Chicago must be rude,
                'My friend tried this diet and got sick, so this diet must be dangerous for everyone.'"""
        self.texas_sharpshooter_fallacy = """
        - Texas Sharpshooter Fallacy: a fallacy which is committed when differences in data are ignored, but similarities are overemphasized.
                Example: 'A company claims their training program is highly effective by only highlighting the 5 employees who got promotions after taking it, while ignoring the 95 who saw no career advancement'"""
    
    def analyze_text(self, text: str) -> dict:
        """Perform both argument and manipulation analysis on the text."""
        argument_analysis = self.argument_agent.analyze(text)

        # Analyze for each type of manipulation
        ad_populum = self.manipulation_agent.analyze(self.ad_populum, text, str(argument_analysis))
        unspecified_authority_fallacy = self.manipulation_agent.analyze(self.unspecified_authority_fallacy, text, str(argument_analysis))
        appeal_to_pride = self.manipulation_agent.analyze(self.appeal_to_pride, text, str(argument_analysis))
        false_dilemma = self.manipulation_agent.analyze(self.false_dilemma, text, str(argument_analysis))
        cherry_picking_data = self.manipulation_agent.analyze(self.cherry_picking_data, text, str(argument_analysis))
        stork_fallacy = self.manipulation_agent.analyze(self.stork_fallacy, text, str(argument_analysis))
        fallacy_of_composition = self.manipulation_agent.analyze(self.fallacy_of_composition, text, str(argument_analysis))
        fallacy_of_division = self.manipulation_agent.analyze(self.fallacy_of_division, text, str(argument_analysis))
        hasty_generalization = self.manipulation_agent.analyze(self.hasty_generalization, text, str(argument_analysis))
        texas_sharpshooter_fallacy = self.manipulation_agent.analyze(self.texas_sharpshooter_fallacy, text, str(argument_analysis))


        
        return {
            "argument_analysis": argument_analysis,
            "ad_populum": ad_populum,
            "unspecified_authority_fallacy": unspecified_authority_fallacy,
            "appeal_to_pride": appeal_to_pride,
            "false_dilemma": false_dilemma,
            "cherry_picking_data": cherry_picking_data,
            "stork_fallacy": stork_fallacy,
            "fallacy_of_composition": fallacy_of_composition,
            "fallacy_of_division": fallacy_of_division,
            "hasty_generalization": hasty_generalization,
            "texas_sharpshooter_fallacy": texas_sharpshooter_fallacy
        }

def main():
    # Check for API key
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

    # Initialize the analysis system
    analysis_system = TextAnalysisSystem()
    
    # Test analysis
    test_text = """
    You can't afford to wait any longer - climate change is destroying our planet RIGHT NOW! 
    All reputable scientists agree that we have less than 5 years to act. 
    Only a fool would ignore the overwhelming evidence. If you care about your children's future, 
    you must support immediate and drastic action. Big Oil wants you to doubt this, but they're 
    just protecting their profits while the world burns. Join us now or be on the wrong side of history!
    """
    
    results = analysis_system.analyze_text(test_text)
    
    log.info("\nArgument Analysis:")
    print(json.dumps(results["argument_analysis"], indent=2))
    log.info("\nad_populum:")
    print(json.dumps(results["ad_populum"], indent=2))
    log.info("\nunspecified_authority_fallacy:")
    print(json.dumps(results["unspecified_authority_fallacy"], indent=2))
    log.info("\nappeal_to_pride:")
    print(json.dumps(results["appeal_to_pride"], indent=2))
    log.info("\nfalse_dilemma:")
    print(json.dumps(results["false_dilemma"], indent=2))
    log.info("\ncherry_picking_data:")
    print(json.dumps(results["cherry_picking_data"], indent=2))
    log.info("\nstork_fallacy:")
    print(json.dumps(results["stork_fallacy"], indent=2))
    log.info("\nfallacy_of_composition:")
    print(json.dumps(results["fallacy_of_composition"], indent=2))
    log.info("\nfallacy_of_division:")
    print(json.dumps(results["fallacy_of_division"], indent=2))
    log.info("\nhasty_generalization:")
    print(json.dumps(results["hasty_generalization"], indent=2))
    log.info("\ntexas_sharpshooter_fallacy:")
    print(json.dumps(results["texas_sharpshooter_fallacy"], indent=2))


if __name__ == "__main__":
    main()