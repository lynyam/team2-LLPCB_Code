from typing import List, Dict
import google.generativeai as genai
import json
from dataclasses import dataclass

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
        
        # Updated safety settings using correct category names
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

    # Rest of the class implementation remains the same
    def setup_prompts(self):

        self.arguments = """
        {{
            "main_hypothesis": {{
                "statement": "The European Union's Common Agricultural Policy (CAP) disproportionately benefits wealthy landowners, including billionaires, while failing to support small farmers and environmental sustainability."
            }},
            "arguments": [
                {{
                "type": "primary",
                "statement": "The analysis of official data from EU member states revealed that 17 billionaires were 'ultimate beneficiaries' linked to \u20ac3.3bn of EU farming handouts over a four-year period.",
                "connection_to_hypothesis": "This data provides concrete evidence of the claim that wealthy individuals are receiving a significant share of EU agricultural subsidies."
                }},
                {{
                "type": "primary",
                "statement": "Strict privacy rules, weak transparency requirements, and complex chains of company ownership make it difficult to scrutinize who receives EU farming subsidies.",
                "connection_to_hypothesis": "The lack of transparency allows wealthy individuals to obscure their ownership of companies receiving subsidies, further supporting the claim that the CAP benefits the wealthy."
                }},
                {{
                "type": "secondary",
                "statement": "The CAP hands out money based on the area of land a farmer owns rather than whether they need the support.",
                "connection_to_hypothesis": "This policy favors large landowners, who typically own more land, over small farmers who may be more in need of financial assistance."
                }},
                {{
                "type": "secondary",
                "statement": "Scientists have criticized 'perverse incentives' in the CAP that push farmers to destroy nature and that 50%-80% of EU farming subsidies go toward animal agriculture rather than foods that would be better for the health of people and the planet.",
                "connection_to_hypothesis": "The CAP's focus on quantity and area premiums incentivizes environmentally harmful practices and undermines the goal of sustainable agriculture."
                }}
            ],
            "counterarguments": [
                {{
                "statement": "A spokesperson for Dyson Farming argued that the family had invested \u00a3140m into sustainably improving its farms and farmland, in addition to the cost of land, which 'dwarfs any subsidy payments' received by Dyson Farming Ltd.",
                "how_addressed": "The author acknowledges Dyson's investment but emphasizes that the company has also benefited from 'many hundreds of millions of pounds in EU taxes and tariffs.'",
                "effectiveness": "moderate"
                }},
                {{
                "statement": "Thomas Dosch, the head of public affairs at T\u00f6nnies, argued that the company supported a 'reorientation' of European agricultural policy so that farmers who worked in environmentally friendly ways were compensated for the associated loss of income.",
                "how_addressed": "The author does not directly address this counterargument but highlights the need for 'sanctioning environmentally harmful behavior by imposing high costs.'",
                "effectiveness": "weak"
                }}
            ]
            }}
        """
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

        self.prompt_with_examples = """
        # Rhetorical Manipulation Analysis System

        You are a specialized text analyzer that identifies rhetorical manipulation in written content. Your output must be in valid JSON format for parsing. Analyze the provided text and respond using the following structure:

        Text:
        {text}

        ## Output Format

        You must output a single JSON object with this exact structure without quotes nor comments:

        {{
            "instances": [
                {{
                    "phrase": <str>,
                    "manipulation_type": {{
                        "primary": <str>,
                        "secondary": <str>,
                        "combined_techniques": [<str>, <str>]
                    }},
                    "explanation": <str>,
                }}
            ],
            }}
        }}

        ## Classification Categories

        The following must be used exactly for the "primary" field in manipulation_type:

        1. "EMOTIONAL_MANIPULATION"
        2. "LOGICAL_MANIPULATION"
        3. "LANGUAGE_MANIPULATION"
        4. "EVIDENCE_MANIPULATION"
        5. "ARGUMENTATIVE_MANIPULATION"
        6. "PSYCHOLOGICAL_MANIPULATION"
        7. "STRUCTURAL_MANIPULATION"
        8. "CONTEXTUAL_MANIPULATION"
        9. "SOURCE_MANIPULATION"
        10. "RESPONSE_MANIPULATION"

        For the "secondary" field, use these specific techniques:

        - Under EMOTIONAL_MANIPULATION:
        - "APPEAL_TO_FEAR"
        - "APPEAL_TO_PITY"
        - "APPEAL_TO_PRIDE"

        - Under LOGICAL_MANIPULATION:
        - "FALSE_CAUSATION"
        - "FALSE_EQUIVALENCE"
        - "SLIPPERY_SLOPE"

        [... similarly structured lists for all categories ...]

        ## Example

        Input: "Experts say you'd be crazy not to invest in CryptoX now. Don't be the only one left behind while everyone else gets rich!"

        Expected Output without comments or quotes:
        {{
        "instances": [
            {{
            "phrase": "Experts say",
            "manipulation_type": {{
                "primary": "SOURCE_MANIPULATION",
                "secondary": "ANONYMOUS_AUTHORITY",
                "combined_techniques": []
            }},
            "explanation": "Uses vague appeal to unnamed experts",
            }},
            {{
            "phrase": "you'd be crazy not to",
            "manipulation_type": {{
                "primary": "RESPONSE_MANIPULATION",
                "secondary": "THOUGHT_TERMINATING_CLICHE",
                "combined_techniques": ["EMOTIONAL_MANIPULATION"]
            }},
            "explanation": "Dismisses rational consideration by implying irrationality",
            }},
            {{
            "phrase": "Don't be the only one left behind",
            "manipulation_type": {{
                "primary": "PSYCHOLOGICAL_MANIPULATION",
                "secondary": "BANDWAGON_EFFECT",
                "combined_techniques": ["APPEAL_TO_FEAR"]
            }},
            "explanation": "Creates fear of missing out and social pressure",
            }}
        ],
        }}

        ## Analysis Instructions

        1. First, read through the entire text carefully.
        2. Identify each instance of manipulation.
        3. For each instance:
        - Extract the exact phrase
        - Record its position in the text
        - Classify according to the manipulation types
        - Assign severity and confidence scores
        - Provide brief explanation
        4. Generate summary statistics.
        5. Output everything in valid JSON format.

        Important:
        - Ensure all JSON is properly formatted and valid
        - Use exact category names as specified
        - Include all required fields
        - Maintain consistent capitalization
        - Use snake_case for keys
        - Include string values in double quotes        

        """
    
        self.prompt_identify_arguments = """
        
        ### TASK
        Analysis Request: Generate JSON Analysis of Text Hypothesis and Arguments
        Please analyze the provided text and return the results in the following JSON structure. Consider all aspects carefully and ensure your response follows this exact format:
        

        ### TEST
        {text}

        ### OUTPUT
        In a json without quotes or comments
        {{
            "main_hypothesis": {{
                "statement": <str>,
            }},
            "arguments": [
                {{
                    "type": <str>, (primary|secondary),
                    "statement": <str>,(The argument being made),
                    "connection_to_hypothesis": <str>, (Explanation of how this supports the main claim),
                }}
            ],
            "counterarguments": [
                {{
                    "statement": <str>, (The opposing viewpoint),
                    "how_addressed": <str>, (How the author responds to this counterargument),
                    "effectiveness": <str>, (strong|moderate|weak)
                }}
            ],
        }}
        """

        self.prompt_with_examples_instances = """
        # Rhetorical Manipulation Analysis System

        You are a specialized text analyzer that identifies rhetorical manipulation in written content. Your output must be in valid JSON format for parsing. Analyze the provided text and respond using the following structure:

        Text:
        {text}

        ## Output Format

        You must output a single JSON object with this exact structure without quotes nor comments:

        {{
            "manipulations": [
                {{
                    "instances": <str>,
                    "manipulation_type": {{
                        "primary": <str>,
                        "secondary": <str>,
                        "combined_techniques": [<str>, <str>]
                    }},
                    "explanation": <str>,
                }}
            ],
            }}
        }}

        ## Classification Categories

        The following must be used exactly for the "primary" field in manipulation_type:

        1. "EMOTIONAL_MANIPULATION"
        2. "LOGICAL_MANIPULATION"
        3. "LANGUAGE_MANIPULATION"
        4. "EVIDENCE_MANIPULATION"
        5. "ARGUMENTATIVE_MANIPULATION"
        6. "PSYCHOLOGICAL_MANIPULATION"
        7. "STRUCTURAL_MANIPULATION"
        8. "CONTEXTUAL_MANIPULATION"
        9. "SOURCE_MANIPULATION"
        10. "RESPONSE_MANIPULATION"

        For the "secondary" field, use these specific techniques:

        - Under EMOTIONAL_MANIPULATION:
        - "APPEAL_TO_FEAR"
        - "APPEAL_TO_PITY"
        - "APPEAL_TO_PRIDE"

        - Under LOGICAL_MANIPULATION:
        - "FALSE_CAUSATION"
        - "FALSE_EQUIVALENCE"
        - "SLIPPERY_SLOPE"

        [... similarly structured lists for all categories ...]

        ## Example

        Expected Output without comments or quotes:
        {{
            "manipulations": [
                {{
                    "instance": "Research shows that 90 percent of experts agree this is the best approach. Scientists have proven that this method works.",
                    "manipulation_type": {{
                        "primary": "SOURCE_MANIPULATION",
                        "secondary": "ANONYMOUS_AUTHORITY",
                        "combined_techniques": []
                    }},
                    "explanation": "Uses vague appeal to unnamed experts",
                }},
                {{
                    "instance": "Listen, at these prices you'd be crazy not to buy now - it's just common sense!",
                    "manipulation_type": {{
                        "primary": "RESPONSE_MANIPULATION",
                        "secondary": "THOUGHT_TERMINATING_CLICHE",
                        "combined_techniques": ["EMOTIONAL_MANIPULATION"]
                    }},
                    "explanation": "Dismisses rational consideration by implying irrationality through the phrase 'you'd be crazy not to' and reinforces it with 'common sense', which acts as a thought-terminating cliché. The emotional manipulation comes from the implied judgment of someone's rationality if they disagree."
                }},
                {{
                    "instance": "Everyone is already protecting their data with this security solution - can you really risk being the only one left vulnerable to cyberattacks?",
                    "manipulation_type": {{
                        "primary": "PSYCHOLOGICAL_MANIPULATION",
                        "secondary": "BANDWAGON_EFFECT",
                        "combined_techniques": ["APPEAL_TO_FEAR"]
                    }},
                    "explanation": "Creates fear of missing out and social pressure",
                }}
            ],
        }}

        ## Analysis Instructions

        1. First, read through the entire text carefully.
        2. Identify each instance of manipulation.
        3. For each instance:
        - Extract the exact phrase
        - Record its position in the text
        - Classify according to the manipulation types
        - Assign severity and confidence scores
        - Provide brief explanation
        4. Generate summary statistics.
        5. Output everything in valid JSON format.

        Important:
        - Ensure all JSON is properly formatted and valid
        - Use exact category names as specified
        - Include all required fields
        - Maintain consistent capitalization
        - Use snake_case for keys
        - Include string values in double quotes        

        """

        self.prompt_with_instances_arguments_and_specific_examples = """
        ##CONTEXT:
            The following text:
            {text}
            Has as a arguments and counter arguments the following:
            {{
            "main_hypothesis": {{
                "statement": "The European Union's Common Agricultural Policy (CAP) disproportionately benefits wealthy landowners, including billionaires, while failing to support small farmers and environmental sustainability."
            }},
            "arguments": [
                {{
                "type": "primary",
                "statement": "The analysis of official data from EU member states revealed that 17 billionaires were 'ultimate beneficiaries' linked to \u20ac3.3bn of EU farming handouts over a four-year period.",
                "connection_to_hypothesis": "This data provides concrete evidence of the claim that wealthy individuals are receiving a significant share of EU agricultural subsidies."
                }},
                {{
                "type": "primary",
                "statement": "Strict privacy rules, weak transparency requirements, and complex chains of company ownership make it difficult to scrutinize who receives EU farming subsidies.",
                "connection_to_hypothesis": "The lack of transparency allows wealthy individuals to obscure their ownership of companies receiving subsidies, further supporting the claim that the CAP benefits the wealthy."
                }},
                {{
                "type": "secondary",
                "statement": "The CAP hands out money based on the area of land a farmer owns rather than whether they need the support.",
                "connection_to_hypothesis": "This policy favors large landowners, who typically own more land, over small farmers who may be more in need of financial assistance."
                }},
                {{
                "type": "secondary",
                "statement": "Scientists have criticized 'perverse incentives' in the CAP that push farmers to destroy nature and that 50%-80% of EU farming subsidies go toward animal agriculture rather than foods that would be better for the health of people and the planet.",
                "connection_to_hypothesis": "The CAP's focus on quantity and area premiums incentivizes environmentally harmful practices and undermines the goal of sustainable agriculture."
                }}
            ]
            }}

            ### Manipulation Categories and Techniques

                ### 1. Emotional Manipulation
                Emotional manipulation uses language intended to evoke strong emotions, such as fear, anger, or sympathy, to bypass rational analysis. Focus on these specific techniques:

                - **Appeal to Fear**: Evokes fear or anxiety to prompt immediate action or agreement.
                - *Examples*: "Imagine the disaster if…" or "This could ruin your future."

                - **Appeal to Pity**: Uses language intended to elicit sympathy or compassion.
                - *Examples*: "Think of the children suffering" or "These families need your help."

                - **Appeal to Pride**: Attempts to flatter or appeal to the reader's sense of pride or superiority.
                - *Examples*: "Only the smartest investors act now" or "You deserve better."

                ### 2. Logical Manipulation
                Logical manipulation relies on flawed reasoning or fallacies to make an argument seem more convincing. Identify these specific techniques:

                - **False Causation**: Suggests a causal link between two events simply because one followed the other.
                - *Examples*: "Since the new policy, productivity has increased" (implying causation without evidence).

                - **False Equivalence**: Treats two situations or outcomes as if they are the same or equally valid, even when they are not.
                - *Examples*: "If we allow this, we should allow anything" or "This is just as bad as…".

                - **Slippery Slope**: Suggests that a minor action will lead to extreme, often negative, outcomes without evidence of progression.
                - *Examples*: "If we let this happen, it will eventually lead to…"

                ### 3. Evidence Manipulation
                Evidence manipulation involves misrepresenting or selectively presenting information to mislead. Focus on these techniques:

                - **Cherry-Picking Data**: Selectively presents data that supports the argument while ignoring data that contradicts it.
                - *Examples*: "Studies show a 90% success rate" (while omitting conflicting results or details about conditions).

                - **Unspecified Source or Anonymous Authority**: Refers to vague sources like “experts” or “studies” without citing specific or credible information.
                - *Examples*: "Experts agree…" or "Studies have shown…" without further details.

                - **Misleading Statistics**: Uses percentages, averages, or other figures out of context to create a specific impression.
                - *Examples*: "Crime rates increased by 50%" without mentioning the low baseline or scope of data.


        ## TASK

            # Rhetorical Manipulation Analysis System

            You are a specialized text analyzer that identifies rhetorical manipulation in written content that tries to prove the above arguments. Your output must be in valid JSON format for parsing. Analyze the provided text and respond using the following structure:

        ## OUTPUT

        You must output a single JSON object with this exact structure without quotes nor comments:

        ## Example Output without comments or quotes:
        {{
            "main_thesis": "This is the primary claim or thesis of the article as understood from the text.",
            "arguments": [
                {{
                    "argument_text": "Studies show a 90% success rate with this product, and experts agree it's the best option.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "Studies show a 90% success rate with this product",
                            "manipulation_type": {{
                                "primary": "EVIDENCE_MANIPULATION",
                                "secondary": "CHERRY_PICKING_DATA",
                                "combined_techniques": []
                            }},
                            "explanation": "Selectively presents success data without context or mention of failures."
                        }},
                        {{
                            "instance": "Experts agree it's the best option",
                            "manipulation_type": {{
                                "primary": "EVIDENCE_MANIPULATION",
                                "secondary": "UNSPECIFIED_SOURCE",
                                "combined_techniques": []
                            }},
                            "explanation": "Appeals to anonymous authority by using 'experts' without specifying sources."
                        }}
                    ]
                }},
                {{
                    "argument_text": "Only the smartest investors know to act now before it's too late.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "Only the smartest investors know to act now",
                            "manipulation_type": {{
                                "primary": "EMOTIONAL_MANIPULATION",
                                "secondary": "APPEAL_TO_PRIDE",
                                "combined_techniques": []
                            }},
                            "explanation": "Attempts to flatter the reader by implying only 'smart' people act immediately."
                        }}
                    ]
                }},
                {{
                    "argument_text": "If we allow this policy, it will lead to a total loss of individual freedoms.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "If we allow this policy, it will lead to a total loss of individual freedoms.",
                            "manipulation_type": {{
                                "primary": "LOGICAL_MANIPULATION",
                                "secondary": "SLIPPERY_SLOPE",
                                "combined_techniques": []
                            }},
                            "explanation": "Suggests that a minor policy change will lead to extreme outcomes without evidence."
                        }}
                    ]
                }}
            ]
        }}

        ## Analysis Instructions

        1. Read the entire text carefully to understand its main thesis and arguments.
        2. Identify the main thesis or primary claim of the article.
        3. Identify and list each argument supporting the thesis.
        4. For each argument:
            - Check if it contains manipulative rhetoric within the categories of Emotional Manipulation, Logical Manipulation, or Evidence Manipulation.
            - If manipulative, identify specific instances of manipulation.
            - Classify each instance according to the techniques in the relevant category.
            - Provide a brief explanation for each identified manipulation.
        5. Output everything in valid JSON format.

        Important:
        - Ensure all JSON is properly formatted and valid.
        - Use exact category names as specified.
        - Include all required fields.
        - Maintain consistent capitalization.
        - Use snake_case for keys.
        - Include string values in double quotes.



            
        """

        self.prompt_with_instances_arguments_and_specific_examples_text2 = """
            ##CONTEXT:
            # Rhetorical Manipulation Analysis System

            You are a specialized text analyzer that identifies rhetorical manipulation in written content. Your output must be in valid JSON format for parsing. Focus only on three types of manipulation: Emotional Manipulation, Logical Manipulation, and Evidence Manipulation. For each instance of manipulation, classify it according to the specific techniques listed below.

            The following text:
            {text}

            Arguments of the text
            {{
            "main_hypothesis": {{
                "statement": "Donald Trump is mentally unfit to be president of the United States.",
            }},
            "arguments": [
                {{
                    "type": "primary",
                    "statement": "Trump has made numerous bizarre and irrational statements, both on the campaign trail and in office.",
                    "connection_to_hypothesis": "These statements suggest that Trump is not in control of his faculties and is not fit to be president."
                }},
                {{
                    "type": "primary",
                    "statement": "Trump has been diagnosed with narcissistic personality disorder by mental health professionals.",
                    "connection_to_hypothesis": "Narcissistic personality disorder is a serious mental illness that can impair a person's judgment and decision-making abilities."
                }},
                {{
                    "type": "secondary",
                    "statement": "Trump's behavior has become increasingly erratic and unpredictable in recent months.",
                    "connection_to_hypothesis": "This suggests that Trump's mental health is deteriorating and that he is becoming more dangerous."
                }}
            ]
        }}
        ### Manipulation Categories and Techniques

                ### 1. Emotional Manipulation
                Emotional manipulation uses language intended to evoke strong emotions, such as fear, anger, or sympathy, to bypass rational analysis. Focus on these specific techniques:

                - **Appeal to Fear**: Evokes fear or anxiety to prompt immediate action or agreement.
                - *Examples*: "Imagine the disaster if…" or "This could ruin your future."

                - **Appeal to Pity**: Uses language intended to elicit sympathy or compassion.
                - *Examples*: "Think of the children suffering" or "These families need your help."

                - **Appeal to Pride**: Attempts to flatter or appeal to the reader's sense of pride or superiority.
                - *Examples*: "Only the smartest investors act now" or "You deserve better."

                ### 2. Logical Manipulation
                Logical manipulation relies on flawed reasoning or fallacies to make an argument seem more convincing. Identify these specific techniques:

                - **False Causation**: Suggests a causal link between two events simply because one followed the other.
                - *Examples*: "Since the new policy, productivity has increased" (implying causation without evidence).

                - **False Equivalence**: Treats two situations or outcomes as if they are the same or equally valid, even when they are not.
                - *Examples*: "If we allow this, we should allow anything" or "This is just as bad as…".

                - **Slippery Slope**: Suggests that a minor action will lead to extreme, often negative, outcomes without evidence of progression.
                - *Examples*: "If we let this happen, it will eventually lead to…"

                ### 3. Evidence Manipulation
                Evidence manipulation involves misrepresenting or selectively presenting information to mislead. Focus on these techniques:

                - **Cherry-Picking Data**: Selectively presents data that supports the argument while ignoring data that contradicts it.
                - *Examples*: "Studies show a 90% success rate" (while omitting conflicting results or details about conditions).

                - **Unspecified Source or Anonymous Authority**: Refers to vague sources like “experts” or “studies” without citing specific or credible information.
                - *Examples*: "Experts agree…" or "Studies have shown…" without further details.

                - **Misleading Statistics**: Uses percentages, averages, or other figures out of context to create a specific impression.
                - *Examples*: "Crime rates increased by 50%" without mentioning the low baseline or scope of data.


        ## TASK

            # Rhetorical Manipulation Analysis System

            You are a specialized text analyzer that identifies rhetorical manipulation in written content that tries to prove the above arguments. Your output must be in valid JSON format for parsing. Analyze the provided text and respond using the following structure:
            Your tasks is to indentify for each arguments, if throughout the text there are instances of manipulation

        ## OUTPUT

        You must output a single JSON object with this exact structure without quotes nor comments:

        ## Example Output without comments or quotes:
        {{
            "main_thesis": "This is the primary claim or thesis of the article as understood from the text.",
            "arguments": [
                {{
                    "argument_text": "Studies show a 90% success rate with this product, and experts agree it's the best option.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "Studies show a 90% success rate with this product",
                            "manipulation_type": {{
                                "primary": "EVIDENCE_MANIPULATION",
                                "secondary": "CHERRY_PICKING_DATA",
                                "combined_techniques": []
                            }},
                            "explanation": "Selectively presents success data without context or mention of failures."
                        }},
                        {{
                            "instance": "Experts agree it's the best option",
                            "manipulation_type": {{
                                "primary": "EVIDENCE_MANIPULATION",
                                "secondary": "UNSPECIFIED_SOURCE",
                                "combined_techniques": []
                            }},
                            "explanation": "Appeals to anonymous authority by using 'experts' without specifying sources."
                        }}
                    ]
                }},
                {{
                    "argument_text": "Only the smartest investors know to act now before it's too late.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "Only the smartest investors know to act now",
                            "manipulation_type": {{
                                "primary": "EMOTIONAL_MANIPULATION",
                                "secondary": "APPEAL_TO_PRIDE",
                                "combined_techniques": []
                            }},
                            "explanation": "Attempts to flatter the reader by implying only 'smart' people act immediately."
                        }}
                    ]
                }},
                {{
                    "argument_text": "If we allow this policy, it will lead to a total loss of individual freedoms.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "If we allow this policy, it will lead to a total loss of individual freedoms.",
                            "manipulation_type": {{
                                "primary": "LOGICAL_MANIPULATION",
                                "secondary": "SLIPPERY_SLOPE",
                                "combined_techniques": []
                            }},
                            "explanation": "Suggests that a minor policy change will lead to extreme outcomes without evidence."
                        }}
                    ]
                }}
            ]
        }}

        ## Analysis Instructions

        1. Read the entire text carefully to understand its main thesis and arguments.
        2. Identify the main thesis or primary claim of the article.
        3. Identify and list each argument supporting the thesis.
        4. For each argument:
            - Check if it contains manipulative rhetoric within the categories of Emotional Manipulation, Logical Manipulation, or Evidence Manipulation.
            - If manipulative, identify specific instances of manipulation.
            - Classify each instance according to the techniques in the relevant category.
            - Provide a brief explanation for each identified manipulation.
        5. Output everything in valid JSON format.

        Important:
        - Ensure all JSON is properly formatted and valid.
        - Use exact category names as specified.
        - Include all required fields.
        - Maintain consistent capitalization.
        - Use snake_case for keys.
        - Include string values in double quotes.

        """
    

        self.prompt_capu = """
        # Rhetorical Manipulation Analysis System

        You are a specialized text analyzer that identifies rhetorical manipulation in written content. Your output must be in valid JSON format for parsing. Focus only on three types of manipulation: Emotional Manipulation, Logical Manipulation, and Evidence Manipulation. For each instance of manipulation, classify it according to the specific techniques listed below.

        Text:
        {text}

        ## Output Format

        You must output a single JSON object with this exact structure without quotes or comments:

        {{
            "main_thesis": "<str>",
            "arguments": [
                {{
                    "argument_text": "<str>",
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
        }}

        ## Manipulation Categories and Techniques

        ### 1. Emotional Manipulation
        Emotional manipulation uses language intended to evoke strong emotions, such as fear, anger, or sympathy, to bypass rational analysis. Focus on these specific techniques:

        - **Appeal to Fear**: Evokes fear or anxiety to prompt immediate action or agreement.
          - *Examples*: "Imagine the disaster if…" or "This could ruin your future."

        - **Appeal to Pity**: Uses language intended to elicit sympathy or compassion.
          - *Examples*: "Think of the children suffering" or "These families need your help."

        - **Appeal to Pride**: Attempts to flatter or appeal to the reader’s sense of pride or superiority.
          - *Examples*: "Only the smartest investors act now" or "You deserve better."

        ### 2. Logical Manipulation
        Logical manipulation relies on flawed reasoning or fallacies to make an argument seem more convincing. Identify these specific techniques:

        - **False Causation**: Suggests a causal link between two events simply because one followed the other.
          - *Examples*: "Since the new policy, productivity has increased" (implying causation without evidence).

        - **False Equivalence**: Treats two situations or outcomes as if they are the same or equally valid, even when they are not.
          - *Examples*: "If we allow this, we should allow anything" or "This is just as bad as…".

        - **Slippery Slope**: Suggests that a minor action will lead to extreme, often negative, outcomes without evidence of progression.
          - *Examples*: "If we let this happen, it will eventually lead to…"

        ### 3. Evidence Manipulation
        Evidence manipulation involves misrepresenting or selectively presenting information to mislead. Focus on these techniques:

        - **Cherry-Picking Data**: Selectively presents data that supports the argument while ignoring data that contradicts it.
          - *Examples*: "Studies show a 90% success rate" (while omitting conflicting results or details about conditions).

        - **Unspecified Source or Anonymous Authority**: Refers to vague sources like “experts” or “studies” without citing specific or credible information.
          - *Examples*: "Experts agree…" or "Studies have shown…" without further details.

        - **Misleading Statistics**: Uses percentages, averages, or other figures out of context to create a specific impression.
          - *Examples*: "Crime rates increased by 50%" without mentioning the low baseline or scope of data.

        ## Example Output without comments or quotes:
        {{
            "main_thesis": "This is the primary claim or thesis of the article as understood from the text.",
            "arguments": [
                {{
                    "argument_text": "Studies show a 90% success rate with this product, and experts agree it's the best option.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "Studies show a 90% success rate with this product",
                            "manipulation_type": {{
                                "primary": "EVIDENCE_MANIPULATION",
                                "secondary": "CHERRY_PICKING_DATA",
                                "combined_techniques": []
                            }},
                            "explanation": "Selectively presents success data without context or mention of failures."
                        }},
                        {{
                            "instance": "Experts agree it's the best option",
                            "manipulation_type": {{
                                "primary": "EVIDENCE_MANIPULATION",
                                "secondary": "UNSPECIFIED_SOURCE",
                                "combined_techniques": []
                            }},
                            "explanation": "Appeals to anonymous authority by using 'experts' without specifying sources."
                        }}
                    ]
                }},
                {{
                    "argument_text": "Only the smartest investors know to act now before it's too late.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "Only the smartest investors know to act now",
                            "manipulation_type": {{
                                "primary": "EMOTIONAL_MANIPULATION",
                                "secondary": "APPEAL_TO_PRIDE",
                                "combined_techniques": []
                            }},
                            "explanation": "Attempts to flatter the reader by implying only 'smart' people act immediately."
                        }}
                    ]
                }},
                {{
                    "argument_text": "If we allow this policy, it will lead to a total loss of individual freedoms.",
                    "contains_manipulation": true,
                    "manipulations": [
                        {{
                            "instance": "If we allow this policy, it will lead to a total loss of individual freedoms.",
                            "manipulation_type": {{
                                "primary": "LOGICAL_MANIPULATION",
                                "secondary": "SLIPPERY_SLOPE",
                                "combined_techniques": []
                            }},
                            "explanation": "Suggests that a minor policy change will lead to extreme outcomes without evidence."
                        }}
                    ]
                }}
            ]
        }}

        ## Analysis Instructions

        1. Read the entire text carefully to understand its main thesis and arguments.
        2. Identify the main thesis or primary claim of the article.
        3. Identify and list each argument supporting the thesis.
        4. For each argument:
            - Check if it contains manipulative rhetoric within the categories of Emotional Manipulation, Logical Manipulation, or Evidence Manipulation.
            - If manipulative, identify specific instances of manipulation.
            - Classify each instance according to the techniques in the relevant category.
            - Provide a brief explanation for each identified manipulation.
        5. Output everything in valid JSON format.

        Important:
        - Ensure all JSON is properly formatted and valid.
        - Use exact category names as specified.
        - Include all required fields.
        - Maintain consistent capitalization.
        - Use snake_case for keys.
        - Include string values in double quotes.
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

    def analyze_text(self, text: str, prompt: str) -> AnalysisResult:
        """Main analysis function with improved error handling"""
        try:
            # responses = {}
            # Get main analysis
            analysis_response = self.model.generate_content(
                prompt.format(text=text)
            )
            return analysis_response
            
            # Extract and parse analysis text
            try:
                analysis_text = self.handle_response(analysis_response)
                print(f'analysis_text: {analysis_text}')
                return analysis_text
                # Clean the response text if needed
                # analysis_text = analysis_text.strip()
                # print('meow 2')
                # analysis_data = json.loads(analysis_text)
                # print('meow 3')
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Raw response text: {analysis_text}")
                # Attempt to clean and retry parsing
                cleaned_text = analysis_text.replace('\n', '').replace('\r', '')
                analysis_data = json.loads(cleaned_text)
            
            # # Get verification questions
            # verification_response = self.model.generate_content(
            #     self.verification_prompt.format(text=text)
            # )
            
            # # Extract and parse verification text
            # try:
            #     verification_text = self.handle_response(verification_response)
            #     verification_text = verification_text.strip()
            #     verification_data = json.loads(verification_text)
            # except json.JSONDecodeError as e:
            #     print(f"JSON parsing error: {str(e)}")
            #     print(f"Raw response text: {verification_text}")
            #     # Attempt to clean and retry parsing
            #     cleaned_text = verification_text.replace('\n', '').replace('\r', '')
            #     verification_data = json.loads(cleaned_text)
            
            # return AnalysisResult(
            #     manipulation_score=analysis_data.get("analysis_score", 0),
            #     rhetorical_devices=analysis_data.get("rhetorical_devices", []),
            #     main_arguments=analysis_data.get("main_arguments", []),
            #     reasoning_patterns=analysis_data.get("reasoning_patterns", []),
            #     verification_questions=verification_data.get("verification_questions", [])
            # )
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            if 'analysis_response' in locals():
                print("Response details:")
                print(f"Candidates: {analysis_response.candidates}")
                if hasattr(analysis_response, 'prompt_feedback'):
                    print(f"Prompt feedback: {analysis_response.prompt_feedback}")
            raise

    def get_chat_response(self, user_input: str) -> str:
        """Get interactive responses with error handling"""
        try:
            response = self.chat.send_message(user_input)
            return self.handle_response(response)
        except Exception as e:
            print(f"Chat error: {str(e)}")
            return "Unable to generate response"


def create_analyzer(api_key: str) -> GeminiAnalyzer:
    return GeminiAnalyzer(api_key)

def analyze_text_for_manipulation(text, analyzer, prompt, prefix):
    try:
        # Get analysis from Gemini
        result = analyzer.analyze_text(text, prompt)
        
        # Extract the text content from the GenerateContentResponse object
        response_text = result.text
        
        # Parse the text content as JSON
        parsed_result = json.loads(response_text)
        
        # Print for debugging
        print(f"Analysis Results - :{prefix}\n")
        print(json.dumps(parsed_result, indent=2))
        
        return parsed_result
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from model response: {str(e)}")
        print(f"Raw response text: {response_text}")  # This will help debug JSON parsing issues
        return None
    except AttributeError as e:
        print(f"Error accessing response properties: {str(e)}")
        print(f"Response type: {type(result)}")
        print(f"Response content: {result}")
        return None
    except Exception as e:
        print(f"Error processing analysis: {str(e)}")
        return None

def main():
    # Initialize analyzer
    
    analyzer = create_analyzer("AIzaSyBoaHgH2fhKTtuHloOHqHP8Qsbjfbvgysg")
    
    # Sample text
    
    text = """
