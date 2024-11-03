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
            # Get main analysis
            analysis_response = self.model.generate_content(
                self.analysis_prompt.format(text=text)
            )
            
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
    try:
        # Get analysis
        result = analyzer.analyze_text(text)
        print("Analysis Results:")
        print(f'type of result is {type(result)}')

        # response: dict = json.loads(result)
        print(json.dumps(result.__dict__, indent=2))
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


    