In displaying all the signs that he is off his rocker, the Republican candidate has infected millions of others

Sat 2 Nov 2024 18.00 CET
Is Donald Trump going mad? It depends how you define the word. But since he's hoping to be elected US president on Tuesday, it would be handy to know. Democrats describe him as “weird” and “unhinged”. His rival, Kamala Harris, raised the “M” question again last week. “This is someone who is “unstable, obsessed with revenge, consumed with grievance, and out for unchecked power,” she warned.

Harris, to her credit, was being relatively polite, though goodness knows why, given the way he disses and demeans her. So let's pose the question in more colloquial, idiomatic terms. Has stark raving Trump finally lost his marbles? Are there bats in the belfry? If he's off his rocker, not playing with a full deck and away with the fairies, the world and the voters have a right to know.

Harris's assessment is obviously not an objective medical diagnosis of mental disorder. It's a normal person's reaction to the abnormal things Trump says and does. Crazy-strange campaign speeches by him and his supporters, notably at Madison Square Garden last weekend - a gathering akin to a Nazi Nuremberg rally - are reviving the debate about his sanity that began during his first term.

In The Dangerous Case of Donald Trump, published in 2017, a group of 27 psychiatrists, psychologists, and other mental health professionals raised numerous red flags. One contributor suggested he was clearly off his chump: “Trump is now the most powerful head of state in the world, and one of the most impulsive, arrogant, ignorant, disorganised, chaotic, nihilistic, self-contradictory, self-important, and self-serving.”

That professional opinion, made seven years ago, still rings true. Yet is the madness of “King” Trump, like the madness of King George (whose tyrannical rule Trump seeks to emulate), getting worse?

By one measure - his wild, deranged language - the deterioration is marked. “His speeches have grown coarser and coarser,” wrote veteran White House watcher Peter Baker, who dubs him “the profanity president”.

“Counting tamer four-letter words like `damn' and `hell,' he has cursed in public at least 1,787 times in 2024,” Baker wrote. His analysis shows Trump is using such language 69% more often than when he ran in 2016. It's shocking, even by today's tawdry standards. Trump calls Harris a “shit vice-president” who is “mentally impaired”. Doubtless he knows of what he speaks.

Vulgarity, however gross, is not proof of madness. But it may be symptomatic. The Merriam-Webster dictionary, America's oldest, defines a mad person as one “completely unrestrained by reason and judgment; unable to think in a clear or sensible way”. Trump aces this definition every time he opens his mouth. It fits him to a tee. Exhibit A: his oddball musings about golfer Arnold Palmer's penis.

Bizarre Trump traits, such as compulsive, blatant lying, meet another dictionary definition of madness - behaviour that is “incapable of being explained or accounted for”.

A third definition, rooted in US rather than British usage, suggests that Trump is indisputably bananas, in the sense that he is constantly “intensely angry or displeased”. Always feeling furious, feeling “mad as hell”, must be exhausting. It's enough to drive anyone round the bend. Older people often get irritable, of course; and screw-loose Trump is 78. So is incipient senility, or cognitive decline, another cause of his exceptional looney-ness?

By publicly projecting and displaying mental dysfunction daily on a national stage, he is driving America nuts, too
Trump stumbles, mispronounces words, forgets where he is and loses his train of thought. Just like Joe Biden, in fact. But Biden is merely old. Trump is nuts.

Trump has refused to take credible mental acuity tests or release his medical records. Last month, more than 230 healthcare specialists urged him to be more transparent. “As we all age, we lose sharpness and revert to base instincts,” they noted. “We are seeing that from Trump as he uses his rallies… to crudely lash out.”

It may go back to childhood. One theory is that Trump, bullied and bullier, was driven up the wall by maternal love denied. Another theory is that he suffers from “disinhibition”. This is when people become less restrained, the older they get.

But the Atlantic journalist McKay Coppins, who interviewed Trump 10 years ago, says he's always been this way. His “depthless vanity, his brittle ego, his tragic craving for elite approval” haven't changed one bit, Coppins wrote.

Narcissism, hedonism, obsession, a need to provoke, scare, shock and scandalise, and chronic, paranoid feelings of victimhood are all indicators of worsening mental imbalance, if not early-onset imbecility. Recent Trump lunacies include claims that flies are buzzing round his head for “suspicious” reasons, North Korea is trying to kill him, the 6 January riot was a “lovefest”, pet-eating migrants are akin to Hannibal Lecter, and that God saved him in the assassination attempt on his life.

If Trump were to go mad on his own time, no problem. Unfortunately, by publicly projecting and displaying mental dysfunction daily on a national stage, he is driving America nuts, too - fans and foes alike. He brings out the worst in everyone, right and left. It could be termed national derangement syndrome (NDS).

The poisonous effect of NDS was on show at Madison Square Garden, where “comedians” amplified Trump's sexist, racist, hate-filled messages. This superspreader craziness destroys reasoned debate, splits the country into opposing camps (hence the dead-heat opinion polls) and sends blood pressure soaring. Many Americans fear civil violence. That's bonkers.

This collective madness, akin to mass hysteria, is all-consuming and universally destructive. Like much that happens in America, it reverberates around the globe. Trump's fascistic Mad Hatter world is also the world of sicko revanchist dictators like Russia's Putin, Europe's far-right ultra-nationalist fruitcases, Iran's manic mullahs and off-their-heads Israeli génocidaires.

It's a mad, mad, mad, mad world - to hijack the title of Stanley Kramer's 1963 comedy classic - but it's no laughing matter. It may be about to get madder still.

 Simon Tisdall is the Observer's Foreign Affairs Commentator
    """
    
    text_2 = """
    The European Union gave generous farming subsidies to the companies of more than a dozen billionaires between 2018 and 2021, the Guardian can reveal, including companies owned by the former Czech prime minister Andrej Babiš and the British businessman Sir James Dyson.

Billionaires were “ultimate beneficiaries” linked to €3.3bn (£2.76bn) of EU farming handouts over the four-year period even as thousands of small farms were closed down, according to the analysis of official but opaque data from EU member states.

The 17 “ultimate beneficiaries” who featured on the 2022 Forbes rich list include Babiš, the former Czech prime minister who was acquitted in February of fraud involving farming subsidies; Dyson, the British vacuum cleaner tycoon who argued that Britain should leave the EU and whose company received payments before Brexit; and Guangchang Guo, a Chinese investor who owns Wolverhampton Wanderers football club.

Other billionaire beneficiaries of EU taxpayer funds include Clemens Tönnies, the German meat magnate who admitted he “was wrong” about Vladimir Putin in 2022; Anders Holch Povlsen, the Danish rewilding enthusiast and UK private landowner; and Kjeld Kirk Kristiansen, the Danish toymaker and former CEO of Lego.

“It's madness,” said Benoît Biteau, a French organic farmer and MEP for the Greens in the last European parliament. “The vast majority of farmers are struggling to make a living.”

The EU gives one-third of its entire budget to farmers through its common agricultural policy (Cap), which hands out money based on the area of land a farmer owns rather than whether they need the support.

But strict privacy rules, weak transparency requirements and complex chains of company ownership mean little scrutiny has been possible of who gets the money. In a study commissioned by the European parliament's budgetary control committee in 2021, researchers from the Centre for European Policy Studies (Ceps) found that it is “currently de facto impossible” to identify the largest ultimate beneficiaries of EU funding with full confidence.

To make a best estimate, the researchers linked data on farm subsidy recipients from each member state with a commercial database of companies. Working backwards from the recipients, they identified people who owned at least 25% of a company at each step of the ownership chain to work out the “ultimate beneficiaries”.

In some cases, the researchers were unable to trace the money because it went to regional bodies who redistributed the cash.

The analysis looked at the final natural person at the end of a chain of companies, said Damir Gojsic, a financial markets researcher who co-wrote the Ceps report and updated the analysis for the Guardian. “Ideally, you would focus on millionaires, but there isn't a list of millionaires out there.”

Gojsic found 17 billionaires had received EU farming handouts through companies they owned wholly or in part over the four-year period. The total sum of money linked to the billionaires was €3.3bn but the chain of companies was too complex and imprecise to weight the amounts by their ownership stake, he said.

Scientists have criticised “perverse incentives” in the Cap that push farmers to destroy nature. They estimate that 50%-80% of EU farming subsidies go toward animal agriculture rather than foods that would be better for the health of people and the planet.

“We need a rapid food transition for a healthier future and subsidies are the biggest economic lever for change,” said Paul Behrens, a global change researcher at Leiden University, who was not involved in the study.

He said: “The inequality in the Cap is extreme and this work highlights again just how much the richest land-owners continue to get richer from subsidies. Although transparency in the Cap has improved over time, the amount of detective work needed to uncover how the public's tax money is spent is astonishing.”

Most of the 17 billionaires did not respond to requests for comment. A handful declined to comment.

Dyson wrote a letter to the Guardian last year arguing he has “never supported the basis of the Cap”. A spokesperson for Dyson Farming said the family had invested £140m into sustainably improving its farms and farmland, in addition to the cost of land, which “dwarfs any subsidy payments” received by Dyson Farming Ltd. They said: “Its companies have also contributed many hundreds of millions of pounds in EU taxes and tariffs.

“The farms now employ more than 250 people and use agri-technology and innovation to support UK food security. In 2023 alone, Dyson Farming sustainably produced 40,000 tonnes of wheat, 12,000 tonnes of potatoes and 750 tonnes of out-of-season British strawberries, which avoid the air miles and carbon impact of fruit imported from overseas.”

Thomas Dosch, the head of public affairs at Tönnies, said the company supported a “reorientation” of European agricultural policy so that farmers who worked in environmentally friendly ways were compensated for the associated loss of income. “No subsidies should be paid for quantity of products or as area premiums per hectare,” he said.

Another option would be to sanction environmentally harmful behaviour by imposing high costs, he added. “However, if this were to lead to much higher food prices and perhaps even to food shortages, I believe this would be politically unacceptable.”
    """
    try:
        # Get analysis
        results = {}
        # original = analyze_text_for_manipulation(text_2, analyzer, analyzer.analysis_prompt)
        # phrases = analyze_text_for_manipulation(text_2, analyzer, analyzer.prompt_with_examples)
        # instances = analyze_text_for_manipulation(text_2, analyzer, analyzer.prompt_with_examples_instances)
        # arguments = analyze_text_for_manipulation(text_2, analyzer, analyzer.prompt_identify_arguments)
        arguments = analyze_text_for_manipulation(text, analyzer, analyzer.prompt_with_instances_arguments_and_specific_examples_text2, 'only manipulation analysis prompt')
        arguments = analyze_text_for_manipulation(text, analyzer, analyzer.prompt_capu, 'Capu prompt')

        # arguments_specific_examples = analyze_text_for_manipulation(text_2, analyzer, analyzer.prompt_with_instances_arguments_and_specific_examples)


        # results['phrases'] = phrases
        # instances['instances'] = instances
        # result = analyzer.analyze_text(text)
        # print("Analysis Results:")
        # print(f'type of result is {type(result)}')

        # response: dict = json.loads(result)
        # print(json.dumps(result.__dict__, indent=2))
        # print(json.dumps(response.__dict__, indent=2))

        # print(json.dumps(result))
        
        # # Example of streaming analysis
        # print("\nStreaming Analysis:")
        # for chunk in analyzer.stream_analysis(text):
        #     print(chunk, end="", flush=True)
            
        # # Example of chat interaction
        # print("\n\nChat Example:")
        # response = analyzer.get_chat_response("What are the main manipulative phrases in this text?")
        # print(f"Response: {response}")
        
    except Exception as e:
        print(f"Main error: {str(e)}")

if __name__ == "__main__":
    main()


    